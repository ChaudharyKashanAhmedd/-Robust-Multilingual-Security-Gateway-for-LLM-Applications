import yaml


with open("config/gateway_config.yaml", "r") as file:

    config = yaml.safe_load(file)


RULE_THRESHOLD = config["rule_threshold"]

SEMANTIC_THRESHOLD = config["semantic_threshold"]

MASK_RISK = config["mask_risk"]


def make_policy_decision(rule_score,
                         semantic_score,
                         pii_entities):

    pii_detected = len(pii_entities) > 0

    final_risk = max(rule_score, semantic_score)

    reason_codes = []

    # BLOCK
    if (
        rule_score >= RULE_THRESHOLD
        or
        semantic_score >= SEMANTIC_THRESHOLD
    ):

        if semantic_score >= SEMANTIC_THRESHOLD:
            reason_codes.append("SEMANTIC_INJECTION")

        if rule_score >= RULE_THRESHOLD:
            reason_codes.append("RULE_BASED_ATTACK")

        return {

            "decision": "BLOCK",

            "final_risk": round(final_risk, 2),

            "reason_codes": reason_codes
        }

    # MASK
    if pii_detected:

        reason_codes.append("PII_DETECTED")

        return {

            "decision": "MASK",

            "final_risk": MASK_RISK,

            "reason_codes": reason_codes
        }

    # ALLOW
    reason_codes.append("SAFE_PROMPT")

    return {

        "decision": "ALLOW",

        "final_risk": round(final_risk, 2),

        "reason_codes": reason_codes
    }