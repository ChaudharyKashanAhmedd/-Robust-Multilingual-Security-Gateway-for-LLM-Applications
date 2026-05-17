import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from detectors.rule_detector import detect_rule_injection
from detectors.semantic_detector import detect_semantic_injection

from pii.presidio_custom import analyze_pii

from policy.policy_engine import make_policy_decision


data = pd.read_csv("data/final_eval.csv")

results = []

y_true = []
y_pred = []


for _, row in data.iterrows():

    text = row["prompt"]

    rule_result = detect_rule_injection(text)

    semantic_result = detect_semantic_injection(text)

    pii_result = analyze_pii(text)

    policy_result = make_policy_decision(

        rule_result["rule_score"],

        semantic_result["semantic_score"],

        pii_result["entities"]
    )

    predicted_policy = policy_result["decision"]

    results.append({

        "id": row["id"],

        "prompt": text,

        "expected_policy": row["expected_policy"],

        "predicted_policy": predicted_policy,

        "rule_score": rule_result["rule_score"],

        "semantic_score": semantic_result["semantic_score"]

    })

    # Binary classification
    expected_binary = 1 if row["expected_policy"] == "BLOCK" else 0

    predicted_binary = 1 if predicted_policy == "BLOCK" else 0

    y_true.append(expected_binary)

    y_pred.append(predicted_binary)


results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/evaluation_results.csv",
    index=False
)


# Metrics
accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(y_true, y_pred)

recall = recall_score(y_true, y_pred)

f1 = f1_score(y_true, y_pred)

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()


print("\n===== METRICS =====")

print(f"Accuracy: {accuracy:.2f}")

print(f"Precision: {precision:.2f}")

print(f"Recall: {recall:.2f}")

print(f"F1 Score: {f1:.2f}")

print(f"False Positives: {fp}")

print(f"False Negatives: {fn}")


metrics_summary = {

    "accuracy": round(accuracy, 2),

    "precision": round(precision, 2),

    "recall": round(recall, 2),

    "f1_score": round(f1, 2),

    "false_positives": int(fp),

    "false_negatives": int(fn)
}


pd.DataFrame([metrics_summary]).to_json(

    "results/metrics_summary.json",

    orient="records",

    indent=4
)

print("\nEvaluation completed.")