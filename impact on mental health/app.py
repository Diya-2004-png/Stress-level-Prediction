from __future__ import annotations

import math
import os
import webbrowser
from threading import Timer
from typing import Any

from flask import Flask, jsonify, redirect, render_template, request, url_for


# =========================================================
# Flask application
# =========================================================

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024


# =========================================================
# Required input fields
# =========================================================

REQUIRED_FIELDS = [
    "Age",
    "Gender",
    "Country",
    "Academic_Level",
    "Most_Used_Platform",
    "Purpose_Of_Use",
    "Avg_Daily_Usage_Hours",
    "Daily_Unlocks",
    "Study_Hours",
    "Physical_Activity_Hours",
    "Sleep_Hours_Per_Night",
    "Mental_Health_Score",
]


NUMERIC_FIELDS = {
    "Age": {
        "minimum": 18,
        "maximum": 60,
        "integer": True,
    },
    "Avg_Daily_Usage_Hours": {
        "minimum": 0,
        "maximum": 24,
        "integer": False,
    },
    "Daily_Unlocks": {
        "minimum": 0,
        "maximum": 1000,
        "integer": True,
    },
    "Study_Hours": {
        "minimum": 0,
        "maximum": 24,
        "integer": False,
    },
    "Physical_Activity_Hours": {
        "minimum": 0,
        "maximum": 24,
        "integer": False,
    },
    "Sleep_Hours_Per_Night": {
        "minimum": 0,
        "maximum": 24,
        "integer": False,
    },
    "Mental_Health_Score": {
        "minimum": 1,
        "maximum": 10,
        "integer": False,
    },
}


STRESS_DETAILS = {
    "Low": {
        "tone": "positive",
        "summary": (
            "Your entered routine indicates a comparatively "
            "low stress pattern."
        ),
        "recommendations": [
            "Continue maintaining a consistent sleep schedule.",
            "Keep social-media usage intentional and balanced.",
            "Continue regular study breaks and physical activity.",
        ],
    },
    "Medium": {
        "tone": "caution",
        "summary": (
            "Some of your daily habits indicate a moderate "
            "stress pattern."
        ),
        "recommendations": [
            "Reduce unnecessary social-media usage.",
            "Take regular breaks during long study sessions.",
            "Maintain a consistent sleep and exercise routine.",
        ],
    },
    "High": {
        "tone": "warning",
        "summary": (
            "Several entered factors are associated with a "
            "high stress pattern."
        ),
        "recommendations": [
            "Reduce excessive phone checking and screen usage.",
            "Aim for at least seven hours of sleep each night.",
            "Increase daily physical activity and offline time.",
            "Speak with someone you trust if stress continues.",
        ],
    },
    "Very High": {
        "tone": "critical",
        "summary": (
            "Multiple entered factors indicate a very high "
            "stress pattern that may require attention."
        ),
        "recommendations": [
            "Reduce excessive and late-night phone usage.",
            "Prioritise adequate sleep and physical activity.",
            "Take regular breaks from social media.",
            "Consider speaking with a qualified counsellor.",
        ],
    },
}


# =========================================================
# Utility functions
# =========================================================

def clean_text(value: Any) -> str:
    return " ".join(str(value).strip().split())


def get_request_data() -> dict[str, Any]:
    """
    Accept JSON, HTML form data or URL query parameters.
    """

    if request.is_json:
        data = request.get_json(silent=True)

        if isinstance(data, dict):
            return data

        return {}

    if request.form:
        return request.form.to_dict()

    if request.args:
        return request.args.to_dict()

    return {}


def validate_input(
    payload: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str], list[str]]:

    cleaned: dict[str, Any] = {}
    errors: dict[str, str] = {}
    warnings: list[str] = []

    for field in REQUIRED_FIELDS:
        value = payload.get(field)

        if value is None or str(value).strip() == "":
            errors[field] = "This field is required."
            continue

        if field in NUMERIC_FIELDS:
            settings = NUMERIC_FIELDS[field]

            try:
                number = float(value)

            except (TypeError, ValueError):
                errors[field] = "Enter a valid number."
                continue

            minimum = settings["minimum"]
            maximum = settings["maximum"]

            if number < minimum or number > maximum:
                errors[field] = (
                    f"Value must be between "
                    f"{minimum} and {maximum}."
                )
                continue

            if settings["integer"]:
                cleaned[field] = int(number)
            else:
                cleaned[field] = round(number, 2)

        else:
            text = clean_text(value)

            if len(text) > 100:
                errors[field] = (
                    "Use 100 characters or fewer."
                )
                continue

            cleaned[field] = text

    if errors:
        return cleaned, errors, warnings

    if cleaned["Age"] > 30:
        warnings.append(
            "Age is outside the main student-age range. "
            "Interpret the result cautiously."
        )

    if cleaned["Avg_Daily_Usage_Hours"] > 12:
        warnings.append(
            "The entered daily social-media usage is unusually high."
        )

    if cleaned["Daily_Unlocks"] > 300:
        warnings.append(
            "The entered daily phone-unlock count is unusually high."
        )

    return cleaned, errors, warnings


def calculate_risk_score(
    data: dict[str, Any],
) -> float:

    risk_score = 0.0

    usage = data["Avg_Daily_Usage_Hours"]

    if usage >= 10:
        risk_score += 25
    elif usage >= 8:
        risk_score += 22
    elif usage >= 6:
        risk_score += 17
    elif usage >= 4:
        risk_score += 11
    elif usage >= 2:
        risk_score += 5

    unlocks = data["Daily_Unlocks"]

    if unlocks >= 300:
        risk_score += 15
    elif unlocks >= 220:
        risk_score += 13
    elif unlocks >= 150:
        risk_score += 10
    elif unlocks >= 80:
        risk_score += 6
    else:
        risk_score += 2

    sleep = data["Sleep_Hours_Per_Night"]

    if sleep < 4:
        risk_score += 20
    elif sleep < 5:
        risk_score += 18
    elif sleep < 6:
        risk_score += 15
    elif sleep < 7:
        risk_score += 10
    elif sleep < 8:
        risk_score += 4

    mental_health = data["Mental_Health_Score"]

    if mental_health <= 2:
        risk_score += 20
    elif mental_health <= 4:
        risk_score += 17
    elif mental_health <= 6:
        risk_score += 11
    elif mental_health <= 8:
        risk_score += 5

    activity = data["Physical_Activity_Hours"]

    if activity < 0.5:
        risk_score += 10
    elif activity < 1:
        risk_score += 8
    elif activity < 2:
        risk_score += 4

    study = data["Study_Hours"]

    if study >= 12:
        risk_score += 10
    elif study >= 10:
        risk_score += 8
    elif study >= 8:
        risk_score += 5
    elif study >= 6:
        risk_score += 2

    purpose = data["Purpose_Of_Use"].lower()

    if purpose == "entertainment":
        risk_score += 3

    platform = data["Most_Used_Platform"].lower()

    high_engagement_platforms = {
        "instagram",
        "tiktok",
        "snapchat",
    }

    if platform in high_engagement_platforms:
        risk_score += 2

    return round(
        min(max(risk_score, 0), 100),
        2,
    )


def get_prediction_from_score(
    risk_score: float,
) -> str:

    if risk_score < 25:
        return "Low"

    if risk_score < 50:
        return "Medium"

    if risk_score < 75:
        return "High"

    return "Very High"


def calculate_probabilities(
    risk_score: float,
) -> dict[str, float]:

    class_centres = {
        "Low": 12.5,
        "Medium": 37.5,
        "High": 62.5,
        "Very High": 87.5,
    }

    standard_deviation = 18.0

    raw_probabilities = {}

    for label, centre in class_centres.items():
        distance = risk_score - centre

        raw_probabilities[label] = math.exp(
            -(
                distance ** 2
            )
            / (
                2 * standard_deviation ** 2
            )
        )

    total = sum(raw_probabilities.values())

    return {
        label: round(
            value / total * 100,
            2,
        )
        for label, value in raw_probabilities.items()
    }


def get_observed_factors(
    data: dict[str, Any],
) -> list[dict[str, str]]:

    factors: list[dict[str, str]] = []

    usage = data["Avg_Daily_Usage_Hours"]

    if usage >= 7:
        usage_impact = "High"
    elif usage >= 4:
        usage_impact = "Moderate"
    else:
        usage_impact = "Lower"

    factors.append(
        {
            "label": "Daily social-media usage",
            "value": f"{usage:g} hours",
            "impact": usage_impact,
        }
    )

    unlocks = data["Daily_Unlocks"]

    if unlocks >= 200:
        unlock_impact = "High"
    elif unlocks >= 100:
        unlock_impact = "Moderate"
    else:
        unlock_impact = "Lower"

    factors.append(
        {
            "label": "Daily phone unlocks",
            "value": f"{unlocks} times",
            "impact": unlock_impact,
        }
    )

    sleep = data["Sleep_Hours_Per_Night"]

    if sleep < 6:
        sleep_impact = "High"
    elif sleep < 7:
        sleep_impact = "Moderate"
    else:
        sleep_impact = "Protective"

    factors.append(
        {
            "label": "Sleep duration",
            "value": f"{sleep:g} hours",
            "impact": sleep_impact,
        }
    )

    mental_health = data["Mental_Health_Score"]

    if mental_health <= 4:
        mental_impact = "High"
    elif mental_health <= 6:
        mental_impact = "Moderate"
    else:
        mental_impact = "Protective"

    factors.append(
        {
            "label": "Mental health score",
            "value": f"{mental_health:g}/10",
            "impact": mental_impact,
        }
    )

    activity = data["Physical_Activity_Hours"]

    if activity < 1:
        activity_impact = "High"
    elif activity < 2:
        activity_impact = "Moderate"
    else:
        activity_impact = "Protective"

    factors.append(
        {
            "label": "Physical activity",
            "value": f"{activity:g} hours",
            "impact": activity_impact,
        }
    )

    study = data["Study_Hours"]

    if study >= 10:
        study_impact = "High"
    elif study >= 7:
        study_impact = "Moderate"
    else:
        study_impact = "Lower"

    factors.append(
        {
            "label": "Study duration",
            "value": f"{study:g} hours",
            "impact": study_impact,
        }
    )

    return factors


def generate_prediction_response(
    payload: dict[str, Any],
):

    cleaned_data, errors, warnings = validate_input(
        payload
    )

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "fields": errors,
            }
        ), 422

    risk_score = calculate_risk_score(
        cleaned_data
    )

    prediction = get_prediction_from_score(
        risk_score
    )

    probabilities = calculate_probabilities(
        risk_score
    )

    confidence = probabilities[prediction]

    details = STRESS_DETAILS[prediction]

    return jsonify(
        {
            "prediction": prediction,
            "confidence": confidence,
            "risk_score": risk_score,
            "probabilities": probabilities,
            "summary": details["summary"],
            "tone": details["tone"],
            "observed_factors": get_observed_factors(
                cleaned_data
            ),
            "recommendations": details[
                "recommendations"
            ],
            "warnings": warnings,
            "model": {
                "name": "Student Stress Predictor",
                "mode": "self-contained-demo",
                "version": "1.0.0",
            },
            "disclaimer": (
                "This result is an educational prediction "
                "and is not a medical diagnosis."
            ),
        }
    )


# =========================================================
# Website routes
# =========================================================

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        model_mode="AI Demo",
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET" and not request.args:
        return redirect(
            url_for("index")
        )

    payload = get_request_data()

    return generate_prediction_response(
        payload
    )


@app.route("/api/predict", methods=["GET", "POST"])
def api_predict():
    if request.method == "GET" and not request.args:
        return jsonify(
            {
                "message": (
                    "Send a POST request containing the "
                    "12 required prediction fields."
                ),
                "required_fields": REQUIRED_FIELDS,
            }
        )

    payload = get_request_data()

    return generate_prediction_response(
        payload
    )


@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify(
        {
            "status": "ok",
            "service": "student-stress-predictor",
            "prediction_endpoint": "/api/predict",
            "alternative_endpoint": "/predict",
            "version": "1.0.0",
        }
    )


@app.route("/api/model-info", methods=["GET"])
def api_model_info():
    return jsonify(
        {
            "name": "Student Stress Predictor",
            "mode": "self-contained-demo",
            "version": "1.0.0",
            "required_fields": REQUIRED_FIELDS,
        }
    )


# =========================================================
# Error handlers
# =========================================================

@app.errorhandler(404)
def page_not_found(_error):
    if request.path.startswith("/api/"):
        return jsonify(
            {
                "error": "API endpoint not found.",
                "prediction_endpoint": "/api/predict",
            }
        ), 404

    return redirect(
        url_for("index")
    )


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify(
        {
            "error": "Method not allowed.",
            "message": (
                "Use POST for prediction requests."
            ),
        }
    ), 405


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(
        {
            "error": "Request body is too large."
        }
    ), 413


@app.errorhandler(Exception)
def unexpected_error(error):
    app.logger.exception(
        "Unexpected error: %s",
        error,
    )

    return jsonify(
        {
            "error": (
                "An unexpected server error occurred."
            )
        }
    ), 500


# =========================================================
# Automatically open browser
# =========================================================

def open_browser(url: str):
    try:
        webbrowser.open_new(url)

    except Exception as error:
        print(
            f"Could not open browser automatically: "
            f"{error}"
        )


# =========================================================
# Run application
# =========================================================

if __name__ == "__main__":

    host = "127.0.0.1"

    port = int(
        os.getenv(
            "PORT",
            "5000",
        )
    )

    application_url = (
        f"http://{host}:{port}"
    )

    print()
    print("=" * 60)
    print("Student Stress Predictor is running")
    print(f"Website: {application_url}")
    print(
        f"Prediction API: "
        f"{application_url}/api/predict"
    )
    print(
        f"Alternative URL: "
        f"{application_url}/predict"
    )
    print("=" * 60)
    print()

    Timer(
        1.5,
        open_browser,
        args=(application_url,),
    ).start()

    app.run(
        host=host,
        port=port,
        debug=False,
        use_reloader=False,
    )