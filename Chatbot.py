from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = """"""
 
# A list of system instructions for the chatbot.[span_0](start_span)[span_0](end_span)
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat log from a JSON file.[span_4](start_span)[span_4](end_span)
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)  # Load existing messages from the chat log.[span_7](start_span)[span_7](end_span)
except FileNotFoundError:
    # If the file doesn't exist, create an empty JSON file to store chat logs.[span_9](start_span)[span_9](end_span)
    with open(r"Data\ChatLog.json", "w") as f:
        dump([],f)
def RealtimeInformation():
    current_date_time=datetime.datetime.now()
    day = current_date_time.strftime("%A")  # Day of the week.[span_0](start_span)[span_0](end_span)
    date = current_date_time.strftime("%d")  # Day of the month.[span_1](start_span)[span_1](end_span)
    month = current_date_time.strftime("%B")  # Full month name.[span_2](start_span)[span_2](end_span)
    year = current_date_time.strftime("%Y")  # Year.[span_3](start_span)[span_3](end_span)
    hour = current_date_time.strftime("%H")  # Hour in 24-hour format.[span_4](start_span)[span_4](end_span)
    minute = current_date_time.strftime("%M")  # Minute.[span_5](start_span)[span_5](end_span)
    second = current_date_time.strftime("%S")  # Second.[span_6](start_span)[span_6](end_span)

    # Format the information into a string.[span_7](start_span)[span_7](end_span)
    data = f"Please use this real-time information if needed,\n[span_8](start_span)"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n[span_9](start_span)"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n[span_10](start_span)"
    return data


# Function to modify the chatbot's response for better formatting.[span_12](start_span)[span_12](end_span)
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines)  # Join the cleaned lines back together
    return modified_answer

