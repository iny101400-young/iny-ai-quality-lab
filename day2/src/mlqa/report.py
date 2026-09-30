"""성능 리포트 자동 생성.

실행: day2 폴더에서  python -m mlqa.report   (PYTHONPATH=src 필요, 아래 README 참고)
결과: reports/model_report.md, reports/confusion_matrix.png, reports/metrics.json
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix  # noqa: E402

from .evaluate import compute_metrics, cross_validate_model  # noqa: E402
from .model import build_model, load_data, split_data  # noqa: E402

LABELS = [0, 1]
LABEL_NAMES = ["malignant", "benign"]


def generate_report(out_dir="reports"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    # 1) 학습 데이터로 교차 검증
    cv = cross_validate_model(build_model(), X_train, y_train)

    # 2) 전체 학습 데이터로 학습 후 테스트 데이터로 한 번 평가
    model = build_model().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    test_metrics = compute_metrics(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred, labels=LABELS)

    ConfusionMatrixDisplay(cm, display_labels=LABEL_NAMES).plot(colorbar=False)
    plt.title("Confusion matrix (test set)")
    plt.tight_layout()
    plt.savefig(out / "confusion_matrix.png", dpi=120)
    plt.close()

    metrics = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "n_train": int(len(y_train)), "n_test": int(len(y_test)),
               "cross_validation": cv, "test": test_metrics}
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    lines = [
        "# 모델 성능 리포트",
        "",
        f"- 생성 시각 (UTC): {metrics['generated_at']}",
        f"- 데이터: 유방암 진단 (학습 {len(y_train)}건, 테스트 {len(y_test)}건), 양성 클래스 = malignant(0)",
        "- 모델: StandardScaler + LogisticRegression",
        "",
        "## 1. 5겹 층화 교차 검증 (학습 데이터)",
        "",
        "| 지표 | 평균 | 표준편차 | 폴드별 |",
        "| --- | --- | --- | --- |",
    ]
    for name, s in cv.items():
        folds = ", ".join(f"{v:.3f}" for v in s["folds"])
        lines.append(f"| {name} | {s['mean']:.3f} | {s['std']:.3f} | {folds} |")
    lines += [
        "",
        "## 2. 테스트 데이터 평가",
        "",
        "| 지표 | 값 |",
        "| --- | --- |",
    ]
    lines += [f"| {k} | {v:.3f} |" for k, v in test_metrics.items()]
    lines += [
        "",
        "![confusion matrix](confusion_matrix.png)",
        "",
        "```text",
        classification_report(y_test, y_pred, labels=LABELS, target_names=LABEL_NAMES, digits=3).rstrip(),
        "```",
        "",
    ]
    (out / "model_report.md").write_text("\n".join(lines), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    result = generate_report()
    print(json.dumps(result["test"], indent=2))
