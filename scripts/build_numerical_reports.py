"""Rebuild bilingual reports without modifying exact original LaTeX sources."""

import argparse
import logging
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from _support.downloads import get_custom_logger  # noqa: E402

logger = get_custom_logger(__name__)
ASSIGNMENTS = ROOT / "courses/numerical-methods/assignments"
REPORTS = {
    name: ASSIGNMENTS / name / "report"
    for name in [
        "lab-02",
        "lab-03",
        "lab-04",
        "lab-05",
        "lab-06",
        "importance-sampling",
    ]
}
REPORTS["linear-algebra-draft"] = ASSIGNMENTS / "lab-03/report-draft"


def adapt_for_tectonic(text: str) -> str:
    r"""Apply engine compatibility changes to a temporary source copy.

    :param text: Original or translated LaTeX source.
    :returns: Source compatible with Tectonic's XeTeX engine.

    Mathematical expressions, numerical results and original source files are
    preserved. Explicit report dates are retained.
    """
    # Remove legacy pdfTeX options and obsolete editor-synchronization packages.
    text = text.replace("[pdftex,bookmarks", "[bookmarks")
    text = text.replace(r"\usepackage{pdfsync}", "")
    text = text.replace(r"\usepackage{memhfixc}", "")
    # Use Unicode fonts so Polish source text and author names render correctly.
    text = text.replace(r"\usepackage[T1]{fontenc}", r"\usepackage{fontspec}")
    text = text.replace(r"\usepackage{polski}", r"\usepackage[polish]{babel}")
    text = text.replace(r"\usepackage[utf8]{inputenc}", "")
    # Supply the missing list environment used by the additional draft.
    if r"\begin{algindent}" in text:
        text = text.replace(
            r"\begin{document}",
            r"\newenvironment{algindent}{\begin{list}{}{\setlength{\leftmargin}{0pt}}}{\end{list}}"
            + "\n"
            + r"\begin{document}",
            1,
        )
    # REMARK: Missing dates otherwise render as the build date, which would make
    # historical reports appear to be newly submitted coursework.
    if r"\date{" not in text.replace(r"%\date{}", ""):
        text = text.replace(
            r"\begin{document}",
            r"\date{Winter 2024/2025}" + "\n" + r"\begin{document}",
            1,
        )
    # REMARK: A stray token outside every slide is present in the original export.
    # Removing it only in the build copy avoids a spurious presentation page.
    return text.replace("\neeeew\n", "\n")


def build_report(report: Path, version: str, tectonic: str) -> None:
    """Compile one version in isolation and replace its published PDF.

    :param report: Report directory containing original and english sources.
    :param version: Original or English source version.
    :param tectonic: Tectonic executable path.
    :raises subprocess.CalledProcessError: If LaTeX compilation fails.
    :raises OSError: If staging or publication fails.
    :side effects: Replaces report-pl.pdf or report-en.pdf after successful build.
    """
    logger.info("Building %s/%s/%s", report.parent.name, report.name, version)
    with tempfile.TemporaryDirectory(prefix="coursework-report-") as temporary:
        stage = Path(temporary) / "source"
        shutil.copytree(report / version, stage)
        for source in stage.glob("*.tex"):
            source.write_text(adapt_for_tectonic(source.read_text()))
        subprocess.run([tectonic, "--keep-logs", "main.tex"], cwd=stage, check=True)
        name = "report-pl.pdf" if version == "original" else "report-en.pdf"
        shutil.copyfile(stage / "main.pdf", report / name)
        logger.info("Published %s", report / name)


def main() -> int:
    """Build selected reports.

    :returns: Zero when all requested versions compile successfully.
    :raises FileNotFoundError: If Tectonic cannot be located.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tectonic", default=shutil.which("tectonic"))
    parser.add_argument(
        "--report",
        action="append",
        choices=sorted(REPORTS),
        help="Build this report only; repeat to select several reports.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if args.tectonic is None:
        raise FileNotFoundError("Install Tectonic or supply --tectonic.")
    reports = [REPORTS[name] for name in (args.report or sorted(REPORTS))]
    for report in reports:
        for version in ["original", "english"]:
            build_report(report, version, args.tectonic)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
