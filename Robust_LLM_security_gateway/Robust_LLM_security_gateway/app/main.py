from fastapi import FastAPI
from pydantic import BaseModel

import time

from detectors.rule_detector import detect_rule_injection
from detectors.semantic_detector import detect_semantic_injection

from utils.language import detect_language
from utils.logger import save_audit_log

from pii.presidio_custom import analyze_pii

from policy.policy_engine import make_policy_decision


app = FastAPI(title="Robust LLM Security Gateway")


class PromptRequest(BaseModel):

    input_id: str
    text: str


@app.get("/")
def home():

    return {
        "message": "LLM Security Gateway Running"
    }


@app.post("/analyze")
def analyze_prompt(request: PromptRequest):

    start_time = time.time()

    language = detect_language(request.text)

    rule_result = detect_rule_injection(request.text)

    semantic_result = detect_semantic_injection(request.text)

    pii_result = analyze_pii(request.text)

    policy_result = make_policy_decision(

        rule_result["rule_score"],

        semantic_result["semantic_score"],

        pii_result["entities"]
    )

    latency_ms = round((time.time() - start_time) * 1000, 2)

    response = {

        "input_id": request.input_id,

        "language": language,

        "original_text": request.text,

        "rule_score": rule_result["rule_score"],

        "semantic_score": semantic_result["semantic_score"],

        "semantic_attack": semantic_result["is_attack"],

        "matched_rules": rule_result["matched_rules"],

        "pii_entities": pii_result["entities"],

        "safe_text": pii_result["masked_text"],

        "decision": policy_result["decision"],

        "final_risk": policy_result["final_risk"],

       "reason_codes": policy_result["reason_codes"],

        "latency_ms": latency_ms
    }

    save_audit_log(response)

    return response