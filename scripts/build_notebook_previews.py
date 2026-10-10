"""Render honest notebook previews without rewriting source notebooks."""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import logging
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from _support.downloads import get_custom_logger  # noqa: E402

logger = get_custom_logger(__name__)


def historical_outputs(notebook: dict, historical: dict) -> int:
    """Attach preserved outputs only to exactly matching source cells.

    :param notebook: Disposable notebook representation to update.
    :param historical: Byte-preserved historical notebook representation.
    :returns: Number of output-bearing matching cells restored.
    """
    matched = 0
    for current, original in zip(notebook["cells"], historical["cells"]):
        if (
            current["cell_type"] == original["cell_type"] == "code"
            and "".join(current["source"]) == "".join(original["source"])
            and original.get("outputs")
        ):
            current["outputs"] = original["outputs"]
            current["execution_count"] = original.get("execution_count")
            matched += 1
    return matched


def render_preview(notebook, output: Path, source: Path, record: dict) -> None:
    """Write an HTML preview with an explicit execution-status banner.

    :param notebook: Notebook containing genuine outputs or source-only content.
    :param output: HTML destination.
    :param source: Original notebook path for navigation.
    :param record: Auditable status, source hash and execution details.
    :returns: None.
    :raises OSError: If the output cannot be written.
    """
    from nbconvert import HTMLExporter

    # Report missing legacy attachments without changing the original notebook.
    presentation = copy.deepcopy(notebook)
    missing = []
    for index, cell in enumerate(presentation.cells):
        if cell.cell_type != "markdown":
            continue

        def replace_attachment(match, cell=cell, index=index):
            name = match.group(2)
            if name in cell.get("attachments", {}):
                return match.group(0)
            missing.append({"cell": index, "name": name})
            return "[Missing historical attachment: " + name + "]"

        cell.source = re.sub(
            r"!\[([^\]]*)\]\(attachment:([^)]+)\)", replace_attachment, cell.source
        )
    record["missing_attachments"] = missing
    exporter = HTMLExporter(template_name="lab", embed_images=True)
    body, _ = exporter.from_notebook_node(presentation)
    link = os.path.relpath(source, output.parent)
    banner = (
        '<aside style="border:2px solid #446;padding:1rem;margin:1rem">'
        "<strong>Execution status: "
        + html.escape(record["status"])
        + "</strong><p>"
        + html.escape(record["detail"])
        + '</p><a href="'
        + html.escape(link, quote=True)
        + '">Source notebook</a></aside>'
    )
    body, replacements = re.subn(
        r"(<body\b[^>]*>)", lambda match: match.group(1) + banner, body, count=1
    )
    if replacements != 1:
        raise ValueError("HTML exporter did not produce a body element")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(body)
    logger.info("Rendered %s: %s", source.name, record["status"])


def execute_preview(
    source: Path,
    output: Path,
    record_path: Path,
    kernel_python: Path,
    *,
    work_directory: Path | None = None,
    blocked_reason: str | None = None,
    historical: Path | None = None,
    cell_timeout: int = 45,
) -> dict:
    """Execute in a supplied disposable worktree and render its result.

    :param source: Source notebook, never modified.
    :param output: HTML preview destination.
    :param record_path: JSON status destination.
    :param kernel_python: Existing environment's Python interpreter.
    :param work_directory: Disposable input/project directory for execution.
    :param blocked_reason: Explicit reason to render without execution.
    :param historical: Optional preserved outputs for blocked previews.
    :param cell_timeout: Maximum execution time per cell in seconds.
    :returns: Execution status and preservation/provenance metadata.
    :raises ValueError: If execution is requested without a work directory.
    :raises OSError: If source or output files cannot be accessed.
    """
    import nbformat
    from jupyter_client import KernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError, CellTimeoutError

    original_bytes = source.read_bytes()
    # Empty list metadata occurs in historical R exports; normalize only the render copy.
    representation = json.loads(original_bytes)
    metadata_repairs = []
    for index, cell in enumerate(representation["cells"]):
        if cell.get("metadata") == []:
            cell["metadata"] = {}
            metadata_repairs.append(index)
    notebook = nbformat.reads(json.dumps(representation), as_version=4)
    record = {
        "source_sha256": hashlib.sha256(original_bytes).hexdigest(),
        "kernel_python": str(kernel_python),
        "seed": 4242,
        "cell_timeout_seconds": cell_timeout,
        "memory_limit_bytes": 4 * 1024**3,
        "historical_output_cells": 0,
        "empty_metadata_cells_normalized": metadata_repairs,
    }
    if blocked_reason:
        record.update(status="blocked", detail=blocked_reason)
        if historical and historical.is_file():
            archived = json.loads(historical.read_text())
            record["historical_output_cells"] = historical_outputs(notebook, archived)
        if record["historical_output_cells"]:
            record["detail"] += (
                " Preserved historical outputs are shown for exactly matching cells; "
                "they are not results of a fresh run."
            )
        else:
            record["detail"] += (
                " Source-only preview; no computed results are available."
            )
    else:
        if work_directory is None:
            raise ValueError("Execution requires a disposable work directory")
        # Isolate kernel registration and fix the execution environment explicitly.
        with tempfile.TemporaryDirectory(prefix="notebook-kernel-") as kernel_root:
            specification = Path(kernel_root) / "kernels/preview"
            specification.mkdir(parents=True)
            specification.joinpath("kernel.json").write_text(
                json.dumps(
                    {
                        "argv": [
                            str(kernel_python),
                            "-m",
                            "ipykernel_launcher",
                            "-f",
                            "{connection_file}",
                        ],
                        "display_name": "Isolated preview",
                        "language": "python",
                        "env": {
                            "MPLBACKEND": "Agg",
                            "OMP_NUM_THREADS": "1",
                            "OPENBLAS_NUM_THREADS": "1",
                            "MKL_NUM_THREADS": "1",
                            "PYTHONHASHSEED": "0",
                            "IPYTHONDIR": str(Path(kernel_root) / "ipython"),
                            "JUPYTER_RUNTIME_DIR": str(Path(kernel_root) / "runtime"),
                        },
                    }
                )
            )
            manager = KernelManager(
                kernel_name="preview",
                connection_file=str(Path(kernel_root) / "connection.json"),
                transport="ipc",
                kernel_spec_manager=KernelSpecManager(
                    kernel_dirs=[str(specification.parent)]
                ),
            )
            setup = (
                "# Preview execution setup; original source is unchanged.\n"
                "import resource\n"
                "resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))\n"
                "import random\nimport numpy as np\n"
                "random.seed(4242)\nnp.random.seed(4242)\n"
                "%matplotlib inline\n"
            )
            code = "\n".join(
                cell.source for cell in notebook.cells if cell.cell_type == "code"
            )
            if "import torch" in code or "from torch" in code:
                setup += "import torch\ntorch.manual_seed(4242)\n"
            notebook.cells.insert(0, nbformat.v4.new_code_cell(setup))
            client = NotebookClient(
                notebook,
                km=manager,
                timeout=cell_timeout,
                resources={"metadata": {"path": str(work_directory)}},
            )
            logger.info("Executing %s", source.name)
            try:
                client.execute()
                record.update(
                    status="executed",
                    detail="Fresh execution completed in source cell order with seed 4242. Historical results were not substituted.",
                )
            except CellTimeoutError:
                record.update(
                    status="timeout",
                    detail=f"A cell exceeded {cell_timeout} seconds. Earlier outputs are partial results; the notebook did not complete.",
                )
            except CellExecutionError as error:
                record.update(
                    status="failed",
                    detail=f"Fresh execution stopped at {error.ename}: {error.evalue}. Earlier outputs are partial results.",
                )
            except (OSError, RuntimeError) as error:
                logger.error("Kernel execution failed", exc_info=True)  # noqa: G201
                record.update(
                    status="failed",
                    detail=f"Kernel execution failed: {type(error).__name__}",
                )
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
    record["output_cells"] = sum(
        bool(cell.get("outputs")) for cell in notebook.cells if cell.cell_type == "code"
    )
    source_cells = notebook.cells if blocked_reason else notebook.cells[1:]
    record["completed_source_cells"] = sum(
        cell.get("execution_count") is not None
        and not any(
            output.get("output_type") == "error" for output in cell.get("outputs", [])
        )
        for cell in source_cells
        if cell.cell_type == "code"
    )
    assert source.read_bytes() == original_bytes
    render_preview(notebook, output, source, record)
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    return record


def main() -> int:
    """Parse one preview job and report whether execution completed.

    :returns: Zero for a completed run or deliberately blocked rendering; one for failure/timeout.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--kernel-python", type=Path, required=True)
    parser.add_argument("--work-directory", type=Path)
    parser.add_argument("--blocked-reason")
    parser.add_argument("--historical", type=Path)
    parser.add_argument("--cell-timeout", type=int, default=45)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    record = execute_preview(
        args.source.resolve(),
        args.output.resolve(),
        args.record.resolve(),
        args.kernel_python.absolute(),
        work_directory=args.work_directory,
        blocked_reason=args.blocked_reason,
        historical=args.historical,
        cell_timeout=args.cell_timeout,
    )
    return int(record["status"] in {"failed", "timeout"})


if __name__ == "__main__":
    raise SystemExit(main())
