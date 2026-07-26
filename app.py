from RadioEngine import Engine
import tkinter as tk

root = tk.Tk()
root.title("Radio Engine V1.0")

engine = Engine()

button = tk.Button(root, text="Listen to a station by entering a tag", command=lambda: print(engine.play_station(engine.search_stations_by_tag(input("Enter a tag: "), 5)[0]["url_resolved"])))
button.pack()

button2 = tk.Button(root, text="Listen to a station by entering a name", width=20, command=lambda: print(engine.radio_search_by_name_and_play(entry.get(), 5)))
button2.pack()

entry = tk.Entry(root, width=20)
entry.pack()





root.mainloop()