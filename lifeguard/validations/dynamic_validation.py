"""
Dynamic validations
"""
from datetime import datetime
import requests

from lifeguard import NORMAL, PROBLEM, change_status
from lifeguard.actions.database import save_result_into_database
from lifeguard.logger import lifeguard_logger as logger
from lifeguard.validations import ValidationResponse, validation

from lifeguard_mongodb.repositories import DATABASE

validation_params = {}

urls = [
    {"description": "my site", "url": "https://diegorubin.dev"},
    {"description": "pudim", "url": "http://pudim.com.br"},
]


def append_to_history(validation_result, _settings):
    history = DATABASE.history
    history.insert_one(
        {
            "validation_name": validation_result.validation_name,
            "status": validation_result.status,
            "details": validation_result.details,
            "created_at": datetime.utcnow(),
        }
    )


def validate_url(url, description):
    def dynamic_validation():
        status = NORMAL
        result = requests.get(url)
        logger.info("pudim status code: %s", result.status_code)

        if result.status_code != 200:
            status = change_status(status, PROBLEM)

        return ValidationResponse(
            description,
            NORMAL,
            {status: result.status_code},
            {"notification": {"notify": True}},
        )

    return dynamic_validation


for url in urls:
    validation_function = validate_url(url["url"], url["description"])
    validation_function.__name__ = url["description"].replace(" ", "_")
    validation(
        description=url["description"],
        actions=[save_result_into_database, append_to_history],
        schedule={"every": {"minutes": 1}},
        settings=None,
    )(validation_function)
