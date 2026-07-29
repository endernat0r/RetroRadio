import customtkinter as ctk
import tkinter as tk
from tkinter import StringVar # Hata vermemesi için bu satır eklendi
from RadioEngine import Engine
import ui_helpers
import ctypes

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Radio Engine V1.0")

def on_close():
    root.withdraw()

root.protocol("WM_DELETE_WINDOW", on_close)

status_text = StringVar()
status_text.set("No station playing")

engine = Engine()

ui_helpers.init_tray(root, engine, status_text)

root.geometry("350x480")
root.resizable(False, False)

TRANSPARENT_COLOR = "#000001"

root.configure(fg_color=TRANSPARENT_COLOR)
root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)

root.overrideredirect(True)

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")

root.bind("<ButtonPress-1>", start_move)
root.bind("<B1-Motion>", do_move)

def force_taskbar_icon():
    try:
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, (style & ~0x00000080) | 0x00040000)
        root.withdraw()
        root.deiconify()
    except:
        pass

root.after(10, force_taskbar_icon)

ui_helpers.marquee_text = "No station playing"
root.after(250, lambda: ui_helpers.start_marquee(root, status_text))

volume_button = ctk.CTkButton(root, text="🔊", font=("Helvetica", 12), width=30, height=30, fg_color="#333333", text_color="white", command=lambda: ui_helpers.open_volume_control(root, engine))
volume_button.place(relx=1.0, rely=0.0, x=-70, y=10, anchor="ne")

ctk.CTkLabel(root, text="Retro Radio", font=("Helvetica", 20, "bold"), text_color="white").pack(pady=(20, 10))

ctk.CTkLabel(root, text="", font=("Courier", 12), border_width=2, border_color="#00ff66", fg_color="#0a2211", text_color="#00ff66", textvariable=status_text, corner_radius=6).pack(ipadx=20, ipady=10, pady=10)

entry = ctk.CTkEntry(root, width=200, text_color="white", placeholder_text="Enter search query")
entry.pack(pady=10)

listBox = tk.Listbox(root, width=32, height=7, fg="#00ff66", bg="#1a1a1a", font=("Courier", 13, "bold"), borderwidth=1, highlightthickness=1, highlightcolor="#00ff66", highlightbackground="#333333")
listBox.pack(pady=10)
listBox.bind("<<ListboxSelect>>", lambda event: ui_helpers.play_selected(event, listBox, engine, status_text))

button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=5)

backButton = ctk.CTkButton(button_frame, text="<< Back", width=100, fg_color="#333333", text_color="white", command=lambda: ui_helpers.load_page(ui_helpers.current_page - 1, listBox, backButton, forwardButton, engine))
backButton.pack(side=ctk.LEFT, padx=5)

forwardButton = ctk.CTkButton(button_frame, text="Forward >>", width=100, fg_color="#333333", text_color="white", command=lambda: ui_helpers.load_page(ui_helpers.current_page + 1, listBox, backButton, forwardButton, engine))
forwardButton.pack(side=ctk.RIGHT, padx=5)

button = ctk.CTkButton(root, text="Search stations by tag", width=210, fg_color="#333333", text_color="white", command=lambda: ui_helpers.search_by_tag(entry, listBox, backButton, forwardButton, engine))
button.pack(pady=3)

button2 = ctk.CTkButton(root, text="Search stations by name", width=210, fg_color="#333333", text_color="white", command=lambda: ui_helpers.search_by_name(entry, listBox, backButton, forwardButton, engine))
button2.pack(pady=3)

button_frame2 = ctk.CTkFrame(root, fg_color="transparent")
button_frame2.pack(pady=10)

stopButton = ctk.CTkButton(button_frame2, text="Stop", width=90, fg_color="#333333", text_color="white", command=engine.stop_station)
stopButton.pack(side=ctk.LEFT, padx=5)

resumeButton = ctk.CTkButton(button_frame2, text="Resume", width=90, fg_color="#333333", text_color="white", command=lambda: engine.play_station(engine.player.get_media().get_mrl()) if engine.player else None)
resumeButton.pack(side=ctk.LEFT, padx=5)

root.mainloop()