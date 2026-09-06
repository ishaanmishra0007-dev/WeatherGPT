from .activities import ACTIVITIES


def generate_reasons(weather, activity="spraying"):

    if activity not in ACTIVITIES:
        raise ValueError(
            f"Unknown activity: {activity}"
        )

    rules = ACTIVITIES[activity]["rules"]

    reasons = []

    # Rain
    maximum_rain = rules["max_rain_probability"]

    if weather["rain_probability"] <= maximum_rain * 0.67:
        reasons.append(
            f"Low precipitation probability ({weather['rain_probability']}%)"
        )
    elif weather["rain_probability"] <= maximum_rain:
        reasons.append(
            f"Moderate precipitation probability ({weather['rain_probability']}%)"
        )
    else:
        reasons.append(
            f"High precipitation probability ({weather['rain_probability']}%)"
        )

    # Wind
    maximum_wind = rules["max_wind"]

    if weather["wind_speed"] <= 10:
        reasons.append(
            f"Wind speed is suitable ({weather['wind_speed']} km/h)"
        )
    elif weather["wind_speed"] <= maximum_wind:
        reasons.append(
            f"Moderate wind conditions ({weather['wind_speed']} km/h)"
        )
    else:
        reasons.append(
            f"High wind speed ({weather['wind_speed']} km/h)"
        )

    # Temperature
    minimum_temp, maximum_temp = rules["ideal_temperature"]

    if minimum_temp <= weather["temperature"] <= maximum_temp:
        reasons.append(
            f"Temperature is favorable ({weather['temperature']}°C)"
        )
    else:
        reasons.append(
            f"Temperature is outside the preferred range ({weather['temperature']}°C)"
        )

    # Humidity
    minimum_humidity, maximum_humidity = rules["ideal_humidity"]

    if minimum_humidity <= weather["humidity"] <= maximum_humidity:
        reasons.append(
            f"Humidity is favorable ({weather['humidity']}%)"
        )
    else:
        reasons.append(
            f"Humidity is outside the preferred range ({weather['humidity']}%)"
        )

    return reasons