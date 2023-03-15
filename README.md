# GPT_scraper
This repository provides a way to use ChatGPT through Selenium, which can be helpful for avoiding the usage of API credits while still using ChatGPT programmatically. It also includes features to store your past prompts, filter them, or classify them for future reference

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- Requests
- Google Chrome (version 111 or later)
- ChromeDriver (download from the official website)

To install the required Python packages, run:

pip install beautifulsoup4, selenium


For ChromeDriver, download the appropriate version for your system from the [official website](https://chromedriver.chromium.org/downloads) and move the executable file to the `C:/` folder.

## Usage

1. First, log in to Chat GPT using your main Google Chrome application. This script relies on the user's browsing history, so it will not work if you have another instance of Chrome open.

2. Close chrome

3. Run the `scraper.py` script:

python scraper.py

4. Interact with chat gpt prompting your questions

5. Close the conversation with one of this options ['exit', 'quit','bye','goodbye','adios','hasta luego','hasta la vista','chao','chau','nos vemos','nos vemos luego','nos vemos pronto','nos vemos luego','nos vemos','until next time','talk to you later','see you soon','take care']

6. Look for your results on the project folder in the json file created with the date of the conversation in this format "%Y-%m-%d_%H-%M-%S" for example : 
  conversation_2023-03-13_12-33-05.json