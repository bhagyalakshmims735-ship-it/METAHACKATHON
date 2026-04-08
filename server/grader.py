def grade(output):
    price = output["predicted_price"]
    time = output["estimated_time"]

    if price <= 0 or time <= 0:
        return 0.0

    if price < 400 and time < 100:
        return 1.0

    elif price < 700:
        return 0.7

    return 0.4