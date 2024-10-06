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
                elif tentativeTransition == 'inright':
                    transition = Move
                elif tentativeTransition == 'onright':
                    transition = MoveOnRigth
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


    backgroundManager = BackgroundManager()