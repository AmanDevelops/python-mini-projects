from flask import Flask, render_template, request

app = Flask(__name__)

CONVERSION_FACTOR_LENGTHS = {
    "millimeter": 0.001,
    "centimeter": 0.01,
    "meter": 1,
    "kilometer": 1000,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
    "mile": 1609.34,
}

CONVERSION_FACTOR_WEIGHTS = {
    "milligram": 0.000001,
    "gram": 0.001,
    "kilogram": 1,
    "ounce": 0.0283495,
    "pound": 0.453592,
}

CONVERSION_FACTOR_TEMPERATURE = {
    "celsius": {"to_celsius": lambda c: c, "from_celsius": lambda c: c},
    "fahrenheit": {
        "to_celsius": lambda f: (f - 32) * 5 / 9,
        "from_celsius": lambda c: c * 9 / 5 + 32,
    },
    "kelvin": {
        "to_celsius": lambda k: k - 273.15,
        "from_celsius": lambda c: c + 273.15,
    },
}


@app.route("/", methods=["GET", "POST"])
def hello_world():

    app_type = request.args.get("app", "length")

    unit_mappings = {
        "length": CONVERSION_FACTOR_LENGTHS,
        "weight": CONVERSION_FACTOR_WEIGHTS,
        "temperature": CONVERSION_FACTOR_TEMPERATURE,
    }

    units = unit_mappings.get(app_type, CONVERSION_FACTOR_LENGTHS)
    result = None

    if request.method == "POST":
        fromValue = float(request.form.get("fromValue"))
        fromUnit = request.form.get("fromUnit")
        toUnit = request.form.get("toUnit")

        if app_type == "temperature":
            celsius_value = units[fromUnit]["to_celsius"](fromValue)
            result = units[toUnit]["from_celsius"](celsius_value)
        else:
            result = fromValue * units[fromUnit] / units[toUnit]

    return render_template("index.html", result=result, units=units)
