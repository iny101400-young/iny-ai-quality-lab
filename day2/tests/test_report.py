"""성능 리포트 생성 테스트 (2일차 5교시)."""

import json

from mlqa.report import generate_report


def test_report_files_are_created(tmp_path):
    generate_report(out_dir=tmp_path)
    assert (tmp_path / "model_report.md").exists()
    assert (tmp_path / "confusion_matrix.png").exists()
    metrics = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert {"cross_validation", "test"} <= set(metrics)
