def check_temperature(temperature, rules):

    minimum, maximum = rules["ideal_temperature"]

    if minimum <= temperature <= maximum:
        return 100

    if temperature < minimum:
        difference = minimum - temperature
    else:
        difference = temperature - maximum

    score = 100 - (difference * 10)

    return max(0, score)


def check_rain(rain_probability, rules):

    maximum = rules["max_rain_probability"]

    if rain_probability <= maximum:
        return 100

    score = 100 - (
        (rain_probability - maximum)
        / (100 - maximum)
        * 100
    )

    return max(0, round(score))


def check_wind(wind_speed, rules):

    maximum = rules["max_wind"]

    if wind_speed <= 10:
        return 100

    score = 100 - (
        (wind_speed - 10)
        / (maximum - 10)
        * 100
    )

    return max(0, round(score))


def check_humidity(humidity, rules):

    minimum, maximum = rules["ideal_humidity"]

    if minimum <= humidity <= maximum:
        return 100

    if humidity < minimum:
        difference = minimum - humidity
    else:
        difference = humidity - maximum

    score = 100 - (difference * 5)

    return max(0, round(score))


def calculate_score(weather, weights, rules):

    temperature_score = check_temperature(
        weather["temperature"],
        rules
    )

    rain_score = check_rain(
        weather["rain_probability"],
        rules
    )

    wind_score = check_wind(
        weather["wind_speed"],
        rules
    )

    humidity_score = check_humidity(
        weather["humidity"],
        rules
    )

    final_score = (
        temperature_score * weights["temperature"]
        + rain_score * weights["rain"]
        + wind_score * weights["wind"]
        + humidity_score * weights["humidity"]
    )

    return round(final_score)


def get_risk(score):

    if score >= 80:
        return "LOW"

    elif score >= 60:
        return "MEDIUM"

    else:
        return "HIGH"