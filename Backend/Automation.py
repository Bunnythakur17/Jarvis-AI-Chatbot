from AppOpener import close, open as appopen    # import function to open and close app
from webbrowser import open as webopen          # import web browser functionality
from pywhatkit import search, playonyt          # import funtion for google search and youtube 
from dotenv import dotenv_values                # import dotenv to manage environment variables
from bs4 import BeautifulSoup                   # import BeautifulSoup for parsing HTML content 
from rich import print                          # import rich for styled console output
from groq import Groq                           # import groq for ai chat funtionalities
import webbrowser                               # import webbrowser for opening URLs
import subprocess                               # import subprocess for interacting with the system
import requests                                 # import requests for making HTTP requests
import keyboard                                  # import keybord for beybord related action
import asyncio                                  # import asyncio for asynchronous programming
import os                                       # import os for oprating system funtionalities

# load environment variable from the .env file
env_vars = dotenv_values(".env") 
GroqAPIKey = env_vars.get("GroqAPIKey")   # retrieve the groq API Key


# define CSS classes for parsing specific element in html content
calsses = ["zCubwf", "hgKEls", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSB YwPhnf", "pclqee", "te-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# define a user-agent for making web requests
useragent = 'Mozilla/5.0 (Widows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896/75 Safari/537.36'

# initialize the groq client with the API key
client = Groq(api_key = GroqAPIKey)

# predefined professional responses for user interactionas
prefessional_responses = [
    "Your satisfation is my top priority; feel free to reach out if there's anything else I can help you with",
    "I'm at your service for any additional question or support you may need-don't hasitate to ask"
]


# list to store chatbot message
messages = []


# system message to provide context to the  chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writter. You have to write content like letter"}]

# funtion to perform a google search 
def GoogleSearh(Topic):
    search(Topic)            # use pywhatkit's searcgh functin to perform a google search 
    return True              # Inducate success

# function to generate content using AI and save it to a file 
def Content(Topic):
    
    # nested Function to open a file in Notepad 
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'     # default text editor 
        subprocess.Popen([default_text_editor, File])   # open the file in Notepad 
        
    # nestef function to generate content using the AI chatbot 
    def ContenWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # add the user's prompt to message
        
        completion = client.chat.completions.create(
            model = 'mixer-8x7b-32768',          # specify the AI model
            messages = SystemChatBot + messages,     # include system instructions and chat history
            max_tokens = 2048,   # limit the maximum tokens in the response
            temperature = 0.7,      # adjust response randomness
            top_p = 1,           # Use nucleus sampling for response diversity
            stream = True,        # enable streaming response
            stop = None       # Allow the model to determine stopping condition
        )
        
        Answer = ""    # initislize an empty string for the response
        
        # process streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:                   # check for content in the current chunk
                Answer += chunk.choices[0].delta.content         # append the content to the answer
                 
        Answer = Answer.replace("</s>", "")               # remove unwanter tokens from the response 
        messages.append({"role": "assistant", "content": Answer})          # add the AI's response to messages
        return Answer
    
    Topic: str = Topic.replace("Content ", "")              # remove "Content " from the topic
    ContentByAI = ContenWriterAI(Topic)                 # generate content using AI
    
    # save the genersted content to a text file
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding = "utf-8") as file:
        file.write(ContentByAI)         # Write the content to the file
        file.close()
    
    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")    # open the file in notepad
    return True    # indicate success

# function to search for a topic on youtube 
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"   # Construct the youtube search url
    webbrowser.open(Url4Search)
    return True   # indicate success

# funtion to play a video on youtube 
def PlayYoutube(query):
    playonyt(query)         # use pywhatkit's playonyt funtion to play the video 
    return True      # indicate success

# function to open an application or a relevent webpage 
def OpenApp(app, sess=requests.session()):
    
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)    # Attempt to open the app
        return True     # indicate success 
    
    except:
        # nested function to extract links from HTML content 
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')     # parse the HTML content
            links = soup.find_all('a', {'jsname': 'UWckNb'})     # find relevant
        
        # nested funtion to perform a google search and retrive HTML
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"     # construct the google search url
            headers = {"User-Agent": useragent}                # use the predefined user-agent
            response = sess.get(url, headers=headers)          # perform the GET request 
            
            if response.status_code == 200:
                return response.text
            else:
                print("failed to retrieve search results.")    # print an error 
            return None
        
        html = search_google(app)    # perform the google search 
        
        if html:
            link = extract_links(html)[0]       # extract the first link from the search results
            webopen(link)          # open the link in a web browser
            
        return True          # indicate success
    
# funtion to close an application
def CloseApp(app):
    
    if "Chrome" in app:
        pass      # skip if the app is chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # attempt to close the app
            return True
        except:
            return True       # indicate failure
        
# function to execute system-level command
def System(command):
    
    # nested function to mute the volume 
    def mute():
        keyboard.press_and_release("volume mute")   # simulate the mute key press
    
    # nested function to unmute the system volume
    def unmute():
         keyboard.press_and_release("volume mute")   # simulate the unmute key press

    # nested function to unmute the system volume
    def volume_up():
         keyboard.press_and_release("volume up")   # simulate the volume up key press
    
    # nested function to unmute the system volume
    def volume_down():
         keyboard.press_and_release("volume down")   # simulate the volume down key press
        
    # execute the appropriate command 
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
        
    return True    # indicate success












