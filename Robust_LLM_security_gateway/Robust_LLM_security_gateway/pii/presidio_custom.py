import re

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import Pattern

from presidio_anonymizer import AnonymizerEngine


analyzer = AnalyzerEngine()

anonymizer = AnonymizerEngine()


# -----------------------------
# Custom CNIC Recognizer
# -----------------------------

cnic_pattern = Pattern(
    name="pakistani_cnic",
    regex=r"\d{5}-\d{7}-\d",
    score=0.95
)

cnic_recognizer = PatternRecognizer(
    supported_entity="CNIC",
    patterns=[cnic_pattern]
)

analyzer.registry.add_recognizer(cnic_recognizer)


# -----------------------------
# Student ID Recognizer
# -----------------------------

student_pattern = Pattern(
    name="student_id",
    regex=r"FA\d{2}-[A-Z]{3}-\d{3}",
    score=0.85
)

student_recognizer = PatternRecognizer(
    supported_entity="STUDENT_ID",
    patterns=[student_pattern]
)

analyzer.registry.add_recognizer(student_recognizer)


def analyze_pii(text):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    entities = []

    for result in results:

        detected_text = text[result.start:result.end]

        entities.append({
            "type": result.entity_type,
            "text": detected_text,
            "score": round(result.score, 2)
        })

    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    return {
        "entities": entities,
        "masked_text": anonymized_result.text
    }