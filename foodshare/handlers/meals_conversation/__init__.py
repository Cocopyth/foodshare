from datetime import datetime
from enum import Enum, auto

from foodshare.utils import datetime_format


class ConversationStage(Enum):
    CHOSING_MEAL = auto()
    CANCELING = auto()


def get_all_meals(user):
    meals_as_cook = [
        meal_job.meal
        for meal_job in user.message_giver
            if (not meal_job.job_done and not meal_job.meal.cancelled
                and not meal_job.meal.is_done)
    ]
    meals_as_cook = list(dict.fromkeys(meals_as_cook))
    meals_as_participant = [
        meal_job.meal
        for meal_job in user.message_receiver
        if (meal_job.answer and not meal_job.job_done
            and not meal_job.meal.cancelled
                and not meal_job.meal.is_done)
    ]
    meals_as_participant = list(dict.fromkeys(meals_as_participant))
    # initialize some variables in `context.user_data` when the keyboard is
    # first called
    all_meals = meals_as_cook + meals_as_participant
    all_meals.sort(
        key=lambda meal: datetime.strptime(meal.when, datetime_format)
    )
    return all_meals, meals_as_cook
