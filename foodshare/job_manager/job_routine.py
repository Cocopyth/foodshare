from foodshare.job_manager.meal_manager import handle_meals
from time import sleep
while True:
    while not handle_meals():
        pass
    sleep(30)