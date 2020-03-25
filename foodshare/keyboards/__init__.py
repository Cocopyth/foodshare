import sys
from importlib import import_module
from pathlib import Path

# let's add the git submodule to our Python path
# Note: `Path(__file__).resolve().parent` is equivalent to
# `os.path.dirname(os.path.abspath(__file__))`
sys.path.append(str(Path(__file__).resolve().parent))

# the following is necessary to import a file name with a dash
# Note: `import_module('foo.bar')` is equivalent to `import foo.bar`
telegram_calendar = import_module('calendar-telegram.telegramcalendar')
