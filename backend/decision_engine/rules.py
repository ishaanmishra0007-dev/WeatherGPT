SPRAYING_RULES = {
    "ideal_temperature": (18, 30),
    "max_wind": 15,
    "max_rain_probability": 30,
    "ideal_humidity": (40, 80),

    # Practical application period for our prototype
    "allowed_hours": (6, 18)
}

def check_humidity(humidity):

    minimum, maximum = SPRAYING_RULES["ideal_humidity"]

    if minimum <= humidity <= maximum:
        return 100
    else:
        return 0