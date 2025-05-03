init python:
    class DialogueManager:
        def __init__(self, fileName):        
            self.ResetDialogueManager()

            self.minHeaderCount = 10
            self.admittedTerminateMethods = ['decision', 'fork', 'end']

            self.currentFile = fileName
            self.LoadDialogue()


        def LoadDialogue(self):
            globalDialogues.append(self.currentFile)
            with open(renpy.loader.transfn("dialogues/" + self.currentFile + '.csv'), mode="r", encoding='utf-8') as f:
                lines = f.readlines()
                f.close()

            self.headers = [s.strip().replace('\ufeff', '') for s in lines[0].split(';')]
            self.rawDialogues = lines[1:] # Ignoramos la primera fila que es la leyenda

        def PrepareDialogues(self):
            endReached = False
            for dialogue in self.rawDialogues:
                splittedDialogue = [d.strip() for d in dialogue.split(';')]
                result = dict()

                if splittedDialogue[0][0] == '#':
                    endReached = True
                    method = splittedDialogue[0][1:]
                    if method not in self.admittedTerminateMethods:
                        raise Exception(f'El método de terminación {method} no existe, los que se admiten son: ' + str(self.admittedTerminateMethods))

                    self.terminateMethod = method
                    continue

                if endReached:                    
                    self.ProcessTerminationMethod(splittedDialogue)
                    continue             

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
                    'key': terminateSplits[0],
                    'text': terminateSplits[1],
                    'nextDialogue': terminateSplits[3],
                    'points': {},
                }

                if terminateSplits[2] != '':
                    points = [s.strip() for s in terminateSplits[2].split(',')]
                    for point in points:
                        pointSplits = point.split(':')
                        pointType = pointSplits[0]
                        pointValue = int(pointSplits[1])
                        to_add['points'][pointType] = pointValue
                        
                self.choices.append((to_add['text'], to_add['key'],))
                self.terminateData.append(to_add)

        def GetNextDialogue(self):
            self.currentDialogue += 1
            if self.currentDialogue + 1 == len(self.dialogues):
                self.dialogueFinished = True

            return self.dialogues[self.currentDialogue]    

        def HandleDialogueEnd(self):
            if self.terminateMethod.lower() == 'decision':
                self.HandleDecision()
                

        def HandleDecision(self):
            result = renpy.display_menu(self.choices)
            for data in self.terminateData:
                if data['key'] == result:
                    targetDecision = data
                    break

            if len(targetDecision['points']) > 0:
                for point, value in targetDecision['points'].items():
                    if point in globalPoints:
                        globalPoints[point] += value
                    else:
                        globalPoints[point] = value

            self.currentFile = targetDecision['nextDialogue']
            globalDecisions.append(targetDecision['key'])
            self.ResetDialogueManager()
            self.LoadDialogue()
            self.PrepareDialogues()

        def ResetDialogueManager(self):
            self.rawDialogues = []
            self.dialogues = []
            self.currentDialogue = -1
            self.terminateData = []
            self.terminateMethod = ''
            self.dialogueFinished = False
            self.choices = []