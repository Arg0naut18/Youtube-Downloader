import tkinter as tk
import customtkinter as ctk
from pytube import YouTube
import os


class YTDownloader:
    def __init__(self):
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('src/theme.json')
        self.app = ctk.CTk()
        self.app.geometry('720x480')
        self.app.title("Youtube Downloader")
        self.app.wm_iconbitmap("src\images\logo.ico")

        self.title = ctk.CTkLabel(self.app, text="Insert youtube video link")
        self.title.pack(padx=10, pady=20)

        self.vid_url = tk.StringVar(self.app)
        self.link = ctk.CTkEntry(self.app, width=350, height=40, textvariable=self.vid_url)
        self.link.pack()

        self.type = ctk.CTkComboBox(self.app, values=['Video', 'Audio'], command=self.show_download_button)
        self.type.set('Video')
        self.type.pack(padx=10, pady=10)

        self.path_label = ctk.CTkLabel(self.app, text="Select Location to download")
        self.path_label.pack(padx=10, pady=10)

        self.download_path = tk.StringVar(self.app, value=os.getcwd())
        self.path = ctk.CTkEntry(self.app, width=300, height=40, textvariable=self.download_path, placeholder_text=os.getcwd())
        self.path.pack()

        self.path_button = ctk.CTkButton(self.app, text="Select", command=self.get_directory)
        self.path_button.pack(padx=10, pady=10)

        self.download = ctk.CTkButton(self.app, text="Download", command=self.start_video_download)
        self.download.pack(padx=10, pady=10)

        self.dwnld_percentage = ctk.CTkLabel(self.app, text="0%")
        self.dwnld_percentage.pack()
        self.progress_bar = ctk.CTkProgressBar(self.app, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=10, pady=10)

        self.finish_download = ctk.CTkLabel(self.app, text="")
        self.finish_download.pack()

    def __call__(self):
        self.app.mainloop()

    def get_directory(self):
        filepath = ctk.filedialog.askdirectory(
            initialdir=r"/", title="Dialog box"
        )
        self.path.configure(placeholder_text=filepath)
        self.download_path.set(filepath)

    def show_download_button(self, choice):
        if choice=='Audio':
            self.download.configure(command=self.start_audio_download)
        else:
            self.download.configure(command=self.start_video_download)

    def start_video_download(self):
        try:
            self.finish_download.configure(text="")
            yt_link = self.vid_url.get()
            yt_object = YouTube(yt_link, on_progress_callback=self.on_progress)
            file = yt_object.streams.get_highest_resolution()
            file.download(output_path=self.download_path.get())
        except Exception as e:
            self.finish_download.configure(text="Error Downloading!", text_color='red')
            print(e)
        else:
            self.finish_download.configure(text="Download Complete!", text_color='green')

    def start_audio_download(self):
        try:
            self.finish_download.configure(text="")
            yt_link = self.vid_url.get()
            yt_object = YouTube(yt_link, on_progress_callback=self.on_progress)
            file = yt_object.streams.get_audio_only()
            file.download(output_path=self.download_path.get())
        except Exception as e:
            self.finish_download.configure(text="Error Downloading!", text_color='red')
            print(e)
        else:
            self.finish_download.configure(text="Download Complete!", text_color='green')

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        completion_percentage = bytes_downloaded/total_size
        self.dwnld_percentage.configure(text=f"{int(completion_percentage)*100}%")
        self.progress_bar.set(completion_percentage)


if __name__ == "__main__":
    app = YTDownloader()
    app()
