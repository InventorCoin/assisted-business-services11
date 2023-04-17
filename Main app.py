import tkinter as tk
from topmen import TopMenu
from GTPSidebar import GTSidebar
import customtkinter as ctk

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

        # Create text boxes with placeholder text and buttons
        self.entries = []
        self.buttons = []
        for i in range(4):
            entry = ctk.CTkEntry(self.template_frame, placeholder_text=f"Placeholder text {i+1}")
            entry.grid(row=i, column=0, padx=20, pady=10, sticky="ew")
            self.entries.append(entry)

            button = ctk.CTkButton(self.template_frame, text=f"Button {i+1}", command=lambda i=i: self.button_click(i))
            button.grid(row=i, column=1, padx=20, pady=10)
            self.buttons.append(button)

        # Configure the template frame grid layout
        self.template_frame.grid_columnconfigure(0, weight=3)
        self.template_frame.grid_columnconfigure(1, weight=1)

    def button_click(self, index):
        print(f"Button {index + 1} clicked. Textbox content: {self.entries[index].get()}")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
