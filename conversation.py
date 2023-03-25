from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from time import sleep
from dotenv import load_dotenv
import os
import bs4
import requests
import json
import random


# Set the browser driver
def set_driver(headless=False):
    # read current user name
    user_name = os.getlogin()
    # set user profile path
    user_profile = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data'.format(user_name)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument("--user-data-dir=" + user_profile)

    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36')

    driver = webdriver.Chrome(r'C:\chromedriver.exe', options=options)
    return driver


# Send the user's input to the chatbot
def send_input(driver, question):
    for char in question:
        driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div[2]/textarea').send_keys(char)
        sleep(random.uniform(0.01, 0.03))
    sleep(3)
    driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div[2]/button').click()
    sleep(15)


# Receive the chatbot's response and print it to the console
def get_response(driver):
    answer = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/main/div[1]/div/div/div/div[3]/div/div[2]')
    return answer.text

# Save the conversation to a JSON file
def save_conversation(conversation):
    #save with the date and time on the file name
    with open('conversation_{}.json'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), 'w') as f:
        json.dump(conversation, f, indent=4)




# Start the conversation loop
def start_conversation():
    driver = set_driver()
    driver.get('https://chat.openai.com/chat')
    sleep(4)

    conversation = []

    while True:
        question = input("You: ")
        if question.lower() in ['exit', 'quit','bye','goodbye','adios','hasta luego','hasta la vista','chao','chau','nos vemos','nos vemos luego','nos vemos pronto','nos vemos luego','nos vemos','until next time','talk to you later','see you soon','take care']:
            break
        send_input(driver, question)
        answer = get_response(driver)
        print(f"Bot: {answer}")
        conversation.append({'question': question, 'answer': answer})

    save_conversation(conversation)
    driver.quit()


if __name__ == '__main__':
    start_conversation()