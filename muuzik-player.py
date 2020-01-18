class MuuzikPlayer:
    def __init__(self, config):
        self.text_to_translate = None
        self.language = None
        try:
            self.pathToMusic = config['secret']['pathToMusic']
        except KeyError:
            self.pathToMusic = "/home"

    def play(self, hermes, intent_message):

        if intent_message.slots.Artist:
            search = intent_message.slots.Artist



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
                    result = genre.find('Breakbeat')
                    print(genre)
                    if result > -1:
                        print(artist)
                        playlist.append(os.path.join(root, filename))
        #                if startFirstSongOnce:
                            #pygame.mixer.init()
                            #pygame.mixer.music.load(os.path.join(root, filename))
                            #pygame.mixer.music.play()
                            #startFirstSongOnce = False
                except:
                    print('errpr')

        tracks_number = len(playlist)
        current_track = 0
        print(playlist)
        # start first track
        pygame.mixer.init(frequency = 48000)
        screen = pygame.display.set_mode((400, 300))
        pygame.mixer.music.load(playlist[current_track])
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

                    print("Play:", playlist[current_track])

                    pygame.mixer.music.load(playlist[current_track])
                    pygame.mixer.music.play()


        pygame.quit()
