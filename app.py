from RadioEngine import Engine
import tkinter as tk
from tkinter import Scale, StringVar

root = tk.Tk()
root.title("Radio Engine V1.0")

status_text = StringVar()
status_text.set("No station playing")

engine = Engine()

root.geometry("400x200")

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

tk.Label(root, text="Retro Radio", font=("Helvetica", 16), bg="#121212", fg="white").pack(pady=20)

tk.Label(root, textvariable=status_text, bg="#121212", fg="white").pack()

entry = tk.Entry(root, width=20, bg="#333333", fg="white", insertbackground="white")
entry.pack(pady=10)

button = tk.Button(root, text="Listen to a station by entering a tag", width=35, bg="#333333", fg="white", command=search_and_play_by_tag)
button.pack()

button2 = tk.Button(root, text="Listen to a station by entering a name", width=35, bg="#333333", fg="white", command=search_and_play_by_name)
button2.pack()

scale = Scale(root, from_=0, to=100 , orient=tk.HORIZONTAL, label="Volume", bg="#333333", fg="white", command=lambda val: engine.set_volume(int(val)))
scale.pack(pady=20)


root.mainloop()