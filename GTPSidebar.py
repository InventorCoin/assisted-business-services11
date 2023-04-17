import tkinter
import tkinter.messagebox
import customtkinter as ctk
from tkinter import Menu, StringVar
from customtkinter import CTkOptionMenu
import openai
from my_secrets import API_KEY
from tkinter import Menu, StringVar
from customtkinter import CTkOptionMenu
import requests


class GTSidebar(tkinter.LabelFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.create_sidebar_widgets()

        # configure grid layout (4x4)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure((2, 3), weight=0)
        self.master.grid_rowconfigure((0, 1, 2), weight=1)

    
    def create_sidebar_widgets(self):
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self.master, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ChatGPT Settings",
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Add a title label for the CTkOptionMenu
        self.optionmenu_1_title = ctk.CTkLabel(self.sidebar_frame, text="Model")
        self.optionmenu_1_title.grid(row=1, column=0, padx=20, pady=(10, 0))

        # Replace sidebar_button_1 with CTkOptionMenu
        self.optionmenu_1 = ctk.CTkOptionMenu(self.sidebar_frame,
                                              dynamic_resizing=False,
                                              values=["gpt-4-0314", "gpt-3.5-turbo"])
        self.optionmenu_1.grid(row=2, column=0, padx=20, pady=(0, 5))

        # Add a title label for the "Max tokens" section
        self.max_tokens_label = ctk.CTkLabel(self.sidebar_frame, text="Max tokens")
        self.max_tokens_label.grid(row=3, column=0, padx=20, pady=(5, 0))

        # Replace sidebar_button_2 with CTkEntry
        self.entry = ctk.CTkEntry(self.sidebar_frame, width=3, placeholder_text="Enter max tokens")
        self.entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.entry.insert(0, '1500')  # Set default value to 1500


        # Add a title label for the "Model temperature" section
        self.model_temperature_label = ctk.CTkLabel(self.sidebar_frame, text="Model temperature")
        self.model_temperature_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        # Replace sidebar_button_3 with CTkSlider   
        self.slider_1 = ctk.CTkSlider(self.sidebar_frame, from_=0.1, to=1, number_of_steps=10,
                                      command=self.update_slider_label)
        self.slider_1.grid(row=6, column=0, padx=(20, 10), pady=(0, 10), sticky="ew")

        self.slider_value_label = ctk.CTkLabel(self.sidebar_frame, text="Value: 0.1")
        self.slider_value_label.grid(row=7, column=0, padx=20, pady=(0, 2))

        # Add a title label for the "n" section
        self.n_label = ctk.CTkLabel(self.sidebar_frame, text="n")
        self.n_label.grid(row=13, column=0, padx=20, pady=(10, 0))

        # Add CTkEntry for "n"
        self.n_entry = ctk.CTkEntry(self.sidebar_frame, width=3, placeholder_text="Enter n")
        self.n_entry.grid(row=14, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Add a title label for the "stop" section
        self.stop_label = ctk.CTkLabel(self.sidebar_frame, text="Stop")
        self.stop_label.grid(row=15, column=0, padx=20, pady=(10, 0))

        # Add CTkEntry for "stop"
        self.stop_entry = ctk.CTkEntry(self.sidebar_frame, width=3, placeholder_text="Enter stop")
        self.stop_entry.grid(row=16, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Add a title label for the "top_p" section
        self.top_p_label = ctk.CTkLabel(self.sidebar_frame, text="Top p")
        self.top_p_label.grid(row=17, column=0, padx=20, pady=(10, 0))

        # Add CTkEntry for "top_p"
        self.top_p_entry = ctk.CTkEntry(self.sidebar_frame, width=3, placeholder_text="Enter top_p")
        self.top_p_entry.grid(row=18, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Add a title label for the "Frequency penalty" section
        self.frequency_penalty_label = ctk.CTkLabel(self.sidebar_frame, text="Frequency penalty")
        self.frequency_penalty_label.grid(row=19, column=0, padx=20, pady=(10, 0))

        # Add CTkEntry for "frequency_penalty"
        self.frequency_penalty_entry = ctk.CTkEntry(self.sidebar_frame, width=3, placeholder_text="Enter freq. penalty")
        self.frequency_penalty_entry.grid(row=20, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Add a title label for the "Presence penalty" section
        self.presence_penalty_label = ctk.CTkLabel(self.sidebar_frame, text="Presence penalty")
        self.presence_penalty_label.grid(row=21, column=0, padx=20, pady=(10, 0))

        # Add CTkEntry for "presence_penalty"
        self.presence_penalty_entry = ctk.CTkEntry(self.sidebar_frame, width=3, placeholder_text="Enter pres. penalty")
        self.presence_penalty_entry.grid(row=22, column=0, padx=20, pady=(0, 10), sticky="nsew")


        # Navigation buttons at the bottom
        self.navigation_label = ctk.CTkLabel(self.sidebar_frame, text="Navigation",
                                             font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_label.grid(row=24, column=0, padx=20, pady=(20, 5))

        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Button 4", command=self.sidebar_button_event)
        self.sidebar_button_4.grid(row=25, column=0, padx=20, pady=5)
        self.sidebar_button_5 = ctk.CTkButton(self.sidebar_frame, text="Button 5", command=self.sidebar_button_event)
        self.sidebar_button_5.grid(row=26, column=0, padx=20, pady=5)
        self.sidebar_button_6 = ctk.CTkButton(self.sidebar_frame, text="Button 6", command=self.sidebar_button_event)
        self.sidebar_button_6.grid(row=27, column=0, padx=20, pady=5)

    def update_slider_label(self, value):
        # Update the slider value label
        formatted_value = f"{float(value):.1f}"
        self.slider_value_label.configure(text=f"Value: {formatted_value}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def update_top_p_slider_label(self, value):
        formatted_value = f"{float(value):.1f}"
        self.top_p_value_label.configure(text=f"Value: {formatted_value}")

    def update_frequency_penalty_slider_label(self, value):
        formatted_value = f"{float(value):.1f}"
        self.frequency_penalty_value_label.configure(text=f"Value: {formatted_value}")

    def update_presence_penalty_slider_label(self, value):
        formatted_value = f"{float(value):.1f}"
        self.presence_penalty_value_label.configure(text=f"Value: {formatted_value}")

if __name__ == "__main__":
    app = GTSidebar()
    app.mainloop()