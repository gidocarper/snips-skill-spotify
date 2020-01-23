#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from hermes_python.hermes import Hermes, MqttOptions
import sys
import fnmatch
from tinytag import TinyTag
import subprocess
import os
import os.path
from os import path
import json

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
        self.current_track = 0
        self.running = False
        pygame.mixer.init(frequency = 48000)

        self.pathToMusic = '/var/lib/snips/skills/snips-skill-spotify/Music'
        self.musicFile = []

    def play(self, hermes, intent_message):
        self.playlist = []

        if intent_message.slots.Artist:
            search = intent_message.slots.Artist
        if intent_message.slots.Album:
            search = intent_message.slots.Album

        if not str(path.exists('/var/lib/snips/skills/snips-skill-spotify/Music/db/musicFound.json')):
            print('play Musik')
            songlist = []
            for root, dirs, files in os.walk(rootPath):
                for filename in fnmatch.filter(files, pattern):
                    try:
                        audiofile = TinyTag.get(os.path.join(root, filename))
                        album = str(audiofile.album)
                        title = str(audiofile.title)
                        genre = str(audiofile.genre)
                        albumArtist = str(audiofile.albumartist)
                        artist = str(audiofile.artist)
                        year = str(audiofile.year)

                        songlist.append({
                            'song': '{} {} {} {}  {} {}  {} '.format(album, title, genre, albumArtist, artist, year,
                                                                     os.path.join(root, filename)),
                            'path': os.path.join(root, filename)
                        })

                    except:
                        print('error')

            with open('/var/lib/snips/skills/snips-skill-spotify/db/musicFound.json', 'w') as f:
                json.dump(songlist, f, indent=4)

        if len(self.musicFile) == 0:
            musicFile = open('/var/lib/snips/skills/snips-skill-spotify/db/musicFound.json')
            self.musicFile = json.load(musicFile)
            musicFile.close()

        print(self.musicFile[0])

        i = 0
        while i < len(self.musicFile):
            path = self.musicFile[i]['path']
            song = self.musicFile[i]['song']
            i += 1

            if song.find(str(intent_message.slots.Artist.first().value)) > 0 \
                    or song.find(intent_message.slots.Album.first().value) > 0 \
                    or song.find(intent_message.slots.Title.first().value) > 0 \
                    or song.find(intent_message.slots.Genre.first().value) > 0:
                playlist.append(path)

            #if len(self.playlist) > 50:
            #    break

        tracks_number = len(self.playlist)
        self.current_track = 0
        self.playSong()
        print(output)
        return output

    def next(self, hermes, intent_message):
        print('next')
        pygame.mixer.music.set_endevent(NEXT)
        self.current_track += 1
        self.playSong()

    def previous(self, hermes, intent_message):
        print('previous')
        self.current_track -= 1
        self.playSong()

    def repeat(self, hermes, intent_message):
        print('repeat')
        self.playSong()

    def stop(self, hermes, intent_message):
        print('stop')
        pygame.mixer.music.stop()
        pygame.mixer.set_endevent(type)

#        pygame.quit()

    def pause(self, hermes, intent_message):
        print('pause')
        pygame.mixer.music.pause()
        pygame.mixer.set_endevent(type)


    def playSong(self):
        # print(self.playlist)
        # start first track
        #self.playlist = ['/var/lib/snips/skills/snips-skill-spotify/Music/11_house/09_Unknown/Track07.mp3', '/var/lib/snips/skills/snips-skill-spotify/Music/11_house/09_Unknown/Track05.mp3', '/var/lib/snips/skills/snips-skill-spotify/Music/11_house/09_Unknown/Track06.mp3', '/var/lib/snips/skills/snips-skill-spotify/Music/11_house/09_Unknown/Track03.mp3', '/var/lib/snips/skills/snips-skill-spotify/Music/11_house/09_Unknown/Track08.mp3']
        self.tracks_number = len(self.playlist)
        #pygame.mixer.init(frequency = 48000)
        screen = pygame.display.set_mode((400, 300))
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.set_volume(5.0)
        pygame.mixer.music.play()
        print(self.playlist)

        pygame.mixer.music.set_endevent(NEXT)

        self.running = True

        if pygame.mixer.get_busy() != None:
            print('test')

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == NEXT:

                    # get next track (modulo number of tracks)
                    self.current_track = (self.current_track + 1) % self.tracks_number

                    print("Play:", self.playlist[self.current_track])

                    pygame.mixer.music.load(self.playlist[self.current_track])
                    pygame.mixer.music.play()

        #pygame.quit()
