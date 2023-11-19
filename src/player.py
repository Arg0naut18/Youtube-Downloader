import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from mutagen.mp3 import MP3
import threading
import pygame
import time
import os


class Player:
    def __init__(self):
        pygame.mixer.init()

        self.current_position = 0
        self.paused = False
        self.selected_folder_path = "" # Store the selected folder path
        pt = threading.Thread(target=self.update_progress)
        pt.daemon = True
        pt.start()

    def update_progress(self):
        while True:
            if pygame.mixer.music.get_busy() and not self.paused:
                self.current_position = pygame.mixer.music.get_pos() / 1000
                pbar["value"] = self.current_position

                if self.current_position >= pbar["maximum"]:
                    self.stop_music()
                    pbar["value"] = 0
                
                window.update()
            time.sleep(0.1)

    def select_music_folder(self):
        global selected_folder_path
        selected_folder_path = filedialog.askdirectory()
        if selected_folder_path:
            lbox.delete(0, tk.END)
            for filename in os.listdir(selected_folder_path):
                if filename.endswith(".mp3"):
                    lbox.insert(tk.END, filename)

    def previous_song(self):
        if len(lbox.curselection()) > 0:
            current_index = lbox.curselection()[0]
            if current_index > 0:
                lbox.selection_clear(0, tk.END)
                lbox.selection_set(current_index - 1)
                self.play_selected_song()

    def next_song(self):
        if len(lbox.curselection()) > 0:
            current_index = lbox.curselection()[0]
            if current_index < lbox.size() - 1:
                lbox.selection_clear(0, tk.END)
                lbox.selection_set(current_index + 1)
                self.play_selected_song()


    def play_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            self.play_selected_song()

    def play_selected_song(self):
        if len(lbox.curselection()) > 0:
            current_index = lbox.curselection()[0]
            selected_song = lbox.get(current_index)
            full_path = os.path.join(selected_folder_path, selected_song)
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(start=self.current_position)
            self.paused = False
            audio = MP3(full_path)
            song_duration = audio.info.length
            pbar["maximum"] = song_duration

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.paused = False


ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')
window = ctk.CTk()
window.title("Music Player App")
window.geometry("600x500")
player = Player()

l_music_player = ctk.CTkLabel(window, text="Music Player", font=("TkDefaultFont", 30, "bold"))
l_music_player.pack(pady=10)

btn_select_folder = ctk.CTkButton(window, text="Select Music Folder",
                                  command=player.select_music_folder,
                                  font=("TkDefaultFont", 18))
btn_select_folder.pack(pady=20)

lbox = tk.Listbox(window, width=50, font=("TkDefaultFont", 16))
lbox.pack(pady=10)

btn_frame = tk.Frame(window)
btn_frame.pack(pady=20)

btn_previous = ctk.CTkButton(btn_frame, text="<", command=player.previous_song,
                            width=50, font=("TkDefaultFont", 18))
btn_previous.pack(side=tk.LEFT, padx=5)

btn_play = ctk.CTkButton(btn_frame, text="Play", command=player.play_music, width=50,
                         font=("TkDefaultFont", 18))
btn_play.pack(side=tk.LEFT, padx=5)

btn_pause = ctk.CTkButton(btn_frame, text="Pause", command=player.pause_music, width=50,
                          font=("TkDefaultFont", 18))
btn_pause.pack(side=tk.LEFT, padx=5)

btn_next = ctk.CTkButton(btn_frame, text=">", command=player.next_song, width=50,
                         font=("TkDefaultFont", 18))
btn_next.pack(side=tk.LEFT, padx=5)

pbar = ctk.CTkProgressBar(window, width=300, mode="determinate")
pbar.set(0)
pbar.pack(pady=10)

window.mainloop()