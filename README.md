# GPT_scraper
this repo is a collection of chatgpt scripts. You don't have to use any API_KEY! so it's a great way to save credits and still use the power of chat-gpt programmatically. there are 3 main tools for now:

1) Backend API Scraper (dont need API_KEY just headers from your current session)
2) Selenium Scraper
3) Store a new conversation


## Requirements
- Python 3.x (https://www.python.org/downloads/)
- Postman or insomnia (https://www.postman.com/downloads/) or  (https://insomnia.rest/download)
- Google Chrome (version 111 or later)
- ChromeDriver (https://chromedriver.chromium.org/downloads)
- requests==2.25.1
- selenium==4.8.3
- beautifulsoup4==4.12.0
- pandas==1.5.3
- python-dotenv==1.0.0

To install the required Python packages, run:

pip install -r requirements.txt

For ChromeDriver, download the appropriate version for your system from the [official website](https://chromedriver.chromium.org/downloads), extract it on some folder and finally move the executable file to the `C:/` folder.

## Usage
1. First, log in to Chat GPT using your main Google Chrome application.

choose one tool to test:
# I) Scrape with backend api
2. with your chat gpt opened in a chrome tab press CTRL+SHIFT+I to inspect the page
3. go to "Network" and filter by "Fetch/XHR" and then refresh the page (or F5). click one of the previous conversations
4. look for conversations?offset=0&limit=20 and for something like "e1dbb0b1-2567-48cd-b2c0-0bcda815d7yd"
    (this are the 2 backend hidden apis headers that we will use)
5. secondary click on each and copy as cURL (bash)

6.1. if you use postman, create a collection and click on "import", select "Raw text" and paste the cURL (bash) from conversations?offset=0&limit=20, click "send", you should have a "200" response , then do the same for the other endpoint (the one that looks similiar to this "e1dbb0b1-2567-48cd-b2c0-0bcda815d7yd")

6.2  if you use insomnia, create a new request and paste to the request  (bash) from conversations?offset=0&limit=20 , , click "send", you should have a "200" response (then do the same for the other (the one that looks similiar to this "e1dbb0b1-2567-48cd-b2c0-0bcda815d7yd")

*note*: with this endpoint-> "conversations?offset=0&limit=20" we get each conversation_id, creation_time and title
        with this endpoint-> "e1dbb0b1-2567-48cd-b2c0-0bcda815d7yd" we get the actual conversation (then we iterate by conversation id)

7. In the program (postman or insomnia) hit the "code" button, the one that looks like </>
8. Choose "python - requests" as lenguage and from each request copy the "headers" dictionary
9. Change the name of the "headers" file to "headers.py" and paste the corresponding headers

ids_header = { copy here the "conversations?offset=0&limit=20" headers from the code provided by postman/insomnia}
conversation_header = {copy here the "e1dbb0b1-2567-48cd-b2c0-0bcda815d7yd" headers from the code provided by postman/insomnia}

10. Run the `api_scraper.py` script in your terminal (cd to the desired folder or open the project on your code editor):

python api_scraper.py

11. Wait for the program to finish. In order to dont get blocked for too many request i put a random time limit (2~5 secs) between each conversation fetch.
12. Look for the results (json or csv) in the "outputs" folder
13. If you want to do it again later in time, you will have to do the process of obtaining the headers again


# II) Scrape with selenium
1. Close chrome ( This script relies on the user's browsing history, so it will not work if you have another instance of Chrome open)
2. Run the `scraper.py` script in your terminal (cd to the desired folder or open the project on your code editor):

python scraper.py

3. Look for the results (json or csv) in the "outputs" folder

# III) conversations.py
1. Close chrome ( This script relies on the user's browsing history, so it will not work if you have another instance of Chrome open)

2. Run the `conversations.py` script in your terminal (cd to the desired folder or open the project on your code editor):

python scraper.py

3. Interact with chat gpt prompting your questions

4. Close the conversation with one of this options ['exit', 'quit','bye','goodbye','adios','hasta luego','hasta la vista','chao','chau','nos vemos','nos vemos luego','nos vemos pronto','nos vemos luego','nos vemos','until next time','talk to you later','see you soon','take care']

5. Look for your results on the project folder in the json file created with the date of the conversation in this format "%Y-%m-%d_%H-%M-%S" for example : 
  conversation_2023-03-13_12-33-05.json
