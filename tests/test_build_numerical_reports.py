"""Verify report staging, source preservation and failed-build behavior."""

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.build_numerical_reports import adapt_for_tectonic, build_report


class ReportBuildTests(unittest.TestCase):
    """Test the boundary between preserved sources and external compilation."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.report = Path(self.temporary.name) / "lab-02"
        self.original = self.report / "original"
        self.original.mkdir(parents=True)
        self.source = (
            r"\usepackage[T1]{fontenc}"
            "\n"
            r"\usepackage{polski}"
            "\n"
            r"\usepackage[pdftex,bookmarks]{hyperref}"
            "\n"
            r"\usepackage{pdfsync}"
            "\n"
            r"\author{Max Stróżyk}"
            "\n"
            r"\date{21 January 2025}"
            "\n"
            r"\begin{document}"
            "\n"
            r"\[x^{(k+1)} = D^{-1}(b-Rx^{(k)})\]"
            "\n"
        )
        (self.original / "main.tex").write_text(self.source)
        (self.original / "figure.png").write_bytes(b"original-figure")

    def test_unicode_compatibility_preserves_formula_and_explicit_date(self):
        adapted = adapt_for_tectonic(self.source)
        self.assertIn(r"\usepackage{fontspec}", adapted)
        self.assertIn(r"\usepackage[polish]{babel}", adapted)
        self.assertNotIn("pdftex,bookmarks", adapted)
        self.assertNotIn(r"\usepackage{pdfsync}", adapted)
        self.assertIn(r"\date{21 January 2025}", adapted)
        self.assertIn(r"\[x^{(k+1)} = D^{-1}(b-Rx^{(k)})\]", adapted)
        self.assertIn(r"\author{Max Stróżyk}", adapted)

    def test_staging_preserves_sources_and_illustrations(self):
        staged = []

        def compile_fixture(command, *, cwd, check):
            stage = Path(cwd)
            staged.append(stage)
            self.assertEqual(command, ["test-tectonic", "--keep-logs", "main.tex"])
            self.assertTrue(check)
            self.assertNotEqual(stage, self.original)
            self.assertIn(r"\usepackage{fontspec}", (stage / "main.tex").read_text())
            self.assertEqual((stage / "figure.png").read_bytes(), b"original-figure")
            (stage / "main.pdf").write_bytes(b"verified-compiler-output")

        with patch("scripts.build_numerical_reports.subprocess.run", compile_fixture):
            build_report(self.report, "original", "test-tectonic")
        self.assertEqual(
            (self.report / "report-pl.pdf").read_bytes(), b"verified-compiler-output"
        )
        self.assertEqual((self.original / "main.tex").read_text(), self.source)
        self.assertEqual(
            (self.original / "figure.png").read_bytes(), b"original-figure"
        )
        self.assertFalse(staged[0].exists())

    def test_failed_compilation_preserves_existing_pdf(self):
        output = self.report / "report-pl.pdf"
        output.write_bytes(b"existing-report")
        error = subprocess.CalledProcessError(1, ["test-tectonic"])
        with (
            patch("scripts.build_numerical_reports.subprocess.run", side_effect=error),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            build_report(self.report, "original", "test-tectonic")
        self.assertEqual(output.read_bytes(), b"existing-report")
        self.assertEqual((self.original / "main.tex").read_text(), self.source)


if __name__ == "__main__":
    unittest.main()
