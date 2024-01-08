import os
import pygame
from tkinter import Tk, Label, Button, Canvas

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        # Set dark theme
        self.root.configure(bg="#1E1E1E")
        self.label_color = "#FFFFFF"
        self.button_color = "#373737"
        self.button_text_color = "#FFFFFF"

        self.songs = []
        self.current_song_index = 0
        self.paused = False
        self.song_length = 0

        self.load_songs()
        self.init_gui()

    def load_songs(self):
        # Change this path to the directory containing your music files
        music_directory = "C:\music"

        for filename in os.listdir(music_directory):
            if filename.endswith(".mp3"):
                self.songs.append(os.path.join(music_directory, filename))

    def init_gui(self):
        self.label = Label(root, text="Now Playing:", bg="#1E1E1E", fg=self.label_color)
        self.label.pack()

        self.ascii_art_label = Label(root, text="   _____                           __   .__         \n  /  _  \  _____  _______   ____ _/  |_ |__|  ______\n /  /_\  \ \__  \ \_  __ \_/ ___\\   __\|  | /  ___/\n/    |    \ / __ \_|  | \/\  \___ |  |  |  | \___ \ \n\____|__  /(____  /|__|    \___  >|__|  |__|/____  >\n        \/      \/             \/                \/ ", bg="#1E1E1E", fg=self.label_color, font=("Courier", 12))
        self.ascii_art_label.pack()

        self.song_label = Label(root, text="", bg="#1E1E1E", fg=self.label_color)
        self.song_label.pack()

        self.time_label = Label(root, text="", bg="#1E1E1E", fg=self.label_color)
        self.time_label.pack()

        self.progress_label = Label(root, text="", bg="#1E1E1E", fg=self.label_color)
        self.progress_label.pack()

        self.progress_canvas = Canvas(root, width=200, height=20, bg="white")
        self.progress_canvas.pack()

        self.play_pause_button = Button(root, text="Play", command=self.toggle_play_pause, bg=self.button_color, fg=self.button_text_color)
        self.play_pause_button.pack()

        self.next_button = Button(root, text="Next", command=self.play_next_song, bg=self.button_color, fg=self.button_text_color)
        self.next_button.pack()

        self.previous_button = Button(root, text="Previous", command=self.play_previous_song, bg=self.button_color, fg=self.button_text_color)
        self.previous_button.pack()

        self.load_song()
        self.update_song_label()
        self.update_time_label()

    def load_song(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.songs[self.current_song_index])
        self.song_length = pygame.mixer.Sound(self.songs[self.current_song_index]).get_length()

        if not self.paused:
            pygame.mixer.music.play()
            self.paused = True
            self.toggle_play_pause()

    def update_song_label(self):
        song_name = os.path.basename(self.songs[self.current_song_index])
        self.song_label.config(text=song_name)

    def update_time_label(self):
        try:
            current_time = pygame.mixer.music.get_pos() / 1000.0
            time_str = f"Time: {int(current_time // 60)}:{int(current_time % 60):02} / {int(self.song_length // 60)}:{int(self.song_length % 60):02}"
            self.time_label.config(text=time_str)

            progress = (current_time / self.song_length) * 100
            self.progress_canvas.delete("progress")
            self.progress_canvas.create_rectangle(0, 0, progress * 2, 20, fill="black", tags="progress")

            progress_str = f"Progress: {progress:.2f}%"
            self.progress_label.config(text=progress_str)

        except pygame.error:
            pass

        # Update every second
        self.root.after(1000, self.update_time_label)

    def toggle_play_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.play_pause_button.config(text="Pause")
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_pause_button.config(text="Play")

    def play_next_song(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.load_song()
        self.update_song_label()
        if not self.paused:
            pygame.mixer.music.play()

    def play_previous_song(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.load_song()
        self.update_song_label()
        if not self.paused:
            pygame.mixer.music.play()

root = Tk()
app = MusicPlayer(root)
root.mainloop()
