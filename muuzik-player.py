import sys
import fnmatch
from tinytag import TinyTag
import subprocess
import os
#from pygame import mixer
import pygame
NEXT = pygame.USEREVENT + 1
os.environ["SDL_VIDEODRIVER"] = "dummy"


class MuuzikPlayer:
    def __init__(self, config):
        self.text_to_translate = None
        self.language = None
        self.pattern = '*.mp3'
        self.playlist = []
        self.startFirstSongOnce = True

        try:
            self.pathToMusic = config['secret']['pathToMusic']
        except KeyError:
            self.pathToMusic = "/home"

    def play(self, hermes, intent_message):
        self.playlist = []

        if intent_message.slots.Artist:
            search = intent_message.slots.Artist
        if intent_message.slots.Album:
            search = intent_message.slots.Album


        print('play Musik')
        for root, dirs, files in os.walk(self.pathToMusic):
            for filename in fnmatch.filter(files, pattern):
                try:
                    audiofile = TinyTag.get(os.path.join(root, filename))
                    album = str(audiofile.album)
                    titel = str(audiofile.title)
                    genre = str(audiofile.genre)
                    albumArtist = str(audiofile.albumartist)
                    artist = str(audiofile.artist)
                    year = str(audiofile.year)

                    if intent_message.slots.Artist:
                        result = artist.find(intent_message.slots.Artist)
                    if intent_message.slots.Album:
                        result = album.find(intent_message.slots.Album)
                    if intent_message.slots.Title:
                        result = titel.find(intent_message.slots.Title)
                    if intent_message.slots.Genre:
                        result = genre.find(intent_message.slots.Genre)
                    #result = genre.find('Breakbeat')

                    if result > -1:
                        print(artist)
                        self.playlist.append(os.path.join(root, filename))
                except:
                    print('errpr')

        tracks_number = len(self.playlist)
        current_track = 0
        print(self.playlist)
        # start first track
        pygame.mixer.init(frequency = 48000)
        screen = pygame.display.set_mode((400, 300))
        pygame.mixer.music.load(self.playlist[current_track])
        pygame.mixer.music.set_volume(5.0)
        pygame.mixer.music.play()

        pygame.mixer.music.set_endevent(NEXT)

        running = True

        if pygame.mixer.get_busy() != None:
            print('test')

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == NEXT:

                    # get next track (modulo number of tracks)
                    current_track = (current_track + 1) % tracks_number

                    print("Play:", self.playlist[current_track])

                    pygame.mixer.music.load(self.playlist[current_track])
                    pygame.mixer.music.play()


        pygame.quit()
