init python:
    class AudioManager:
        def __init__(self):
            self.baseMusicPath = 'music/{0}.wav'
            self.baseSoundPath = 'sounds/{0}.wav'
            self.prepared = False
            self.defaultFadeIn = 3.0

            self.currentMusicName = None
            self.oneTimeSoundsQueue = []
            self.loopedSoundsQueue = []
            self.currentLoopedSounds = []
            self.currentFadeIn = None
            self.musicPrepared = False
            self.soundPrepared = False

        def PrepareMusic(self,musicPrompt):
            self.prepared = True
            self.musicPrepared = True
            fadein = self.defaultFadeIn

            promptSplits = musicPrompt.split(':')
            musicName = promptSplits[0]

            if len(promptSplits) == 2:
                fadein = float(promptSplits[1])

            self.currentMusicName = musicName
            self.currentFadeIn = fadein

        def PrepareSound(self, soundPrompt):
            self.prepared = True
            self.soundPrepared = True

            recievedSounds = [r.strip() for r in soundPrompt.split(',')]

            for sound in recievedSounds:
                splittedSound = [s.strip() for s in sound.split(':')]
                soundName = splittedSound[0].replace('_', ' ')
                looped = False

                if len(splittedSound) > 1:
                    if splittedSound[1] == 'loop': looped = True

                if looped:
                    self.loopedSoundsQueue.append(soundName)
                else:
                    self.oneTimeSoundsQueue.append(self.baseSoundPath.format(soundName))

        def HandleSFX(self):
            self.prepared = False

            if self.musicPrepared:
                self.musicPrepared = False
                self.PlayMusic()

            if self.soundPrepared:
                self.soundPrepared = False
                self.PlaySound()

        def PlayMusic(self):                 
            if self.currentMusicName == '*':
                renpy.music.stop(channel='music', fadeout=self.currentFadeIn)
            else:
                renpy.music.play(self.baseMusicPath.format(self.currentMusicName), channel='music', fadein=self.currentFadeIn)

        def PlaySound(self):
            if len(self.oneTimeSoundsQueue) > 0:
                renpy.music.play(self.oneTimeSoundsQueue, channel='sound')
                if len(self.currentLoopedSounds) > 0:
                    # If a sound are looped and play a single sound, all loops break, so restart the looped sound list
                    self.currentLoopedSounds = []

            toPlaySounds = []
            toStopSounds = []
            # TODO: sacar de la lista de sonidos en loop cuando se reproduce un sonido nuevo

            for sound in self.loopedSoundsQueue:

                if sound in self.currentLoopedSounds:
                    toStopSounds.append(self.baseSoundPath.format(sound))
                    soundIdx = self.currentLoopedSounds.index(sound)
                    del self.currentLoopedSounds[soundIdx]
                else:
                    toPlaySounds.append(self.baseSoundPath.format(sound))
                    self.currentLoopedSounds.append(sound)

            if len(toPlaySounds) > 0: renpy.music.play(toPlaySounds, channel='sound', loop=True)
            if len(toStopSounds) > 0: renpy.music.stop(channel='sound')

            self.oneTimeSoundsQueue = []
            self.loopedSoundsQueue = []