from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os 
import mtranslate as mt 
import time



# load envirment variable from the .env file
env_vars = dotenv_values(".env")

# get the input language setting from the environment variable 
InputLanguage = env_vars.get("InputLanguage")

# define the HTML code for the speech recognition interface 
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">    <!-- Bootstrap CSS (from CDN) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Your custom CSS (style.css) -->
    <link rel="stylesheet" href="style.css">
    <title>Speech Recognition</title>
</head>

<body>
    <div class="container text-center">
       <h1 class="text-primary">Hello with Bootstrap</h1>
       <p class="custom-text">This is styled by style.css</p>
    </div>
    <div class="container text-center">
    <button id="start" type="button" onclick="startRecognition()">Start Recognition</button>
    <button id="end" type="button" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    </div>



<script src="script.js"></script>

</body>
</html>'''

# replace the language setting in the HTML code with the inoput language  from the envirnmet variables
# HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}")
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# write the modified HTMl code to a file 
with open (r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# get the current woprking directory 
current_dir = os.getcwd()
# generate the file path for the html file
link = f"{current_dir}/Data/Voice.html"

# set chrome option for the webdriver
# chrome_options = Options()
# user_agent = "Mozilla/5.0 ( Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36 (KHTML, link Gecko) Chrome/89.0/142/86 Safari/537/36"
# chrome_options.add_argument(f"user-agent={user_agent}")
# chrome_options.add_argument("--use-fake-ui-for-media-stream")
# chrome_options.add_argument("--use-fake-device-for-media-stream")
# # chrome_options.add_argument("--headless=new")  

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--log-level=3")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142/86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--headless=new")   # no spaces!
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--silent")
service = Service(ChromeDriverManager().install(), log_path="NUL")
# chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")



# initialize the chrome webdriver using ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = chrome_options)

# define the path for temporary files 
TempDirPath = rf"{current_dir}/Frontend/Files"

# funtion to set the assistent status by writing 
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding = 'utf-8') as file:
        file.write(Status)
        

# function to modify a query to ensure proper punctuation and formation
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    
    # check if the query is a question and add a question mark if necessary
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
            
    else:
        #add a period if the query is not a question 
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
            
    return new_query.capitalize()


# funtion to translate text into english using the mtranslate library
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation


# function to perform speech recognition using the WebDriver
# def SpeechRecognition():
#     # open the html file in the browser
#     driver.get("file:///" + link)
#     # satrt speech recognition by clicking the start button 
#     # driver.find_element(by = By.ID, value = "start").click()
#     driver.find_element(By.ID, "start").click()
    
#     while True:
#         try:
#             # get the recognized text from the html output elemnet 
#             # Text = driver.find_element(by = By.ID, value = "output").click()
#             Text = driver.find_element(By.ID, "output").text

            
#             if Text :
#                 # Stop recognition by clicking the stop button
#                 # driver.find_element(by = By.ID, value = "end").click()
#                 # driver.find_element(By.ID, "end").click()

#                 # IF the input language is english, return the modifief query
#                 # if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
#                 if "en" in InputLanguage.lower():
#                     return QueryModifier(Text)
#                 else:
#                     # if the  input language is not english, translate the tect and return it
#                     SetAssistantStatus("Translating ...")
#                     return QueryModifier(UniversalTranslator(Text))
#         except Exception as e:
#             print("Error:", e)
#             time.sleep(0.5)
        
        
def SpeechRecognition():
    driver.get("file:///" + link)
    driver.find_element(By.ID, "start").click()  # start recognition

    while True:
        try:
            # safe read from output
            Text = driver.execute_script("return document.getElementById('output').textContent;")

            if Text:
                if "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating ...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception as e:
            print("Error:", e)
            time.sleep(0.5)


# main execution block 
if __name__ == "__main__":
    while True :
        # Continuosly perform speech regognition and print the recognition text 
        Text = SpeechRecognition()
        print(Text)
        
    





















