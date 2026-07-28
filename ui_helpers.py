import threading
import tkinter as tk
from tkinter import Toplevel, Scale
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
    top = Toplevel(root)
    top.title("Volume Control")
    top.geometry("100x80")
    top.configure(bg="#121212")
    scale = Scale(top, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", bg="#333333", fg="white", command=lambda val: engine.set_volume(int(val)))
    scale.pack(pady=10)
    scale.set(70)

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
    selection = listBox.curselection()
    if selection:
        index = selection[0]
        station = current_results[index]
        engine.play_station(station["url_resolved"])
        status_text.set(f"Playing: {station['name']}")

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