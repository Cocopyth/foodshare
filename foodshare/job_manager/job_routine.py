from foodshare.job_manager.meal_manager import handle_meals
from time import sleep

def main():
    while True:
        while not handle_meals():
            pass
        sleep(30)

if __name__ == '__main__':
    main()
