import threading
import tkinter as tk
from tkinter import Toplevel, Scale
import customtkinter as ctk
from PIL import Image
import pystray
from pystray import Menu, MenuItem

image = Image.open("pnge.png")

pageSize = 7
current_page = 1
last_search_type = ""
last_search_query = ""
current_results = []

def init_tray(root, engine, status_text):
    def after_click(icon, item):
        if str(item) == "Show Retro Radio":
            root.after(0, root.deiconify)
            root.after(0, root.lift)
        elif str(item) == "Stop Radio":
            engine.stop_station()
            status_text.set("Stopped via tray")
        elif str(item) == "Exit":
            icon.stop()
            root.after(0, root.destroy)

    tray_menu = Menu(
        MenuItem("Show Retro Radio", after_click, default=True),
        MenuItem("Stop Radio", after_click),
        MenuItem("Exit", after_click)
    )

    icon = pystray.Icon("Retro Radio", image, "Retro Radio", menu=tray_menu)
    threading.Thread(target=icon.run, daemon=True).start()

def can_it_move_by_name(engine, search_name, page):
    offset = (page - 1) * pageSize
    stations = engine.search_stations_by_name(search_name, pageSize, offset)
    back_button_active = (page > 1)
    forward_button_active = (len(stations) == pageSize)
    return stations, back_button_active, forward_button_active

def can_it_move_by_tag(engine, search_tag, page):
    offset = (page - 1) * pageSize
    stations = engine.search_stations_by_tag(search_tag, pageSize, offset)
    back_button_active = (page > 1)
    forward_button_active = (len(stations) == pageSize)
    return stations, back_button_active, forward_button_active

def open_volume_control(root, engine):
    top = ctk.CTkToplevel(root)
    top.title("Volume Control")
    top.geometry("180x100")
    top.resizable(False, False)
    top.configure(fg_color="#121212")

    # Maybe I should have made it 100 but 70 is coler
    initial_vol = 70
    
    label = ctk.CTkLabel(top, text=f"Volume: {initial_vol}%", text_color="white", font=("Helvetica", 12))
    label.pack(pady=(10, 0))

    def update_vol(val):
        v = int(val)
        engine.set_volume(v)
        label.configure(text=f"Volume: {v}%")

    slider = ctk.CTkSlider(top, from_=0, to=100, orientation="horizontal", command=update_vol)
    slider.pack(pady=10)
    slider.set(initial_vol)

def search_by_tag(entry, listBox, backButton, forwardButton, engine):
    global last_search_type, last_search_query
    last_search_type = "tag"
    last_search_query = entry.get()
    load_page(1, listBox, backButton, forwardButton, engine)

def search_by_name(entry, listBox, backButton, forwardButton, engine):
    global last_search_type, last_search_query
    last_search_type = "name"
    last_search_query = entry.get()
    load_page(1, listBox, backButton, forwardButton, engine)

def play_selected(event, listBox, engine, status_text):
    global marquee_text, marquee_index
    selection = listBox.curselection()
    if selection:
        index = selection[0]
        station = current_results[index]
        engine.play_station(station["url_resolved"])
        clean_name = station['name'].strip()
        marquee_text = f"Playing: {clean_name}"
        marquee_index = 0

def load_page(page, listBox, backButton, forwardButton, engine):
    global current_page, current_results
    if last_search_type == "name":
        stations, back_active, forward_active = can_it_move_by_name(engine, last_search_query, page)
    elif last_search_type == "tag":
        stations, back_active, forward_active = can_it_move_by_tag(engine, last_search_query, page)
    else:
        return
    current_page = page
    current_results = stations
    listBox.delete(0, tk.END)
    listBox.insert(tk.END, *[station["name"] for station in stations])
    if back_active:
        backButton.configure(state=tk.NORMAL)
    else:
        backButton.configure(state=tk.DISABLED)
    if forward_active:
        forwardButton.configure(state=tk.NORMAL)
    else:
        forwardButton.configure(state=tk.DISABLED)

marquee_text = ""
marquee_index = 0

def start_marquee(root, status_text):
    global marquee_index
    if marquee_text:
        display_length = 22
        padded_text = marquee_text + "   ***   "
        if len(padded_text) > display_length:
            double_text = padded_text + padded_text
            current_display = double_text[marquee_index:marquee_index + display_length]
            status_text.set(current_display)
            marquee_index = (marquee_index + 1) % len(padded_text)
        else:
            status_text.set(padded_text[:display_length])
    root.after(250, lambda: start_marquee(root, status_text))