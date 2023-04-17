import openai
from my_secrets import API_KEY
import tkinter as tk

openai.api_key = API_KEY
URL = "https://api.openai.com/v1/chat/completions"

def chat_with_ai(sidebar, messages, callback):
    model = sidebar.optionmenu_1.get()
    max_tokens = int(sidebar.entry.get())
    temperature = float(sidebar.slider_1.get())

    ai_response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Check if the response is from GPT-4 or GPT-3.5-turbo
    if 'choices' in ai_response and len(ai_response.choices) > 0:
        if 'message' in ai_response.choices[0]:
            ai_text = ai_response.choices[0].message['content'].strip()  # GPT-3.5-turbo
        else:
            ai_text = ai_response.choices[0].text.strip()  # GPT-4
    else:
        ai_text = ""

    # Call the callback function with the AI response
    callback(ai_text)
