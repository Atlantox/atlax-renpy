init python:    
    class DialogueGenerator:
        def __init__(self, fileName):
            self.dialogues = []
            f = open(renpy.loader.transfn("dialogues/" + fileName),"r")
            lines = f.readlines()
            f.close()

            self.headers = [s.strip() for s in lines[0].split(';')]
            print(self.headers)
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
            self.backgroundPlaced = False

        def ChangeBackground(self, bgPrompt):
            transition = Dissolve
            time = [2.0]
                
            bgSplits = bgPrompt.split(':')
            bgName = bgSplits[0]            

            if len(bgSplits) >= 2:
                tentativeTransition = bgSplits[1].lower()

                if tentativeTransition == 'dissolve':
                    transition = Dissolve
                elif tentativeTransition == 'fade':
                    transition = Fade
                    time = [1, 0.5, 1]
                elif tentativeTransition == 'pixel':
                    transition = Pixellate
                    time = [3, 18]
                elif tentativeTransition == 'push':
                    transition = PushMove
                    time = [1.5, 'pushup']
                elif tentativeTransition == 'rup':
                    transition = Swing
                    time = [1.5, True, False]
                elif tentativeTransition == 'rright':
                    transition = Swing
                    time = [1.5, False, False]
                elif tentativeTransition == 'rdown':
                    transition = Swing
                    time = [1.5, True, True]
                elif tentativeTransition == 'rleft':
                    transition = Swing
                    time = [1.5, False, True]
                else:
                    transition = Dissolve
            
            if len(bgSplits) == 3:
                params = [float(p.strip()) for p in bgSplits[2].split(',') if p != '']
                time = params


            renpy.scene()      

            commandString = 'bg ' + bgName 
            renpy.show(commandString)

            if not self.backgroundPlaced:
                self.backgroundPlaced = True
            else:
                renpy.transition(transition(*time))


    class AudioManager:
        def PlayMusic(self, musicData):
            splittedMusic = musicData.split(':')

            fileName = 'music/{0}.wav'.format(splittedMusic[0])
            fadein = 3

            if len(splittedMusic) == 2:
                fadein = float(splittedMusic[1])

            if splittedMusic[0] == '*':
                renpy.music.stop(channel='music', fadeout=fadein)
            else:
                renpy.music.play(fileName, channel='music', fadein=fadein)

        def PlaySound(self, soundData):
            fileName = 'sounds/{0}.wav'.format(soundData)
            renpy.music.play(fileName, channel='sound')


    class EffectManager:       
        continuousEffect = None
        duringEffect = False

        def ProcessEffect(self, effectData):
            splits = effectData.split(':')

            if splits[0] in ['vertical', 'horizontal']:
                self.ShakeData(splits)
            elif splits[0] in ['blur']:
                self.ProcessContinuousEffect(splits)
                

        def ScreenShake(self, shakeData):
            intensity = 20

            if len(shakeData) >= 2:
                intensity = int(shakeData[1])

            print(intensity * -1)
            if shakeData[0] == 'vertical':
                myTransition = Move((0, intensity), (0, intensity * -1), .10, bounce=True, repeat=True, delay=.275)
                
            if shakeData[0] == 'horizontal':
                myTransition = Move((intensity, 0), (intensity * -1, 0), .10, bounce=True, repeat=True, delay=.275)

            renpy.transition(myTransition)

        
        def ProcessContinuousEffect(self, blurData):
            effectName = blurData[0]

            # If another effect it's in progress, ignore the effect
            if(self.duringEffect is True) and (self.continuousEffect != effectName):
                return

            # Probar una especie de cambio de fondo con el blur aplicado y transición
            blurIntensity = 10
            duration = 1

            if effectName == 'blur':
                renpy.with_statement(Dissolve(duration))
                if self.duringEffect:
                    renpy.layer_at_list("master", [])
                    self.duringEffect = False
                else:
                    renpy.layer_at_list("master", [Transform(blur=blurIntensity)])                
                    self.duringEffect = True
    
    
    backgroundManager = BackgroundManager()
    audioManager = AudioManager()
    effectManager = EffectManager()