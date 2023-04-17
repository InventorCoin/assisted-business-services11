import tkinter as tk
from tkinter import scrolledtext
from topmen import TopMenu
from GTPSidebar import GTSidebar
import customtkinter as ctk
import os
import json
import requests
from threading import Thread
from PIL import Image, ImageTk
from my_secrets import API_KEY
from call_ai import chat_with_ai  # Import the chat_with_ai function from call_ai.py

class GPTChatFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure the main window
        self.title("Main Window")
        self.geometry("1200x1000")

        # Create the top menu
        self.top_menu = TopMenu(self)

        # Create the template frame and import the sidebar
        self.template_frame = ctk.CTkFrame(self, corner_radius=0)
        self.template_frame.grid(row=0, column=1, sticky="nsew")

        self.sidebar = GTSidebar(self, width=200)  # Set the width attribute here
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Configure grid layout 
        self.grid_columnconfigure(0, weight=0)  # Change weight to 0
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=8)

        # Chat UI
        self.conversation_text = ctk.CTkTextbox(self.template_frame, height=20)
        self.conversation_text.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")

        self.user_input_frame = ctk.CTkFrame(self.template_frame)
        self.user_input_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew", rowspan=5)

        self.user_input = ctk.CTkEntry(self.user_input_frame, placeholder_text="Type your message here...")
        self.user_input.pack(side="left", fill="both", expand=True)

        self.submit_button = ctk.CTkButton(self.user_input_frame, text="Send", command=self.on_send_button_click)
        self.submit_button.pack(side="right", padx=5, pady=5)

        # Configure the template frame grid layout
        self.template_frame.grid_columnconfigure(0, weight=3)
        self.template_frame.grid_columnconfigure(1, weight=2)
        self.template_frame.grid_rowconfigure(0, weight=10)
        self.template_frame.grid_rowconfigure(1, weight=5)

        # Initialize chat history list
        self.chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

    def display_ai_response(self, ai_text):
        self.conversation_text.insert(tk.END, f"\nAI: {ai_text}")

    def on_send_button_click(self):
        user_msg = self.user_input.get()
        self.conversation_text.insert(tk.END, f"\nYou: {user_msg}")

        # Clear the user input field
        self.user_input.delete(0, tk.END)

        # Append the user's message to the chat history
        self.chat_history.append({"role": "user", "content": user_msg})

        # Call AI chat function in a separate thread
        chat_thread = Thread(target=chat_with_ai, args=(self.sidebar, self.chat_history, self.display_ai_response))
        chat_thread.start()



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
