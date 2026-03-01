init python:
    import base64
    import hashlib
    
    class DialogueManager:
        def __init__(self, fileName):        
            self.ResetDialogueManager()

            self.minHeaderCount = 10
            self.defaultCharacterSpeed = '45'
            self.admittedTerminateMethods = ['decision', 'condition points', 'condition decision', 'condition scene', 'linear', 'credits', 'title']
            self.admittedTerminateTransitions = ['fade', 'video']
            self.admittedPostChangingFilter = ['clear']
            self.returnToTitleDefaultTransitionParams = [Fade(4.0, 1, 2.0), 'screens', False]
            self.returnToTitleDefaultTransitionWait = 4.0

            self.returnToTitleScreen = False
            self.currentFile = fileName
            self.clearAfterNewDialogue = False
            self.lastEmisor = ''            

            self.LoadDialogue()

        def DisplayDialogue(self, dialogue, emisor):
            finalSentence = dialogue
            finalEmisor = emisor

            if delayManager.textSpeedDelay != False:
                finalSentence = "{cps=" + str(delayManager.textSpeedDelay) + "}" + dialogue + "{/cps}"     
            else:      
                finalSentence = "{cps=" + self.defaultCharacterSpeed + "}" + dialogue + "{/cps}"     

            if emisor == '':
                finalEmisor = self.lastEmisor
            elif emisor == '*':
                finalEmisor = ''

            if finalEmisor != self.lastEmisor:                
                pass
                
            self.lastEmisor = finalEmisor
            
            if finalEmisor in languageDependingNames:
                finalEmisor = languageDependingNames[finalEmisor][currentLanguage]

            finalEmisor = characters[finalEmisor]
                
            finalSentence = finalSentence.replace('#.,',';').replace('%','%%')
            renpy.say(finalEmisor, finalSentence)
            delayManager.textSpeedDelay = False

        def GetBytes(self, data):
            key = hashlib.sha256(atlax_encryption_key.encode()).digest()
            return bytes(
                data[i] ^ key[i % len(key)]
                for i in range(len(data))
            )

        def DecryptScene(self, sceneFileContent):           
            data = base64.b64decode(sceneFileContent)
            decrypted = self.GetBytes(data)
            return decrypted.decode("utf-8")
            

        def LoadDialogue(self):
            fileName = self.currentFile.split('/')
            if len(fileName) > 1:
                fileName = fileName[-1]
            else:
                fileName = fileName[0]

            globalScenes.append(fileName)

            with open(renpy.loader.transfn("scenes/" + self.currentFile + '.csv'), mode="r", encoding="utf-8") as f:
                sceneContent = f.read()
                f.close()

            if requireSceneEncryption:
                sceneContent = self.DecryptScene(sceneContent)
            
            lines = sceneContent.strip().split('\n')

            self.headers = [s.strip().replace('\ufeff', '') for s in lines[0].split(';')]
            self.rawDialogues = lines[1:] # Ignoramos la primera fila que es la leyenda

            dialogueCheckpoint = True
            if dialogueCheckpoint:
                finalDialogues = []
                for i in range(len(self.rawDialogues)):
                    line = self.rawDialogues[i]
                    if line[0] == '*':
                        self.rawDialogues = self.rawDialogues[i:]
                        break


        def PrepareDialogues(self):
            endReached = False
            for dialogue in self.rawDialogues:
                splittedDialogue = [d.strip() for d in dialogue.split(';')]
                result = dict()

                if splittedDialogue[0][0] == '#':
                    endReached = True
                    self.ProcessTerminationMethod(splittedDialogue)
                    continue

                if endReached:                    
                    self.ProcessTerminationData(splittedDialogue)
                    continue             

                if len(splittedDialogue) < self.minHeaderCount:
                    error = 'Error en el diálogo {0}: No cumple con el mínimo número de columnas'.format(splittedDialogue[0])
                    raise Exception(error)

                headerIdx = 0
                for header in self.headers:
                    if headerIdx >= len(splittedDialogue):
                        break

                    result[header] = splittedDialogue[headerIdx].strip()
                    headerIdx += 1
                    
                self.dialogues.append(result)

        def ProcessTerminationMethod(self, splittedDialogue):  
            method = splittedDialogue[0][1:]
            if method not in self.admittedTerminateMethods:
                error = 'Error en el diálogo {0}: El método de terminación {1} no existe, los que se admiten son: '.format(splittedDialogue[0], method)
                raise Exception(error + str(self.admittedTerminateMethods))

            self.terminateMethod = method

            if len(splittedDialogue) > 1:
                transitionSplits = [s.strip() for s in splittedDialogue[1].split(':')]
                terminateTransition = transitionSplits[0]

                if terminateTransition not in self.admittedTerminateTransitions and terminateTransition != '':
                    error = 'Error en el diálogo {0}: La transicion de terminación {1} no existe, los que se admiten son: '.format(splittedDialogue[0], terminateTransition)
                    raise Exception(error + str(self.admittedTerminateTransitions))

            if len(splittedDialogue) > 2:
                if splittedDialogue[2] == 'clear':
                    self.clearAfterNewDialogue = True

                self.ProcesTerminationTransition(splittedDialogue[1])

        def ProcessTerminationData(self, terminateSplits):
            to_add = {
                'key': terminateSplits[0]
            }

            if self.terminateMethod.lower() == 'linear':
                to_add['nextDialogue'] = terminateSplits[1]

            elif self.terminateMethod.lower() == 'decision':
                to_add['nextDialogue'] = terminateSplits[2]
                to_add['text'] = terminateSplits[allLanguages.index(currentLanguage) + 3]
                to_add['points'] = {}

                if terminateSplits[1] != '':
                    points = [s.strip() for s in terminateSplits[1].split(',')]
                    for point in points:
                        pointSplits = point.split(':')
                        pointType = pointSplits[0]
                        pointValue = int(pointSplits[1])
                        to_add['points'][pointType] = pointValue
                        
                self.choices.append((to_add['text'], to_add['key'],))

            elif self.terminateMethod.lower() == 'condition points':
                to_add['nextDialogue'] = terminateSplits[2]
                to_add['match'] = False

                conditions = [s.strip() for s in terminateSplits[1].split(',')]                
                
                if conditions == ['']:
                    to_add['match'] = True
                else:
                    results = []
                    for condition in conditions:
                        results.append(self.GetConditionResult(condition))
                    
                    if all(results):
                        to_add['match'] = True    

            elif self.terminateMethod.lower() == 'condition decision':
                to_add['nextDialogue'] = terminateSplits[2]
                to_add['match'] = False

                decisions = [s.strip() for s in terminateSplits[1].split(',')]
                for decision in decisions:
                    if decision in globalDecisions:
                        to_add['match'] = True

            elif self.terminateMethod.lower() == 'condition scene':
                to_add['nextDialogue'] = terminateSplits[2]
                to_add['match'] = False

                dialogues = [s.strip() for s in terminateSplits[1].split(',')]
                for dialogue in dialogues:
                    if dialogue in globalScenes:
                        to_add['match'] = True

            self.terminateData.append(to_add)

        def ProcesTerminationTransition(self, transitionData):
            splits = [s.strip() for s in transitionData.split(':')]
            transitionName = splits[0]

            if transitionName == 'fade':
                fadeOut = float(splits[1])
                fadeDuration = float(splits[2])
                fadeIn = float(splits[3])
                fade = Fade(fadeOut, fadeDuration, fadeIn)
                layer = 'screens'
                always = True

                self.terminateTransition = renpy.transition
                self.terminateParams = [fade, layer, always]
                self.terminatePause = fadeOut + fadeDuration + fadeIn
            elif transitionName == 'video':
                videoName = splits[1]
                self.terminateTransition = renpy.movie_cutscene
                self.terminateParams = ['videos/' + videoName]

        def GetNextDialogue(self):
            self.currentDialogue += 1
            if self.currentDialogue + 1 == len(self.dialogues):
                self.dialogueFinished = True

            return self.dialogues[self.currentDialogue]    

        def HandleDialogueEnd(self):
            nextDialogue = None
            
            if self.terminateMethod.lower() == 'decision':
                nextDialogue = self.HandleDecision()
            elif 'condition' in self.terminateMethod.lower():
                nextDialogue = self.HandleFork()  
            elif self.terminateMethod.lower() == 'linear':
                nextDialogue = self.terminateData[0]['nextDialogue']
            elif self.terminateMethod.lower() == 'title':
                self.returnToTitleScreen = True

                self.terminateTransition = renpy.transition
                self.terminateParams = self.returnToTitleDefaultTransitionParams
                self.terminatePause = self.returnToTitleDefaultTransitionWait

            if self.terminateTransition is not None:
                self.HandleTransition(clear=True)

            if nextDialogue is not None:
                if self.clearAfterNewDialogue:
                    self.ClearScene()              

                self.GoToNewDialogue(nextDialogue)


        def ClearScene(self):
            renpy.scene()
            eventManager.DestroyAllCharacters()
            eventManager.ResetEventManager()
            self.clearAfterNewDialogue = False

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

            globalDecisions.append(targetDecision['key'])    
            return targetDecision['nextDialogue']

        def HandleFork(self):            
            targetFork = None
            for option in self.terminateData:
                if option['match']:
                    targetFork = option
                    break
                
            # If no one condition matchs, take the last one
            if targetFork == None:
                targetFork = self.terminateData[-1]

            globalDecisions.append(targetFork['key'])
            return targetFork['nextDialogue']

        def HandleTransition(self, clear = False):
            self.terminateTransition(*self.terminateParams)
            renpy.pause(self.terminatePause / 2, hard=True)
            backgroundManager.DestroyCurrentBackground()

            if clear:
                self.ClearScene()

            renpy.pause(self.terminatePause / 2, hard=True)

        def GoToNewDialogue(self, newDialogue):
            self.currentFile = newDialogue
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
            self.terminatePause = 0

            self.terminateTransition = None
            self.terminateParams = []

        def GetConditionResult(self, condition):
            operators = ['<', '>', '=']
            targetOperator = None

            for operator in operators:
                if operator in condition:
                    targetOperator = operator
                    splits = [s.strip() for s in condition.split(operator)]

            if targetOperator == None:
                raise Exception('Operador inválido para ' + condition)

            key = splits[0]
            value = int(splits[1])

            if key not in globalPoints:
                raise Exception('El punto ' + key + ' no existe')

            result = None
            if targetOperator == '>':
                result = globalPoints[key] > value
            elif targetOperator == '<':
                result = globalPoints[key] < valu
            elif targetOperator == '=':
                result = globalPoints[key] == value

            return result
                