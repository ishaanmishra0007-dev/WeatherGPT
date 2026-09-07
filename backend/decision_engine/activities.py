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
    },


    "irrigation": {
        "name": "Crop Irrigation",

        "weights": {
            "temperature": 0.20,
            "rain": 0.50,
            "wind": 0.10,
            "humidity": 0.20
        },

        "rules": {
            "ideal_temperature": (15, 30),
            "max_wind": 20,
            "max_rain_probability": 30,
            "ideal_humidity": (40, 85)
        },

        "minimum_score": 70,
        "allowed_hours": (5, 20)
    },


    "cricket": {
        "name": "Cricket",

        "weights": {
            "temperature": 0.25,
            "rain": 0.40,
            "wind": 0.25,
            "humidity": 0.10
        },

        "rules": {
            "ideal_temperature": (18, 30),
            "max_wind": 25,
            "max_rain_probability": 30,
            "ideal_humidity": (30, 80)
        },

        "minimum_score": 70,
        "allowed_hours": (6, 21)
    },


    "football": {
        "name": "Football",

        "weights": {
            "temperature": 0.25,
            "rain": 0.40,
            "wind": 0.25,
            "humidity": 0.10
        },

        "rules": {
            "ideal_temperature": (15, 28),
            "max_wind": 25,
            "max_rain_probability": 35,
            "ideal_humidity": (30, 80)
        },

        "minimum_score": 70,
        "allowed_hours": (6, 21)
    },


    "driving": {
        "name": "Driving",

        "weights": {
            "temperature": 0.10,
            "rain": 0.50,
            "wind": 0.25,
            "humidity": 0.15
        },

        "rules": {
            "ideal_temperature": (10, 35),
            "max_wind": 35,
            "max_rain_probability": 30,
            "ideal_humidity": (30, 90)
        },

        "minimum_score": 65,
        "allowed_hours": (5, 23)
    },


    "travel": {
        "name": "Travel",

        "weights": {
            "temperature": 0.30,
            "rain": 0.35,
            "wind": 0.20,
            "humidity": 0.15
        },

        "rules": {
            "ideal_temperature": (10, 25),
            "max_wind": 25,
            "max_rain_probability": 25,
            "ideal_humidity": (30, 80)
        },

        "minimum_score": 70,
        "allowed_hours": (6, 18)
    }
}
