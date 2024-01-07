import os
import pygame

class RetroMusicPlayer:
    def __init__(self):
        self.songs = []
        self.current_song = 0
        self.paused_position = 0

        pygame.mixer.init()

        self.load_songs()

    def load_songs(self):
        music_directory = "C:\music"

        for filename in os.listdir(music_directory):
            if filename.endswith(".mp3"):
                self.songs.append(os.path.join(music_directory, filename))

    def play_song(self):
        pygame.mixer.music.load(self.songs[self.current_song])
        pygame.mixer.music.play(start=self.paused_position)

    def pause_song(self):
        pygame.mixer.music.pause()
        self.paused_position = pygame.mixer.music.get_pos()

    def resume_song(self):
        pygame.mixer.music.unpause()

    def stop_song(self):
        pygame.mixer.music.stop()

    def run(self):
        while True:
            print("Retro Music Player")
            print("1. Play/Pause")
            print("2. Next Song")
            print("3. Previous Song")
            print("4. Quit")

            choice = input("Select an option (1-4): ")

            if choice == '1':
                if pygame.mixer.music.get_busy():
                    self.pause_song()
                else:
                    self.resume_song()
            elif choice == '2':
                self.current_song = (self.current_song + 1) % len(self.songs)
                self.stop_song()
                self.play_song()
            elif choice == '3':
                self.current_song = (self.current_song - 1) % len(self.songs)
                self.stop_song()
                self.play_song()
            elif choice == '4':
                break

if __name__ == "__main__":
    player = RetroMusicPlayer()
    player.run()
