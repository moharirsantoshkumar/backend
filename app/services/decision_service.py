from app.schemas.recommendation import Decision


def build_decision(product):

    return Decision(
        confidence=product["confidence"],
        summary=product["decision_summary"],
        tradeoff=product["tradeoff_vs_next"],
        best_for=product["best_for"],
    )