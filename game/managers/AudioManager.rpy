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
            self.soundChannels = {}

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
                for sound in self.oneTimeSoundsQueue:
                    channelName = self.GetNextChannel()
                    renpy.music.play(sound, channel=channelName, synchro_start=True, loop=False)

            toPlaySounds = []
            toStopSounds = []

            for sound in self.loopedSoundsQueue:
                if sound in self.currentLoopedSounds:
                    toStopSounds.append(self.soundChannels[sound])
                    soundIdx = self.currentLoopedSounds.index(sound)
                    del self.currentLoopedSounds[soundIdx]      
                    del self.soundChannels[sound]              
                else:
                    channelName = self.GetNextChannel()
                    self.soundChannels[sound] = channelName
                    toPlaySounds.append({'name': sound, 'channel': channelName})
                    self.currentLoopedSounds.append(sound)

            if len(toPlaySounds) > 0: 
                for sound in toPlaySounds:
                    renpy.music.play(self.baseSoundPath.format(sound['name']), channel=sound['channel'], loop=True)

            if len(toStopSounds) > 0: 
                for sound in toStopSounds:
                    renpy.music.stop(channel=sound)

            self.oneTimeSoundsQueue = []
            self.loopedSoundsQueue = []

        def GetNextChannel(self):
            result = 'sfx1'

            for idx in range(1, configManager.simultaneousSounds + 1):
                channelName = 'sfx{0}'.format(idx)
                if(channelName in self.soundChannels.values()):
                    continue
                else:
                    result = channelName
                    break

            return result