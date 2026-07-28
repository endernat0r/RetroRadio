import threading
import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import Image
import pystray
from pystray import Menu, MenuItem
from RadioEngine import Engine

image = Image.open("pnge.png")

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

root = tk.Tk()
root.title("Radio Engine V1.0")

def on_close():
    root.withdraw()

root.protocol("WM_DELETE_WINDOW", on_close)

status_text = StringVar()
status_text.set("No station playing")

engine = Engine()
current_results = []

root.geometry("350x440")
root.resizable(False, False)
root.configure(bg="#121212")

pageSize = 6
current_page = 1
last_search_type = ""
last_search_query = ""
stations = []

def can_it_move_by_name(search_name, page):
    offset = (page - 1) * pageSize
    stations = engine.search_stations_by_name(search_name, pageSize, offset)
    back_button_active = (page > 1)
    forward_button_active = (len(stations) == pageSize)
    return stations, back_button_active, forward_button_active

def can_it_move_by_tag(search_tag, page):
    offset = (page - 1) * pageSize
    stations = engine.search_stations_by_tag(search_tag, pageSize, offset)
    back_button_active = (page > 1)
    forward_button_active = (len(stations) == pageSize)
    return stations, back_button_active, forward_button_active

def open_volume_control():
    top = Toplevel(root)
    top.title("Volume Control")
    top.geometry("100x80")
    top.configure(bg="#121212")
    scale = Scale(top, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", bg="#333333", fg="white", command=lambda val: engine.set_volume(int(val)))
    scale.pack(pady=10)
    scale.set(70)

def search_by_tag():
    global last_search_type, last_search_query
    last_search_type = "tag"
    last_search_query = entry.get()
    load_page(1)

def search_by_name():
    global last_search_type, last_search_query
    last_search_type = "name"
    last_search_query = entry.get()
    load_page(1)

def play_selected(event):
    selection = listBox.curselection()
    if selection:
        index = selection[0]
        station = current_results[index]
        engine.play_station(station["url_resolved"])
        status_text.set(f"Playing: {station['name']}")

def load_page(page):
    global current_page, current_results
    if last_search_type == "name":
        stations, back_active, forward_active = can_it_move_by_name(last_search_query, page)
    elif last_search_type == "tag":
        stations, back_active, forward_active = can_it_move_by_tag(last_search_query, page)
    else:
        return
    current_page = page
    current_results = stations
    listBox.delete(0, tk.END)
    listBox.insert(tk.END, *[station["name"] for station in stations])
    if back_active:
        backButton.config(state=tk.NORMAL)
    else:
        backButton.config(state=tk.DISABLED)
    if forward_active:
        forwardButton.config(state=tk.NORMAL)
    else:
        forwardButton.config(state=tk.DISABLED)

volume_button = tk.Button(root, text="🔊", font=("Helvetica", 12), width=4, bg="#333333", fg="white", command=open_volume_control)
volume_button.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")

tk.Label(root, text="Retro Radio", font=("Helvetica", 20), bg="#121212", fg="white").pack(pady=(20, 10))

tk.Label(root, font=("Courier", 12), borderwidth=2, relief="groove", bg="#0a2211", fg="#00ff66", textvariable=status_text).pack(ipadx=20, ipady=10, pady=10)

entry = tk.Entry(root, width=25, bg="#333333", fg="white", insertbackground="white")
entry.pack(pady=10)

listBox = tk.Listbox(root, width=45, height=6, bg="#333333", fg="white", selectbackground="#00ff66", selectforeground="black")
listBox.pack(pady=10)
listBox.bind("<<ListboxSelect>>", play_selected)

button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)

backButton = tk.Button(button_frame, text="<< Back", width=10, bg="#333333", fg="white", command=lambda: load_page(current_page - 1))
backButton.pack(side=tk.LEFT, padx=10)

forwardButton = tk.Button(button_frame, text="Forward >>", width=10, bg="#333333", fg="white", command=lambda: load_page(current_page + 1))
forwardButton.pack(side=tk.RIGHT, padx=10)

button = tk.Button(root, text="Search stations by tag", width=35, bg="#333333", fg="white", command=search_by_tag)
button.pack()

button2 = tk.Button(root, text="Search stations by name", width=35, bg="#333333", fg="white", command=search_by_name)
button2.pack()

button_frame2 = tk.Frame(root, bg="#121212")
button_frame2.pack(pady=10)

stopButton = tk.Button(button_frame2, text="Stop", width=7, bg="#333333", fg="white", command=engine.stop_station)
stopButton.pack(side=tk.LEFT, padx=10)

resumeButton = tk.Button(button_frame2, text="Resume", width=7, bg="#333333", fg="white", command=lambda: engine.play_station(engine.player.get_media().get_mrl()) if engine.player else None)
resumeButton.pack(side=tk.LEFT, padx=10)

root.mainloop()