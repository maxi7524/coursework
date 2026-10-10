"""Check output provenance and preservation boundaries for HTML previews."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

from scripts.build_notebook_previews import historical_outputs


class HistoricalOutputTests(unittest.TestCase):
    """Retain historical results only where the corresponding code is exact."""

    def test_different_source_never_receives_historical_results(self):
        current = {"cells": [{"cell_type": "code", "source": "changed", "outputs": []}]}
        old = {
            "cells": [
                {"cell_type": "code", "source": "original", "outputs": ["result"]}
            ]
        }
        self.assertEqual(historical_outputs(current, old), 0)
        self.assertEqual(current["cells"][0]["outputs"], [])

    def test_exact_source_receives_attributed_results_and_execution_count(self):
        current = {"cells": [{"cell_type": "code", "source": "x", "outputs": []}]}
        old = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ["x"],
                    "outputs": ["result"],
                    "execution_count": 2,
                }
            ]
        }
        self.assertEqual(historical_outputs(current, old), 1)
        self.assertEqual(current["cells"][0]["outputs"], ["result"])
        self.assertEqual(current["cells"][0]["execution_count"], 2)

    @unittest.skipUnless(
        importlib.util.find_spec("nbconvert"),
        "Optional notebook rendering dependencies are unavailable",
    )
    def test_blocked_preview_preserves_source_and_exposes_status(self):
        import nbformat

        from scripts.build_notebook_previews import execute_preview

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.ipynb"
            nbformat.write(
                nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("print(1)")]),
                source,
            )
            original = source.read_bytes()
            record = execute_preview(
                source,
                root / "preview.html",
                root / "status.json",
                Path("/not-used"),
                blocked_reason="Missing input",
            )
            self.assertEqual(record["status"], "blocked")
            self.assertEqual(source.read_bytes(), original)
            rendered = (root / "preview.html").read_text()
            self.assertIn("Execution status: blocked", rendered)
            self.assertIn("Source-only preview", rendered)

    @unittest.skipUnless(
        importlib.util.find_spec("nbconvert"),
        "Optional notebook execution dependencies are unavailable",
    )
    def test_successful_execution_preserves_source_and_includes_results(self):
        import sys

        import nbformat

        from scripts.build_notebook_previews import execute_preview

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.ipynb"
            nbformat.write(
                nbformat.v4.new_notebook(
                    cells=[nbformat.v4.new_code_cell("print(6 * 7)")]
                ),
                source,
            )
            original = source.read_bytes()
            record = execute_preview(
                source,
                root / "preview.html",
                root / "status.json",
                Path(sys.executable),
                work_directory=root,
            )
            self.assertEqual(record["status"], "executed")
            self.assertEqual(record["completed_source_cells"], 1)
            self.assertEqual(source.read_bytes(), original)
            self.assertIn("42", (root / "preview.html").read_text())

    @unittest.skipUnless(
        importlib.util.find_spec("nbconvert"),
        "Optional notebook rendering dependencies are unavailable",
    )
    def test_missing_attachment_is_reported_without_rewriting_markdown(self):
        import nbformat

        from scripts.build_notebook_previews import render_preview

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            notebook = nbformat.v4.new_notebook(
                cells=[nbformat.v4.new_markdown_cell("![Figure](attachment:image.png)")]
            )
            record = {"status": "blocked", "detail": "Original environment unavailable"}
            render_preview(
                notebook, root / "preview.html", root / "source.ipynb", record
            )
            self.assertEqual(
                notebook.cells[0].source, "![Figure](attachment:image.png)"
            )
            self.assertEqual(
                record["missing_attachments"], [{"cell": 0, "name": "image.png"}]
            )
            self.assertIn(
                "Missing historical attachment", (root / "preview.html").read_text()
            )


class LegacyMetadataTests(unittest.TestCase):
    """Verify render-only recovery of an observed malformed R export."""

    @unittest.skipUnless(importlib.util.find_spec("nbconvert"), "nbconvert unavailable")
    def test_empty_list_metadata_is_normalized_without_source_changes(self):
        import json
        import sys

        from scripts.build_notebook_previews import execute_preview

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "legacy.ipynb"
            source.write_text(
                json.dumps(
                    {
                        "nbformat": 4,
                        "nbformat_minor": 5,
                        "metadata": {},
                        "cells": [
                            {
                                "cell_type": "code",
                                "id": "legacy-cell",
                                "metadata": [],
                                "source": "print(42)",
                                "outputs": [],
                                "execution_count": None,
                            }
                        ],
                    }
                )
            )
            original = source.read_bytes()
            record = execute_preview(
                source,
                root / "preview.html",
                root / "record.json",
                Path(sys.executable),
                blocked_reason="Original R kernel unavailable",
            )
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(record["empty_metadata_cells_normalized"], [0])
            self.assertIn("print", (root / "preview.html").read_text())


if __name__ == "__main__":
    unittest.main()
