import sys
from pathlib import Path

# let's add the git submodule to our Python path
# Note: `Path(__file__).resolve().parent` is equivalent to
# `os.path.dirname(os.path.abspath(__file__))`
sys.path.append(str(Path(__file__).resolve().parent / 'calendar-telegram'))

import telegramcalendar as telegram_calendar
