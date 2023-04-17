import tkinter as tk
from topmen import TopMenu
from GTPSidebar import GTSidebar
import customtkinter as ctk
import os
import json
import requests
from threading import Thread
from PIL import Image, ImageTk
from background_images import background_image_1  # Import the image path from background_images.py
from my_secrets import API_KEY



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Main Window")
        self.geometry("800x600")

        # Create the top menu
        self.top_menu = TopMenu(self)

        # Create the template frame and import the sidebar
        self.template_frame = ctk.CTkFrame(self, corner_radius=0)
        self.template_frame.grid(row=0, column=1, sticky="nsew")

        self.sidebar = GTSidebar(self, width=200)  # Set the width attribute here
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)  # Change weight to 0
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Chat UI
        self.conversation_text = tk.Text(self.template_frame, wrap=tk.WORD)
        self.conversation_text.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.user_input = ctk.CTkEntry(self.template_frame, placeholder_text="Type your message here...")
        self.user_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.submit_button = ctk.CTkButton(self.template_frame, text="Send", command=self.on_send_button_click)
        self.submit_button.grid(row=1, column=1, padx=20, pady=10)

        # Configure the template frame grid layout
        self.template_frame.grid_columnconfigure(0, weight=3)
        self.template_frame.grid_columnconfigure(1, weight=1)

        try:
            # Load the background image
            image = Image.open(background_image_1)  # Use the imported image path
            image = image.resize((300, 300), Image.ANTIALIAS)  # Resize the image to 300x300 pixels
            self.background_image = ImageTk.PhotoImage(image)  # Convert the image to a PhotoImage

            # Create a label to display the background image
            self.background_label = tk.Label(self, image=self.background_image)
            self.background_label.place(x=0, y=0, relx=1, rely=1, anchor="se")  # Position the label in the bottom right corner
            self.background_label.lift()  # Bring the label to the front
        except FileNotFoundError:
            print(f"Error: Background image file not found: {background_image_1}")

    def on_send_button_click(self):
        user_msg = self.user_input.get()
        self.conversation_text.insert(tk.END, f"\nYou: {user_msg}")

        # Clear the user input field
        self.user_input.delete(0, tk.END)

        # Call AI chat function in a separate thread
        chat_thread = Thread(target=self.chat_with_ai, args=(user_msg,))
        chat_thread.start()

    def chat_with_ai(self, user_msg):
        user_message = {"role": "system", "content": "You are a helpful assistant."}
        ai_message = {"role": "user", "content": user_msg}
        messages = [user_message, ai_message]

        # Call AI chat function in a separate thread
        response = self.sidebar.call_openai(messages=messages)
        ai_response = ""

        if response:
            ai_response = response

        # Display AI's response in the conversation_text widget
        self.conversation_text.insert(tk.END, "\nAI: " + ai_response)



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
