import pandas as pd
import time
import json
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

# Set the browser driver
def set_driver(headless=False):
    driver = None
    # get current user
    user = os.getlogin()
    user_profile = r'C://Users//' + user + r'//AppData//Local//Google//Chrome//User Data'
    print(user_profile)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument("--user-data-dir=" + user_profile)
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36')
    driver = webdriver.Chrome(r'C:\chromedriver.exe', options=options)
    return driver

def load_conversations(driver):
    # Navigate to the OpenAI chat page
    driver.get("https://chat.openai.com/chat")
    time.sleep(5)  # Wait for the page to load
    # Click the "Show more" button multiple times to load all the conversations
    while True:
        try:
            show_more_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div/nav/div/div/button/div')
            driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(3)
            # Wait for 3 seconds to load the conversations
        except:
            #quit the loop if the button is not found
            break

def store_convseration(url_id, title, question, answer, data):
    # Find the conversation with the desired ID or title, or create a new conversation if one does not exist
    conversation = None
    for c in data['conversations']:
        if c['id'] == url_id:
            conversation = c
            break
    if conversation is None:
        conversation = {
            'id': url_id,
            'title': title,
            'messages': []
        }
        data['conversations'].append(conversation)
    # Append a new message object for the human's question to the conversation's list of messages
    human_message = {
        'sender': 'human',
        'text': question
    }
    conversation['messages'].append(human_message)

    # Append a new message object for the bot's answer to the conversation's list of messages
    bot_message = {
        'sender': 'bot',
        'text': answer
    }
    conversation['messages'].append(bot_message)

    return data

def scrape_conversations(driver):
    data = {'conversations': []}
    c = 1
    try:
        while True:
            conversation = driver.find_element(By.XPATH,f'//*[@id="__next"]/div[1]/div[2]/div/div/nav/div/div/a[{str(c)}]')
            conversation.click()
            print(f'Index: {c}', print(conversation.text))
            # Click on the element
            # Get the current URL
            current_url = driver.current_url
            # Extract the ID from the URL
            url_id = urlparse(current_url).path.split('/')[-1]
            title =  conversation.text
            time.sleep(2)
            print(f'URL ID: {url_id}', title)
            # Navigate back to the page containing the clickable elements
            # iterate through each element f'//*[@id="__next"]/div[1]/div[2]/div/div/nav/div/div/a[{i}]/div[1]' while its possible
            i=2
            while True:
                try:
                    question = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[1]/div[1]/main/div[1]/div/div/div/div[{str(i)}]/div/div[2]')
                    answer = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[1]/div[1]/main/div[1]/div/div/div/div[{str(i+1)}]/div/div[2]')
                    # store in json. each conversation has an unique id and title and attached to it a list of questions and answer
                    data = store_convseration(url_id, title, question.text, answer.text, data)
                    # the append should be to the list of questions and answers 
                    i+=1
                    time.sleep(0.5)
                    print("ID: ", url_id, "Title: ", title, "Question: ", question.text, "Answer: ", answer.text)
                except Exception as e:
                    if "Unable to locate element:" in str(e):
                        pass
                    else :
                        print(str(e))
                    c+=1
                    break
            driver.back()
            time.sleep(random.randint(6, 10))

    except Exception as e:
        # Close the browser
        driver.quit()
    return data

def save_json(data,date):
    # Create the filename
    filename = f"outputs/API scraped conversations {str(date)}.json"
    # Write a new file and save the JSON file
    with open(filename, "w") as f:
        json.dump(data, f)

def save_csv(data, date):
    json_file = f"outputs/API scraped conversations {str(date)}.json"
    df = pd.read_json(json_file)
    df = pd.DataFrame(df['conversations'].values.tolist())
    filename = f"outputs/API scraped conversations {str(date)}.csv"
    df.to_csv(filename, index=False)

def main():
    driver = set_driver()
    load_conversations(driver)
    data = scrape_conversations(driver)
    # Get the current date and time
    date = time.strftime("%d-%m-%Y %H-%M")
    save_json(data, date)
    save_csv(data, date )
if __name__ == "__main__":
    main()