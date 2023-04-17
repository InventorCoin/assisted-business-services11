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
from tkinter import filedialog
from bs4 import BeautifulSoup
import re

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

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

        # Add the profile builder frame
        self.profile_builder = ProfileBuilder(self.template_frame, self)
        self.profile_builder.grid(row=0, column=1, padx=20, pady=20)

        # Add the websitescrape frame
        self.website_scrape = WebsiteScrape(self.template_frame, self)
        self.website_scrape.grid(row=0, column=1, padx=20, pady=20)
        self.website_scrape.grid_remove()  # Hide the frame initially


class WebsiteScrape(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, bg_color="#ffffff", corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        # Title label
        title_label = ctk.CTkLabel(self, text="Website Scrape", font=("Arial", 24), bg_color="#ffffff", fg_color="#000000")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Website URL
        website_label = ctk.CTkLabel(self, text="Website URL:", bg_color="#ffffff", fg_color="#000000")
        website_label.grid(row=1, column=0, sticky="w", padx=10)
        self.website_entry = ctk.CTkEntry(self, width=50)
        self.website_entry.grid(row=1, column=1, padx=10)

        # Scrape URL button
        scrape_button = ctk.CTkButton(self, text="Scrape URL", command=self.scrape_website)
        scrape_button.grid(row=2, column=1, pady=10)

        # Scrape URL results
        scrape_results_frame = ctk.CTkLabelFrame(self, text="Scraped Text", bg_color="#ffffff", fg_color="#000000")
        scrape_results_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        scrape_results_frame.columnconfigure(0, weight=1)
        scrape_results_frame.rowconfigure(0, weight=1)
        self.text_box = scrolledtext.ScrolledText(scrape_results_frame, height=10, width=120, wrap=tk.WORD)
        self.text_box.pack(expand=True, fill="both")

        ai_summary_frame = ctk.CTkLabelFrame(self, text="AI Summary", bg_color="#ffffff", fg_color="#000000")
        ai_summary_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        ai_summary_frame.columnconfigure(0, weight=1)
        ai_summary_frame.rowconfigure(0, weight=1)
        self.ai_summary_box = scrolledtext.ScrolledText(ai_summary_frame, height=7, width=120, wrap=tk.WORD)
        self.ai_summary_box.pack(expand=True, fill="both")

        # Ask AI button
        ask_ai_button = ctk.CTkButton(self, text="Ask Mark to Summarize my website", command=self.ask_ai_summarize)
        ask_ai_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Keywords
        keywords_frame = ctk.CTkLabelFrame(self, text="Keywords", bg_color="#ffffff", fg_color="#000000")
        keywords_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        keywords_frame.columnconfigure(0, weight=1)
        keywords_frame.rowconfigure(0, weight=1)
        self.keywords_box = scrolledtext.ScrolledText(keywords_frame, height=10, width=120, wrap=tk.WORD)
        self.keywords_box.pack(expand=True, fill="both")

        # Generate Keywords button
        generate_keywords_button = ctk.CTkButton(self, text="Generate High Converting keywords, and negative keywords", command=self.generate_keywords)
        generate_keywords_button.grid(row=7, column=0, columnspan=2, pady=10)

    def scrape_website(self):
        # Placeholder method for scraping the website
        pass

    def ask_ai_summarize(self):
        # Placeholder method for asking AI to summarize the website
        pass

    def generate_keywords(self):
        # Placeholder method for generating high converting keywords and negative keywords
        pass

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
