
import datetime
from json import dump, load
from dotenv import dotenv_values
from googlesearch import search
from groq import Groq

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")  # Fixed key name
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)
FILE_PATH = r"Data\ChatLog.json"

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try:
    with open(FILE_PATH, "r") as f:
        messages = load(f)
except Exception:
    with open(FILE_PATH, "w") as f:
        dump([], f)
        messages = []


def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f" The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer


def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)


# Fixed role name string formatting
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"},
]


def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%m")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = "Use This Real-time Information if needed:\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data


def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    try:
        with open(FILE_PATH, "r") as f:
            messages = load(f)
    except Exception:
        messages = []

    messages.append({"role": "user", "content": f"{prompt}"})

    search_result_msg = {"role": "system", "content": GoogleSearch(prompt)}
    SystemChatBot.append(search_result_msg)

    # Fixed valid model name
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot
        + [{"role": "system", "content": Information()}]
        + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None,
    )

    Answer = ""
    # Complete response loop first before returning
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("~~", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save updated history
    with open(FILE_PATH, "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()  # Clean up temp system message
    return AnswerModifier(Answer=Answer)


# Fixed Indentation
if __name__ == "__main__":
    while True:
        prompt = input("Enter your Query: ")
        if prompt.lower() in ["exit", "quit"]:
            break
        print(RealtimeSearchEngine(prompt))