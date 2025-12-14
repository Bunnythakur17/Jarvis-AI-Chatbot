from groq import Groq # importing the Groq library to use its API
import os
from json import load, dump, JSONDecodeError # importiin g funtions to read and write JSON files
import datetime # importing the datetime module for real time date and time information
from dotenv import dotenv_values # importing dotenv_values to read environment variables from a .env file


# load envirnment variable from the .env files
env_vars = dotenv_values(".env")


# retrieve specific envirnment variable for username , assistant name, and API key

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")


# initialize the Groq client using the provided API key
client = Groq(api_key = GroqAPIKey)

# initialize an empty list to store chat messages
messages = []

# define a system messages that provides context to the AI chatbot about its role and behavior 
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, give response in detailed, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# a list of system instruction for the chatbot 
SystemChatBot = [
    {"role" : "system", "content" : System}
]


# attempt to load the chat log from a JSON file 
chatlog_path = r"Data\ChatLog.json"

# Ensure the file exists and is not empty
if not os.path.exists(chatlog_path) or os.path.getsize(chatlog_path) == 0:
    with open(chatlog_path, "w") as f:
        dump([], f, indent=4)

# Now safely load the chat log
try:
    with open(chatlog_path, "r") as f:
        messages = load(f)
except JSONDecodeError:
    # Reset file if it's corrupted
    messages = []
    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)


# function to get real time date and time info
def RealtimeInformation ():
    current_date_time = datetime.datetime.now() # get current date and time
    day = current_date_time.strftime("%A")  # day of the week
    date = current_date_time.strftime("%d") # day of the month
    month = current_date_time.strftime("%B") # full month name
    year = current_date_time.strftime("%Y") # year
    hour = current_date_time.strftime("%H") # hour in 24 hour formate
    minute = current_date_time.strftime("%M") # minute
    second = current_date_time.strftime("%S") # second
    
    # formate the informstion into string 
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds \n" 
    return data

# funtion to modify the chatbot's response for better formstting 
def AnswerModifier(Answer):
    lines = Answer.split('\n') # split the response into lines
    non_empty_lines = [line for line in lines if line.split()]  # remove empty lines
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer 

# main chatbot function to handle user
def ChatBot(Query):
    """ this function sends the user's query to the chatbot and returns the AI's response"""
    
    try:
        # load the existing chat log from the JSON file
        with open(r"Data\ChatLog.json", "t") as f:
            messages = load(f)
            
        # append the user's query to the messsage list 
        messages.append({"role": "user", "content": f"{Query}"})
        
        # make a request to the Groq API for a response 
        completion = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",   # specify the AI model to use
            messages = SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,  # include system instruction, real-time info, and chat history
            max_tokens = 1024,   # limit the maximum token in the response
            temperature = 0.7,   # adjust response randomness (higher means more random)
            top_p = 1,   # use nucleus sampling to control diversity
            stream = True,  # enable streaming response
            stop = None # allow the model to determine when to stop
        )
        
        Answer = ""  # initize an empty string to store the API response
        
        # process the streamed response chunks 
        for chunk in completion:
            if chunk.choices[0].delta.content:    # check if there is content in the current chunk 
                Answer += chunk.choices[0].delta.content   # append the content to the answer
                
                
        Answer = Answer.replace("</s>", "")   # clean up any  unwanted tocken from the response
        
        # append the chatbot response to the messages list
        messages.append({"role": "assistant", "content": Answer})
        
        # save the updated chat log to the JSON file
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
            
        # return the fromatted response
        return AnswerModifier(Answer=Answer)
    except Exception as e:
        # handle error by printing the exception and resetting the chat log 
        print(f"Error: {e}")
        with open (r"Data\ChatLog.json", "w") as f:
            dump([], f, indent = 4)
        return ChatBot(Query)    # retry the query after resetting the log
    
# main program entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question >>> ")  # prompt the user for a question
        print("Response >>> ", ChatBot(user_input))   # call the chatBot funtion and print its response
    
    

























