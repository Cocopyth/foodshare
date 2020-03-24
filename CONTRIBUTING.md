# How to contribute
## Getting started
[![Python version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/release/python-370/)

The project was written using **Python 3.7+** and uses [**Poetry**](https://python-poetry.org/) as a dependency manager.

:open_file_folder: **Clone the repository**  
Clone the repository and dive into it:
```shell
git clone --recurse-submodules https://github.com/Cocopyth/foodshare.git
cd foodshare
```
*The `--recurse-submodules` parameter is necessary because this repository uses [Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).*

:four_leaf_clover: **Install poetry**  
[**Poetry**](https://python-poetry.org/) is a dependency management tool that we use thorouglhy throughout our development process. You can install Poetry isolated from the rest of your system (recommended way) by following the instructions [here](https://python-poetry.org/docs/#installation).

:books: **Install the project dependencies**  
Many libraries are used by the project and for development (a complete list of dependencies can be found in [`pyproject.toml`](pyproject.toml)). Run the following from within the project folder to install all the dependencies:
```shell
poetry install
```

## Write some code
This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.

:point_up: A few notes:
- We recommend to set your IDE line length ruler to 79 characters.
- Please use `'` rather than `"` for strings:
  ```diff
  - message = "Hello world!"
  + message = 'Hello world!'
  ```
- Please use no capital letter or point in short inline comments:
  ```diff
  - # Let's add the git submodule to our Python path.
  + # let's add the git submodule to our Python path
  ```

After you wrote some code please use the `check_commit.py` script to clean your code:
```shell
# get help on the check_commit.py script
poetry run python check_commit.py -h

# run the check_commit.py script on the main Python package
poetry run python check_commit.py foodshare
```

## Run the bot
In order to run and test the bot on your local computer you need to:
- [ ] :envelope: Create a Telegram account.
- [ ] :robot: Use the [Telegram Bots API documentation](https://core.telegram.org) to get a bot token from `BotFather`.
- [ ] :wrench: Set the `TELEGRAM_BOT_TOKEN` environment variable:
  ```shell 
  export TELEGRAM_BOT_TOKEN=1786460108:AJHFkCrvGb7LRjy3loPn3dWT2VL-c8Ttwjk
  ```
- [ ] :rocket: Run the bot using the `run_bot.py` script:
  ```shell
  poetry run python run_bot.py
  ```
- [ ] :tada: Your bot is now up and running and ready to discuss with you!
