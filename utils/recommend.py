def recommend_products(products, user_history):

    recommendations = []

    for p in products:
        score = 0

        # Price preference
        if p["price"] < 2000:
            score += 30
        elif p["price"] < 10000:
            score += 20

        # Popularity (simulate)
        score += 20

        # Based on user history
        if len(user_history) > 0:
            score += 30

        recommendations.append({
            "product": p,
            "score": score,
            "reason": generate_reason(p)
        })

    # Sort by score
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations


def generate_reason(product):

    if product["price"] < 1000:
        return "Recommended because it's budget-friendly and trending"

    elif product["price"] < 10000:
        return "Balanced product with good performance and demand"

    else:
        return "Premium product with high value and quality"