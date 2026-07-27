from tkinter import font
from RadioEngine import Engine
import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title("Radio Engine V1.0")

status_text = StringVar()
status_text.set("No station playing")

engine = Engine()
current_results = []

root.geometry("350x400")
root.resizable(False, False)
root.configure(bg="#121212")

def open_volume_control():
    top = Toplevel(root)
    top.title("Volume Control")
    top.geometry("100x80")
    top.configure(bg="#121212")
    scale = Scale(top, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", bg="#333333", fg="white", command=lambda val: engine.set_volume(int(val)))
    scale.pack(pady=10)
    scale.set(70)

def search_by_tag():
    global current_results
    tag = entry.get()
    current_results = engine.search_stations_by_tag(tag, 20)
    listBox.delete(0, tk.END)
    for station in current_results:
        listBox.insert(tk.END, station["name"])

def search_by_name():
    global current_results
    name = entry.get()
    current_results = engine.search_stations_by_name(name, 20)
    listBox.delete(0, tk.END)
    for station in current_results:
        listBox.insert(tk.END, station["name"])

def play_selected(event):
    selection = listBox.curselection()
    if selection:
        index = selection[0]
        station = current_results[index]
        engine.play_station(station["url_resolved"])
        status_text.set(f"Playing: {station['name']}")

volume_button = tk.Button(root, text="🔊", font=("Helvetica", 12), width=4, bg="#333333", fg="white", command=open_volume_control)
volume_button.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")

tk.Label(root, text="Retro Radio", font=("Helvetica", 20), bg="#121212", fg="white").pack(pady=(20, 10))

tk.Label(root, font=("Courier", 12), borderwidth=2, relief="groove", bg="#0a2211", fg="#00ff66", textvariable=status_text).pack(ipadx=20, ipady=10, pady=10)

entry = tk.Entry(root, width=25, bg="#333333", fg="white", insertbackground="white")
entry.pack(pady=10)

listBox = tk.Listbox(root, width=45, height=6, bg="#333333", fg="white", selectbackground="#00ff66", selectforeground="black")
listBox.pack(pady=10)
listBox.bind("<<ListboxSelect>>", play_selected)

button = tk.Button(root, text="Search stations by tag", width=35, bg="#333333", fg="white", command=search_by_tag)
button.pack()

button2 = tk.Button(root, text="Search stations by name", width=35, bg="#333333", fg="white", command=search_by_name)
button2.pack()

button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)

stopButton = tk.Button(button_frame, text="Stop", width=7, bg="#333333", fg="white", command=engine.stop_station)
stopButton.pack(side=tk.LEFT, padx=10)

resumeButton = tk.Button(button_frame, text="Resume", width=7, bg="#333333", fg="white", command=lambda: engine.play_station(engine.player.get_media().get_mrl()) if engine.player else None)
resumeButton.pack(side=tk.LEFT, padx=10)

root.mainloop()