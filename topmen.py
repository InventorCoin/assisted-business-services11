import tkinter as tk
from tkinter import Menu, StringVar
import customtkinter

class TopMenu:
    def __init__(self, master):
        self.master = master
        self.top_menu_bar = Menu(master)
        master.config(menu=self.top_menu_bar)

        self.appearance_mode_var = StringVar(master)
        self.appearance_mode_var.set("System")
        self.appearance_mode_menu = Menu(self.top_menu_bar, tearoff=0)
        self.appearance_mode_menu.add_radiobutton(label="Light", variable=self.appearance_mode_var, value="Light",
                                                  command=lambda: self.change_appearance_mode_event(self.appearance_mode_var.get()))
        self.appearance_mode_menu.add_radiobutton(label="Dark", variable=self.appearance_mode_var, value="Dark",
                                                  command=lambda: self.change_appearance_mode_event(self.appearance_mode_var.get()))
        self.appearance_mode_menu.add_radiobutton(label="System", variable=self.appearance_mode_var, value="System",
                                                  command=lambda: self.change_appearance_mode_event(self.appearance_mode_var.get()))

        self.scaling_var = StringVar(master)
        self.scaling_var.set("100%")
        self.scaling_menu = Menu(self.top_menu_bar, tearoff=0)
        self.scaling_menu.add_radiobutton(label="80%", variable=self.scaling_var, value="80%",
                                          command=lambda: self.change_scaling_event(self.scaling_var.get()))
        self.scaling_menu.add_radiobutton(label="90%", variable=self.scaling_var, value="90%",
                                          command=lambda: self.change_scaling_event(self.scaling_var.get()))
        self.scaling_menu.add_radiobutton(label="100%", variable=self.scaling_var, value="100%",
                                          command=lambda: self.change_scaling_event(self.scaling_var.get()))
        self.scaling_menu.add_radiobutton(label="110%", variable=self.scaling_var, value="110%",
                                          command=lambda: self.change_scaling_event(self.scaling_var.get()))
        self.scaling_menu.add_radiobutton(label="120%", variable=self.scaling_var, value="120%",
                                          command=lambda: self.change_scaling_event(self.scaling_var.get()))

        self.top_menu_bar.add_cascade(label="Appearance Mode", menu=self.appearance_mode_menu)
        self.top_menu_bar.add_cascade(label="UI Scaling", menu=self.scaling_menu)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
