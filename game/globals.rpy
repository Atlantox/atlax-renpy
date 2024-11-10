init python:    
    class DialogueGenerator:
        def __init__(self, fileName):
            self.dialogues = []
            f = open(renpy.loader.transfn("dialogues/" + fileName),"r")
            lines = f.readlines()
            f.close()

            self.headers = [s.strip() for s in lines[0].split(';')]

            self.dialogues = lines[1:] # Ignoramos la primera fila que es la leyenda
            f.close()
            self.generator = self.getNextDialogue()

        def getNextDialogue(self):
            for dialogue in self.dialogues:
                splittedDialogue = dialogue.split(';')
                result = dict()
                if len(splittedDialogue) != len(self.headers):
                    raise ZeroDivisionError('El diálogo {0} tiene distintas columnas que la cabecera'.format(splittedDialogue[0]))

                headerIdx = 0
                for header in self.headers:
                    result[header] = splittedDialogue[headerIdx].strip()
                    headerIdx += 1
                    
                yield result

    
    class BackgroundManager:
        def __init__(self):
            self.baseBgPath = 'images/backgrounds/'
            self.defaultTransition = Dissolve
            self.defaultDuration = 2.0

            self.prepared = False

            self.backgroundPlaced = False

            self.targetTransition = None
            self.currentBgPath = None
            self.currentBgName = None
            self.params = None
            self.transformsToApply = {}

            self.postHandleEvents = []
            self.postHandleParams = []

        def PrepareBackground(self, bgPrompt):
            self.prepared = True
            currentTransition = self.defaultTransition
            params = [self.defaultDuration]
                
            promptSplits = bgPrompt.split(':')
            bgName = promptSplits[0]            

            if len(promptSplits) >= 2:
                recievedTransition = promptSplits[1].lower()

                if recievedTransition == 'fade':
                    currentTransition = Fade
                    params = [1, 0.5, 1]
                elif recievedTransition == 'pixel':
                    currentTransition = Pixellate
                    params = [3, 18]
                elif recievedTransition == 'push':
                    currentTransition = PushMove
                    params = [1.5, 'pushup']
                elif recievedTransition == 'rup':
                    currentTransition = Swing
                    params = [1.5, True, False]
                elif recievedTransition == 'rright':
                    currentTransition = Swing
                    params = [1.5, False, False]
                elif recievedTransition == 'rdown':
                    currentTransition = Swing
                    params = [1.5, True, True]
                elif recievedTransition == 'rleft':
                    currentTransition = Swing
                    params = [1.5, False, True]
            
            if len(promptSplits) == 3:
                params = [float(s.strip()) for s in promptSplits[2].split(',') if s != '']


            backgroundPath = self.baseBgPath + f'{bgName}.png'

            self.currentBgPath = backgroundPath
            self.currentBgName = bgName
            self.targetTransition = currentTransition
            self.params = params

        def HandleBackground(self):
            self.prepared = False
            renpy.scene()
            commandString = 'bg ' + self.currentBgName

            transforms = []
            for ker, value in self.transformsToApply.items():
                transforms.append(value)

            renpy.show(commandString, transforms)

            if not self.backgroundPlaced: # Placing the background without transition             
                self.backgroundPlaced = True
            else:
                renpy.transition(self.targetTransition(*self.params))
                currentTransition = self.defaultTransition
                params = [self.defaultDuration]

        def HandlePostEventsEffects(self):
            print('Ejeutando eventos post realización')
            for i in range(len(self.postHandleEvents)):
                # Calling functions with corresponded params
                print(i)
                self.postHandleEvents[i](*self.postHandleParams[i])

            self.postHandleEvents = []
            self.postHandleParams = []


    class AudioManager:
        def __init__(self):
            self.prepared = False
            self.defaultFadeIn = 3.0

            self.currentMusicName = None
            self.currentMusicPath = None
            self.currentSoundPath = None
            self.currentFadeIn = None
            self.musicChanged = False
            self.soundChanged = False

        def PrepareMusic(self,musicPrompt):
            self.prepared = True
            self.musicChanged = True
            fadein = self.defaultFadeIn

            promptSplits = musicPrompt.split(':')
            musicName = promptSplits[0]

            if len(promptSplits) == 2:
                fadein = float(promptSplits[1])

            self.currentMusicPath = f'music/{musicName}.wav'
            self.currentMusicName = musicName
            self.currentFadeIn = fadein

        def PrepareSound(self, soundPrompt):
            self.prepared = True
            self.soundChanged = True
            self.currentSoundPath = 'sounds/{0}.wav'.format(soundPrompt)

        def HandleSFX(self):
            self.prepared = False

            if self.musicChanged:
                self.musicChanged = False
                self.PlayMusic()

            if self.soundChanged:
                self.soundChanged = False
                self.PlaySound()

        def PlayMusic(self):                 
            if self.currentMusicName == '*':
                renpy.music.stop(channel='music', fadeout=self.currentFadeIn)
            else:
                renpy.music.play(self.currentMusicPath, channel='music', fadein=self.currentFadeIn)

        def PlaySound(self):
            renpy.music.play(self.currentSoundPath, channel='sound')


    class EffectManager:
        def __init__(self):
            self.prepared = False
            self.availableContinuousEffects = ['blur', 'rotate', 'hwarp', 'vwarp'] # Suffocation
            self.availableSingleEffects = ['vpunch', 'hpunch', 'flash', 'blackout']  # Centelleo, Apagón

            self.defaultShakeIntensity = 20
            self.defaultBlurIntensity = 15.0
            self.defaultRotationDegrees = 45
            self.defaultWarp = 1.1
            self.defaultSingleEffetDuration = 0.1
            self.defaultBlinkTimes = 4

            self.continuousEffectQueue = []
            self.effectQueue = []

            self.currentContinuousEffects = []

        def PrepareEffects(self, effectPrompt):
            self.prepared = True
            promptSplits = [e.strip() for e in effectPrompt.split(',')]
            for effect in promptSplits: # Iterating between the effects
                effectSplits = [e.strip() for e in effect.split(':')]
                effectName = effectSplits[0]

                if effectName in self.availableContinuousEffects:
                    self.PrepareContinuousEffect(effectSplits)   
                else:
                    if effectName in self.availableSingleEffects:
                        self.PrepareSingleEffect(effectSplits)
                    else: # Maybe it's a background flashing
                        exists = renpy.exists(backgroundManager.baseBgPath + effectName + '.png')
                        self.PrepareSuddenImage(effectSplits, exists)

        def PrepareSingleEffect(self, effectSplits):
            if effectSplits[0] in ['vpunch', 'hpunch']:
                self.PrepareShake(effectSplits)
            elif effectSplits[0] in ['flash', 'blackout']:
                self.PrepareSuddenImage(effectSplits)

        def PrepareShake(self, shakeSplits):
            intensity = self.defaultShakeIntensity

            if len(shakeSplits) >= 2:
                intensity = int(shakeSplits[1])

            if shakeSplits[0] == 'vpunch':
                shakeTransition = Move((0, intensity), (0, intensity * -1), .10, bounce=True, repeat=True, delay=.275)
                
            if shakeSplits[0] == 'hpunch':
                shakeTransition = Move((intensity, 0), (intensity * -1, 0), .10, bounce=True, repeat=True, delay=.275)

            self.effectQueue.append(shakeTransition)
        
        def PrepareContinuousEffect(self, effectSplits):
            effectName = effectSplits[0]            

            if effectName in self.availableContinuousEffects:  # Effects that depends of the current background
                self.PrepareBackgroundTransform(effectSplits)
            elif effectName in ['suffocation']:  # Effects that displays an image on the current background
                # TODO: effects that displays a PNG over the current background
                pass

        def PrepareBackgroundTransform(self, effectSplits):
            effectName = effectSplits[0]
            backgroundManager.prepared = True

            if effectName in self.currentContinuousEffects:  # The effect it's in progress, then stop it
                effectIdx = self.currentContinuousEffects.index(effectName)
                del self.currentContinuousEffects[effectIdx]
                del backgroundManager.transformsToApply[effectName]
            else: # The effect isn't in progress, then prepare it
                self.currentContinuousEffects.append(effectName)
                recievedParam = len(effectSplits) > 1  # A param was recieved

                if effectName == 'blur':
                    intensity = float(effectSplits[1]) if recievedParam else self.defaultBlurIntensity
                    targetEffect = Transform(blur=intensity)
                elif effectName == 'rotate':
                    degrees = float(effectSplits[1]) if recievedParam else self.defaultRotationDegrees
                    targetEffect = Transform(rotate=degrees, rotate_pad=False, transform_anchor=True)
                elif effectName in ['hwarp', 'vwarp']:
                    factor = float(effectSplits[1]) if recievedParam else self.defaultWarp
                    if effectName == 'hwarp':                        
                        targetEffect = Transform(xsize=factor)
                    else:
                        targetEffect = Transform(ysize=factor)
                else:
                    return

                backgroundManager.transformsToApply[effectSplits[0]] = targetEffect

        def PrepareSuddenImage(self, effectSplits, imageExists = True):
            if imageExists is False: return
            effectName = effectSplits[0]
            duration = self.defaultSingleEffetDuration
            times = self.defaultBlinkTimes

            if len(effectSplits) > 1:
                duration = float(effectSplits[1])

            if len(effectSplits) > 2:
                times = int(effectSplits[2])

            imageToShow = 'bg ' + effectName
            

            # Building the function to pass to the backgroundManager
            def BlinkImage(imageToShow, times, duration):
                for _ in range(times):
                    renpy.show(imageToShow, [Transform(alpha=1.0)])
                    renpy.pause(duration)
                    #renpy.show(imageToShow, [Transform(alpha=0.0)])
                    renpy.show('bg ' + backgroundManager.currentBgName)
                    renpy.pause(duration)

            
            backgroundManager.postHandleEvents.append(BlinkImage)
            backgroundManager.postHandleParams.append([imageToShow, times, duration])

        def HandleEffects(self):
            self.prepared = False
            if len(self.effectQueue) > 0:
                for e in self.effectQueue:
                    renpy.transition(e)
                self.effectQueue = []

            if len(self.continuousEffectQueue) > 0:
                pass


    backgroundManager = BackgroundManager()
    audioManager = AudioManager()
    effectManager = EffectManager()