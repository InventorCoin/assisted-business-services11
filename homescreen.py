import tkinter as tk
import customtkinter as ctk
from topmen import TopMenu
import Frame_ProfileBuilder
import Frame_GTP_Chat


class AiAssistedServices(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("AI Assisted Services")
        self.geometry("800x400")

        # Create the top menu
        self.top_menu = TopMenu(self)

        # Create header
        header = tk.Label(self, text="AI Assisted Services", font=("Arial", 24))
        header.grid(row=0, column=1, columnspan=3, pady=20)

        # Configure column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        # Create buttons
        gpt_chat_button = ctk.CTkButton(self, text="GPT Chat", font=("Arial", 18), command=self.show_gpt_chat)
        gpt_chat_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        profile_builder_button = ctk.CTkButton(self, text="Profile Builder", font=("Arial", 18), command=self.show_profile_builder)
        profile_builder_button.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        # Create the frames
        self.gpt_chat_frame = Frame_GTP_Chat.GPTChatFrame(self)
        self.profile_builder_frame = Frame_ProfileBuilder.ProfileBuilderFrame(self)

        self.gpt_chat_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.profile_builder_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")

        # Configure row weight
        self.rowconfigure(2, weight=1)

    def open_gpt_chat(self):
        self.gpt_chat_frame = Frame_GTP_Chat.GPTChatFrame(self)
        self.gpt_chat_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    def open_profile_builder(self):
        self.profile_builder_frame = Frame_ProfileBuilder.ProfileBuilderFrame(self)
        self.profile_builder_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

    # Add this method
    def show_gpt_chat(self):
        self.open_gpt_chat()

    # Update this method
    def open_profile_builder(self):
        self.profile_builder_frame = Frame_ProfileBuilder.ProfileBuilderFrame(self)
        self.profile_builder_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    app = AiAssistedServices()
    app.mainloop()