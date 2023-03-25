import pandas as pd
import json

import random
import requests
from time import sleep, strftime

from headers import ids_header, conversation_header

def get_response(url, headers, payload):
    response = requests.request("GET", url, headers=headers, data=payload)
    return response
# get ids
def get_ids():
    payload={}
    headers = ids_header
    data = {}
    ids, create_time, titles = [], [], []
    # iterate through offset and limit to get all conversations
    i, offset, total_iterations = 0, 0, 0
    while True:
        try:
            url = f"https://chat.openai.com/backend-api/conversations?offset={str(offset)}&limit=100"
            response = get_response(url, headers, payload)
            data = json.loads(response.text)

            print(len(data['items']))
            for item in data['items']:
                
                ids.append(item['id'])
                create_time.append(item['create_time'])
                titles.append(item['title'])
            if i == 0:
                total_chats = data['total']
                #divide by 100 to get the number of iterations 
                total_iterations = total_chats/100
                if total_iterations/100 % 1 != 0:
                    total_iterations = int(total_iterations) +1
                offset = offset + 101
                i+=1
            else :
                offset = offset + 100
                i+=1
            if i == total_iterations:
                break
        except Exception as e:
            print(str(e))
            print('done')
            break
    #save data id by id with a comprehension (considering created_time list also)
    data = {'conversations': [{'id': id, 'title': title, 'create_time': create_time, 'messages': []} for id, title, create_time in zip(ids, titles, create_time)]}
    return data, ids

def get_conversations(data, ids):
    # get conversation
    payload={}
    headers = conversation_header

    for i, id in enumerate(ids):
        print(id)
        url = f"https://chat.openai.com/backend-api/conversation/{id}"
        response = get_response(url, headers, payload)
        response_json = json.loads(response.text)

        for message_id, message_data in response_json["mapping"].items():
            if "message" in message_data:
                role = message_data["message"]["author"]["role"]
                # Check if the role is "user" or "assistant"
                    
                    # conversation["messages"].append(message_data["message"]["content"]["parts"])
                if role == "user":
                    # Append a new message object for the human's question to the conversation's list of messages
                    human_message = {
                        'sender': 'human',
                        'text': message_data["message"]["content"]["parts"]
                    }
                    data['conversations'][i]['messages'].append(human_message)
                    # append the message to the conversation
                elif role == "assistant":
                    # Append a new message object for the bot's answer to the conversation's list of messages
                    bot_message = {
                        'sender': 'bot',
                        'text': message_data["message"]["content"]["parts"]
                    } 
                    data['conversations'][i]['messages'].append(bot_message)
        sleep(random.randint(2, 5))
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
    data, ids = get_ids()
    data = get_conversations(data, ids)
    # Get the current date and time
    date = strftime("%d-%m-%Y %H-%M")
    save_json(data, date)
    save_csv(data, date )

if __name__ == "__main__":
    main()