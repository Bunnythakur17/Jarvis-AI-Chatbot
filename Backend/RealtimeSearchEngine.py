from googlesearch import search
from groq import Groq # importing the Groq library to use its API
import os
from json import load, dump, JSONDecodeError # importiin g funtions to read and write JSON files
import datetime # importing the datetime module for real time date and time information
from dotenv import dotenv_values # importing dotenv_values to read environment variables from a .env file


# load envirnment variable from the .env files
env_vars = dotenv_values(".env")

# Retrieve envirnment variable for the chatbot configuration 
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# initialize the groq client with the provided API key
client = Groq(api_key = GroqAPIKey)

# define the system instruction for the chatbot 

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# try to load the caht log from a JSON file , or creat an emptu one if it doesn't exist 
try:
    with open (r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)


# Function to perform a google search and format the resultd
def GoogleSearch(query):
    results = list(search(query, advanced = True, num_results = 5 ))
    Answer = f"The search result for '{query}' are:\n[start]\n"
    
    for i in results :
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
        
    Answer += "[end]"
    return Answer

# funtion to cleanup the answer by removing empty lines
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.split()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# predefine chatbot conversation system message and an initial user message
SystemChatBot = [
    {"role": "system", "content": System}, 
    {"role": "user", "content": "Hi"}, 
    {"role": "assistant", "content": "Hello, How can I help you?"}   
]

# funtion to get real-time information like the current date and time
def Information():
    data = ""
    current_date_time = datetime.datetime.now() # get current date and time
    day = current_date_time.strftime("%A")  # day of the week
    date = current_date_time.strftime("%d") # day of the month
    month = current_date_time.strftime("%B") # full month name
    year = current_date_time.strftime("%Y") # year
    hour = current_date_time.strftime("%H") # hour in 24 hour formate
    minute = current_date_time.strftime("%M") # minute
    second = current_date_time.strftime("%S") # second
    data += f"Use this Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes,{second} seconds. \n"
    return data

# funtion to handle real-time search and response generation 
def RealtimeSearchEngin(prompt):
    global SystemChatbot, messages
    
    # load the chat log from JSON file 
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load (f)
    messages.append({"role": "user", "content": f"{prompt}"})
    
    # add Google search result to the system chatbot message
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})
    
    # generate a response using the groq client
    completion = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature = 0.7,
        max_tokens = 2048,
        top_p = 1,
        stream = True,
        stop = None
    )
    
    Answer = ""
    
    # concatenate response chunks from the stream output
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # clean up the response
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    
    # save the updated chat log back to JSON file
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
        
    # remove the most recent system message from the chatBot conversation
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# main program entry point
if __name__ == "__main__":
    while True:
        prompt = input("Enter your Question >>> ")  # prompt the user for a question
        print("\nResponse >>> ", RealtimeSearchEngin(prompt))   # call the chatBot funtion and print its response
    
        

































