init python:
    class DialogueManager:
        def __init__(self, fileName):
            self.minHeaderCount = 10
            self.rawDialogues = []
            self.dialogues = []
            self.currentDialogue = -1
            self.terminateData = []
            self.terminateMethod = ''
            self.admittedTerminateMethods = ['decision', 'fork', 'end']

            self.currentFile = fileName
            self.LoadDialogue()


        def LoadDialogue(self):
            with open(renpy.loader.transfn("dialogues/" + self.currentFile + '.csv'), mode="r", encoding='utf-8') as f:
                lines = f.readlines()
                f.close()

            self.headers = [s.strip().replace('\ufeff', '') for s in lines[0].split(';')]
            self.rawDialogues = lines[1:] # Ignoramos la primera fila que es la leyenda

        def PrepareDialogues(self):
            dialogueFinished = False
            for dialogue in self.rawDialogues:
                splittedDialogue = [d.strip() for d in dialogue.split(';')]
                result = dict()

                if splittedDialogue[0][0] == '#':
                    dialogueFinished = True
                    method = splittedDialogue[1:]
                    if method not in self.admittedTerminateMethods:
                        raise Exception(f'El método de terminación {method} no existe, los que se admiten son: ' + str(self.admittedTerminateMethods))

                    self.terminateMethod = method
                    continue

                if dialogueFinished:                    
                    self.ProcessTerminationMethod(splittedDialogue)                

                if len(splittedDialogue) < self.minHeaderCount:
                    error = 'El diálogo {0} no cumple con el mínimo número de columnas'.format(splittedDialogue[0])
                    raise ZeroDivisionError(error)

                headerIdx = 0
                for header in self.headers:
                    result[header] = splittedDialogue[headerIdx].strip()
                    headerIdx += 1
                    
                self.dialogues.append(result)

        def ProcessTerminationMethod(self, terminateSplits):
            if self.terminateMethod.lower() == 'decision':

                to_add = {
                    'key': splittedDialogue[0],
                    'name': splittedDialogue[1],
                    'nextDialogue': splittedDialogue[3],
                    'points': {}
                }

                if splittedDialogue[2] != '':
                    points = [s.strip() for s in splittedDialogue[2].split(',')]
                    for point in points:
                        pointSplits = point.split(':')
                        pointType = pointSplits[0]
                        pointValue = int(pointSplits[1])
                        to_add['points'][pointType] = pointValue
                        
                self.terminateData

        def GetNextDialogue(self):
            self.currentDialogue += 1
            return self.dialogues[self.currentDialogue]            