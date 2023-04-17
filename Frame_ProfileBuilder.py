import tkinter as tk
import customtkinter as ctk
from topmen import TopMenu
from GTPSidebar import GTSidebar
from tkinter import filedialog
from website_scraping import scrape_website
from call_ai import chat_with_ai, openai
import json




class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Main Window")
        self.geometry("1500x800")

        # Create the top menu
        self.top_menu = TopMenu(self)

        # Create the template frame and import the sidebar
        self.template_frame = ctk.CTkFrame(self, corner_radius=0)
        self.template_frame.grid(row=0, column=1, sticky="nsew")

        self.sidebar = GTSidebar(self, width=150)  # Set the width attribute here
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Create a content frame for ProfileBuilder, WebScrape, AISummaryFrame, and KeywordsFrame
        self.content_frame = ctk.CTkFrame(self.template_frame)
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create a frame for the profile builder and place it in the content_frame
        self.profile_builder_frame = ctk.CTkFrame(self.content_frame, width=400, height=450, border_width=0)
        self.profile_builder_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Add the profile builder frame
        self.profile_builder1 = ProfileBuilder(self.profile_builder_frame, self)
        self.profile_builder1.pack()

        # Create a ctk scrollable frame for WebScrape and place it in the content_frame
        self.web_scrape_scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, width=1200, height=450)
        self.web_scrape_scrollable_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Add the WebScrape frame inside the scrollable frame
        self.web_scrape = WebScrape(self.web_scrape_scrollable_frame, self)
        self.web_scrape.pack()

        # Create a container frame for AISummaryFrame and KeywordsFrame
        self.ai_keywords_frame = ctk.CTkFrame(self.content_frame, height=400)
        self.ai_keywords_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Add AISummaryFrame
        self.ai_summary_frame = AISummaryFrame(self.ai_keywords_frame, self)
        self.ai_summary_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Add KeywordsFrame
        self.keywords_frame = KeywordsFrame(self.ai_keywords_frame, self)
        self.keywords_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


class ProfileBuilder(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # Title label
        title_label = ctk.CTkLabel(self, text="Profile Builder", font=("Arial", 18))
        title_label.grid(row=0, column=1, columnspan=2, pady=10)

        # Form fields
        fields = ["Business Name", "Industry", "Physical or ecommerce stores",
                "Website", "Target audience", "Location", "Goal of marketing",
                "Tone of voice"]
        self.entries = []

        for i, field in enumerate(fields):
            label = ctk.CTkLabel(self, text=field)
            label.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self)
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
            self.entries.append(entry)

                # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

        save_button = ctk.CTkButton(button_frame, text="Save Profile", command=self.save_profile)
        save_button.grid(row=0, column=0, padx=5)

        load_button = ctk.CTkButton(button_frame, text="Load Profile", command=self.load_profile)
        load_button.grid(row=0, column=1, padx=5)

    def save_profile(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as f:
                for field, entry in zip(fields, self.entries):
                    f.write(f"{field}: {entry.get()}\n")

    def load_profile(self):
        filename = filedialog.askopenfilename(defaultextension=".txt")
        if filename:
            with open(filename, "r") as f:
                lines = f.readlines()
                for entry, line in zip(self.entries, lines):
                    value = line.split(": ")[1].strip()
                    entry.insert(0, value)
            print("Profile loaded successfully.")

class WebScrape(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.entries = []       
        self.text_boxes = []    
        self.summary_boxes = []  
        self.prompts = []

        default_prompt = ("You are a marketing expert and are creating a report to help us build marketing campaigns. "
                        "Here is a scraped webpage, please provide us with a marketing summary of the business")

        # Configure the weights for the rows and columns
        for i in range(3):
            self.grid_rowconfigure(i * 2 + 1, weight=1)  # Rows with text boxes
            self.grid_columnconfigure(0, weight=1)      # Column with scraped data text boxes
            self.grid_columnconfigure(2, weight=1)      # Column with AI summary text boxes

            scraped_data_label = ctk.CTkLabel(self, text="Scraped Data")
            scraped_data_label.grid(row=i*2, column=0, padx=5, pady=1, sticky="w")

            entry = ctk.CTkEntry(self, placeholder_text=f"Enter URL {i+1}", width=50)
            entry.grid(row=i*2, column=2, padx=5, pady=1, sticky="ew")
            self.entries.append(entry)

            scrape_button = ctk.CTkButton(self, text="Scrape", command=lambda i=i: self.scrape_website(self.entries[i].get()))
            scrape_button.grid(row=i*2, column=1, padx=5, pady=1)

            text_box = ctk.CTkTextbox(self, wrap="word", width=600, height=125)
            text_box.grid(row=i*2+1, column=0, columnspan=3, padx=5, pady=1, sticky="nsew")
            self.text_boxes.append(text_box)

            summary_label = ctk.CTkLabel(self, text="Summary")
            summary_label.grid(row=i*2, column=3, padx=5, pady=1, sticky="w")

            prompt_entry = ctk.CTkEntry(self, width=50)
            prompt_entry.grid(row=i*2, column=5, padx=5, pady=1, sticky="ew")  
            prompt_entry.insert(0, default_prompt)
            self.prompts.append(prompt_entry)

            summarize_button = ctk.CTkButton(self, text="Summarize", command=lambda i=i: self.summarize_text(i))
            summarize_button.grid(row=i*2, column=4, padx=5, pady=1)

            edit_prompt_button = ctk.CTkButton(self, text="Edit Prompt", command=lambda i=i: self.edit_prompt(i))
            edit_prompt_button.grid(row=i*2, column=6, padx=5, pady=1)

            summary_box = ctk.CTkTextbox(self, wrap="word", width=600, height=125)
            summary_box.grid(row=i*2+1, column=3, columnspan=4, padx=5, pady=1, sticky="nsew")
            self.summary_boxes.append(summary_box)

    def scrape_website(self, url):
        scraped_text = scrape_website(url)
        text_box_index = next((i for i, entry in enumerate(self.entries) if entry.get() == url), None)
        if text_box_index is not None:
            self.text_boxes[text_box_index].delete(1.0, 'end')
            self.text_boxes[text_box_index].insert(1.0, scraped_text)
        else:
            print("URL not found in the entries.")

    def summarize_text(self, index):
        prompt = self.prompts[index].get()
        scraped_text = self.text_boxes[index].get("1.0", tk.END).strip()

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n{scraped_text}"}
        ]

        # Pass the sidebar instance to chat_with_ai
        response = tk.StringVar()
        chat_with_ai(self.controller.sidebar, messages, response)
        summarized_text = response.get()

        self.summary_boxes[index].delete("1.0", tk.END)
        self.summary_boxes[index].insert(tk.END, summarized_text)

    def edit_prompt(self, index):
            prompt_window = tk.Toplevel(self)
            prompt_window.title("Edit Prompt")

            prompt_entry = ctk.CTkEntry(prompt_window, width=80)
            prompt_entry.pack(padx=10, pady=10)
            prompt_entry.insert(0, self.prompts[index].get())

            save_button = ctk.CTkButton(prompt_window, text="Save", command=lambda: self.save_prompt(prompt_entry.get(), index))
            save_button.pack(pady=(0, 10))

    def save_prompt(self, new_prompt, index):
        self.prompts[index].delete(0, tk.END)
        self.prompts[index].insert(0, new_prompt)



class AISummaryFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # Title label
        title_label = ctk.CTkLabel(self, text="AI Summary of Business", font=("Arial", 18))
        title_label.grid(row=0, column=0, pady=1)

        # Large text box
        self.summary_box = ctk.CTkTextbox(self, wrap="word", width=600, height=400)
        self.summary_box.grid(row=1, column=0, padx=5, pady=1, sticky="nsew")

        # Summarize business button
        summarize_button = ctk.CTkButton(self, text="Summarize Business", command=self.summarize_business)
        summarize_button.grid(row=2, column=0, pady=10)

    def summarize_business(self):
        scraped_text = ""
        for i in range(3):
            scraped_text += self.controller.web_scrape.text_boxes[i].get("1.0", tk.END).strip()

        prompt = ("You are a marketing expert and are creating a report to help us build marketing campaigns. "
                "Here is a summary of the business:")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n{scraped_text}"}
        ]

        # Pass the sidebar instance to chat_with_ai
        response = tk.StringVar()
        chat_with_ai(self.controller.sidebar, messages, response)
        summarized_text = response.get()

        self.summary_box.delete("1.0", tk.END)
        self.summary_box.insert(tk.END, summarized_text)

class KeywordsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # Title label
        title_label = ctk.CTkLabel(self, text="Keywords", font=("Arial", 18))
        title_label.grid(row=0, column=0, pady=1)

        # Large text box
        self.summary_box = ctk.CTkTextbox(self, wrap="word", width=600, height=400)
        self.summary_box.grid(row=1, column=0, padx=5, pady=1, sticky="nsew")

        # create keywords button
        generate_keywords_button = ctk.CTkButton(self, text="Keyword Generation", command=self.generate_keywords)
        generate_keywords_button.grid(row=2, column=0, pady=10)

    def generate_keywords(self):
        scraped_text = ""
        for i in range(3):
            scraped_text += self.controller.web_scrape.text_boxes[i].get("1.0", tk.END).strip()
        
        ai_summary = self.controller.ai_summary_frame.summary_box.get("1.0", tk.END).strip()

        prompt = ("Generate a comma-separated list of keywords that should be used in marketing for the company described. "
                  "50 positive keywords, 25 negative keywords, and 25 long-tail keywords. "
                  "Also, describe a persona. "
                  f"\n\nScraped Data:\n{scraped_text}\n\nAI Summary:\n{ai_summary}")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        # Pass the sidebar instance to chat_with_ai
        response = tk.StringVar()
        chat_with_ai(self.controller.sidebar, messages, response)
        generated_keywords = response.get()

        self.summary_box.delete("1.0", tk.END)
        self.summary_box.insert(tk.END, generated_keywords)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
