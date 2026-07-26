from tkinter import font

from RadioEngine import Engine
import tkinter as tk
from tkinter import Scale, StringVar

root = tk.Tk()
root.title("Radio Engine V1.0")

status_text = StringVar()
status_text.set("No station playing")

engine = Engine()

root.geometry("300x380")

root.resizable(False, False)

root.configure(bg="#121212")

def search_and_play_by_tag():
    tag = entry.get()
    station = engine.radio_search_by_tag_and_play(tag, 5)
    if station:
        status_text.set(f"Playing: {station['name']}")
    else:
        status_text.set("No station found for the given tag.")

def search_and_play_by_name():
    name = entry.get()
    station = engine.radio_search_by_name_and_play(name, 5)
    if station:
        status_text.set(f"Playing: {station['name']}")
    else:
        status_text.set("No station found for the given name.")

tk.Label(root, text="Retro Radio", font=("Helvetica", 20), bg="#121212", fg="white").pack(pady=20)

tk.Label(root, font=("Courier", 12), borderwidth=2, relief="groove", bg="#0a2211", fg="#00ff66", textvariable=status_text).pack(ipadx=20, ipady=10, pady=10)

entry = tk.Entry(root, width=20, bg="#333333", fg="white", insertbackground="white")
entry.pack(pady=10)

button = tk.Button(root, text="Listen to a station by entering a tag", width=35, bg="#333333", fg="white", command=search_and_play_by_tag)
button.pack()

button2 = tk.Button(root, text="Listen to a station by entering a name", width=35, bg="#333333", fg="white", command=search_and_play_by_name)
button2.pack()

button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)

stopButton = tk.Button(button_frame, text="Stop", width=7, bg="#333333", fg="white", command=engine.stop_station)
stopButton.pack(side=tk.LEFT, padx=10)

resumeButton = tk.Button(button_frame, text="Resume", width=7, bg="#333333", fg="white", command=lambda: engine.play_station(engine.player.get_media().get_mrl()) if engine.player else None)
resumeButton.pack(side=tk.LEFT, padx=10)

scale = Scale(root, from_=0, to=100 , orient=tk.HORIZONTAL, label="Volume", bg="#333333", fg="white", command=lambda val: engine.set_volume(int(val)))
scale.pack(pady=20)
scale.set(70)

root.mainloop()