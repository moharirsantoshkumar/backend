from app.schemas.consensus import (
    Consensus,
    AIModelOpinion,
)


def generate_consensus(product: dict) -> Consensus:

    score = product.get("score", 0)

    confidence = product.get("confidence")

    opinions = []

    agreement = 0

    # GPT-4
    gpt_agrees = score >= 0.85

    opinions.append(

        AIModelOpinion(
            model="GPT-4",
            recommendation=product["name"] if gpt_agrees else "Alternative Product",
            reasoning="Excellent overall balance of price, rating and value."
            if gpt_agrees
            else "Another product may better fit niche requirements.",
            agrees_with_final=gpt_agrees,
        )

    )

    if gpt_agrees:
        agreement += 1

    # Claude
    claude_agrees = confidence and confidence.score >= 80

    opinions.append(

        AIModelOpinion(
            model="Claude",
            recommendation=product["name"] if claude_agrees else "Alternative Product",
            reasoning="High confidence recommendation with strong supporting evidence."
            if claude_agrees
            else "Confidence level suggests reviewing alternatives.",
            agrees_with_final=claude_agrees,
        )

    )

    if claude_agrees:
        agreement += 1

    # Gemini
    gemini_agrees = (
        product.get("pricing")
        and product["pricing"].price_status != "Market Price"
    )

    opinions.append(

        AIModelOpinion(
            model="Gemini",
            recommendation=product["name"] if gemini_agrees else "Alternative Product",
            reasoning="Current market pricing makes this a good purchase."
            if gemini_agrees
            else "Pricing could improve by waiting.",
            agrees_with_final=gemini_agrees,
        )

    )

    if gemini_agrees:
        agreement += 1

    agreement_score = round((agreement / 3) * 100)

    if agreement == 3:
        summary = "All AI models agree with this recommendation."
    elif agreement == 2:
        summary = "Most AI models agree with this recommendation."
    else:
        summary = "AI models have mixed opinions about this recommendation."

    return Consensus(
        agreement_score=agreement_score,
        majority_choice=product["name"],
        summary=summary,
        opinions=opinions,
    )