ACTIVITIES = {

    "spraying": {
        "name": "Crop Spraying",

        "weights": {
            "temperature": 0.30,
            "rain": 0.40,
            "wind": 0.20,
            "humidity": 0.10
        },

        "rules": {
            "ideal_temperature": (18, 30),
            "max_wind": 15,
            "max_rain_probability": 30,
            "ideal_humidity": (40, 80)
        },

        "minimum_score": 80,
        "allowed_hours": (6, 18)
    },


    "running": {
        "name": "Running",

        "weights": {
            "rain": 0.40,
            "temperature": 0.30,
            "wind": 0.20,
            "humidity": 0.10
        },

        "rules": {
            "ideal_temperature": (10, 25),
            "max_wind": 25,
            "max_rain_probability": 50,
            "ideal_humidity": (30, 80)
        },

        "minimum_score": 70,
        "allowed_hours": (5, 21)
    },


    "outdoor_event": {
        "name": "Outdoor Event",

        "weights": {
            "temperature": 0.30,
            "rain": 0.40,
            "wind": 0.20,
            "humidity": 0.10
        },

        "rules": {
            "ideal_temperature": (15, 30),
            "max_wind": 25,
            "max_rain_probability": 30,
            "ideal_humidity": (30, 80)
        },

        "minimum_score": 70,
        "allowed_hours": (7, 22)
    }
}