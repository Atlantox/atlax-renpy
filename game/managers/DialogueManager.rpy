init python:
    import base64
    import hashlib
    
    class DialogueManager:
        def __init__(self, fileName):        
            self.ResetDialogueManager()

            self.minHeaderCount = 10
            self.admittedTerminateMethods = [
                'decision', 
                'condition points', 
                'condition decision', 
                'condition scene', 
                'linear', 
                'script',

                # End games
                'credits', 
                'title',
                ]
            self.admittedTerminateTransitions = ['fade', 'video']
            self.admittedPostChangingFilter = ['clear']
            self.returnToTitleDefaultTransitionParams = [Fade(7.0, 7.0, 2.0), 'screens', False]
            self.returnToTitleDefaultTransitionWait = 15.0

            self.endGame = False
            self.keysWalked = []      
            self.currentFile = fileName
            self.clearAfterNewDialogue = False
            self.lastEmisor = ''            

            self.LoadDialogue()

        def ResetDialogueManager(self):
            self.rawDialogues = []
            self.dialogues = []
            self.currentDialogue = None
            self.currentDialogueIndex = -1
            self.terminateData = []
            self.terminateMethod = ''
            self.dialogueFinished = False
            self.choices = []
            self.terminatePause = 0

            self.customScriptResponse = None
            self.customScriptLabel = None
            self.customScriptsForks = {}

            self.terminateTransition = None
            self.terminateParams = []

        def DisplayDialogue(self, dialogue, emisor):
            finalSentence = dialogue
            finalEmisor = emisor

            if delayManager.textSpeedDelay != False:
                finalSentence = "{cps=" + str(delayManager.textSpeedDelay) + "}" + dialogue + "{/cps}"     
            else:      
                finalSentence = '{cps=' + str(preferences.text_cps) + '}' + dialogue + '{/cps}'    

            if emisor == '':
                finalEmisor = self.lastEmisor
            elif emisor == '*':
                finalEmisor = ''
            else:
                if preferences.language in configManager.characterDefinitions[finalEmisor]: # If exists a language variation of this emisor, use it
                    finalEmisor = configManager.characterDefinitions[finalEmisor][preferences.language]
                else: # If don't, then use the Original name
                    finalEmisor = configManager.characterDefinitions[finalEmisor]['Original']
                
            self.lastEmisor = finalEmisor

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
            scenePath = configManager.basePaths['path_scene'] + self.currentFile + '.csv'

            sceneContent = configManager.OpenCSVFile(scenePath)

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

                if '//' in splittedDialogue[0]:
                    continue

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

            if self.terminateMethod == 'script':
                self.customScriptLabel = splittedDialogue[1]
                self.customScriptsForks = {}
                return

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
                to_add['nextScene'] = terminateSplits[1]

            elif self.terminateMethod.lower() == 'decision':
                to_add['nextScene'] = terminateSplits[2]
                to_add['text'] = terminateSplits[configManager.allLanguages.index(preferences.language) + 3]
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
                to_add['nextScene'] = terminateSplits[2]
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
                to_add['nextScene'] = terminateSplits[2]
                to_add['match'] = False

                decisions = [s.strip() for s in terminateSplits[1].split(',')]
                for decision in decisions:
                    if decision in self.keysWalked:
                        to_add['match'] = True

            elif self.terminateMethod.lower() == 'condition scene':
                to_add['nextScene'] = terminateSplits[2]
                to_add['match'] = False

                dialogues = [s.strip() for s in terminateSplits[1].split(',')]
                for dialogue in dialogues:
                    if dialogue in globalScenes:
                        to_add['match'] = True

            elif self.terminateMethod.lower() == 'credits':
                to_add['credits_label'] = 'credits'
                if len(terminateSplits) > 1:
                    to_add['credits_label'] = terminateSplits[1]

            elif self.terminateMethod.lower() == 'script':
                to_add['expected_value'] = terminateSplits[1]
                to_add['nextScene'] = terminateSplits[2]

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
            self.currentDialogueIndex += 1
            if self.currentDialogueIndex + 1 == len(self.dialogues):
                self.dialogueFinished = True

            self.currentDialogue = self.dialogues[self.currentDialogueIndex]
            return self.currentDialogue

        def HandleDialogueEnd(self):
            nextScene = None            
            
            if self.terminateMethod.lower() == 'decision':
                nextScene = self.HandleDecision()
            elif 'condition' in self.terminateMethod.lower():
                nextScene = self.HandleFork()  
            elif self.terminateMethod.lower() == 'linear':
                nextScene = self.terminateData[0]['nextScene']
                self.keysWalked.append(self.terminateData[0]['key'])
            elif self.terminateMethod.lower() == 'title':
                self.endGame = True
                self.ReturnToMainMenu()
                return
            elif self.terminateMethod.lower() == 'credits':
                backgroundManager.TurnScreenToBlack()
                renpy.call(self.terminateData[0]['credits_label'])
                return
            elif self.terminateMethod.lower() == 'script':     
                # Custom scripts must finish setting the property dialogueManager.customScriptResponse      
                # To an available response defiend in the respective .csv control file
                renpy.call(self.customScriptLabel)                
                

            if self.terminateTransition is not None:
                self.HandleTransition(clear=True)

            if nextScene is not None:
                if self.clearAfterNewDialogue:
                    self.ClearScene()              

                self.GoToNewScene(nextScene)

        def ProcessCustomScriptResponse(self):
            targetScene =  self.terminateData[-1]
                
            for fork in self.terminateData:
                if fork['expected_value'] == self.customScriptResponse:
                    targetScene = fork
                    break

            nextScene = targetScene['nextScene']
            
            key = targetScene['key']
            self.keysWalked.append(key)
            self.GoToNewScene(nextScene)

        def ReturnToMainMenu(self):
            backgroundManager.TurnScreenToBlack()
            backgroundManager.ShowMainMenuBackground()

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

            self.keysWalked.append(targetDecision['key'])    
            return targetDecision['nextScene']

        def HandleFork(self):            
            targetFork = None
            for option in self.terminateData:
                if option['match']:
                    targetFork = option
                    break
                
            # If no one condition matchs, take the last one
            if targetFork == None:
                targetFork = self.terminateData[-1]

            self.keysWalked.append(targetFork['key'])
            return targetFork['nextScene']

        def HandleTransition(self, clear = False):
            self.terminateTransition(*self.terminateParams)
            renpy.pause(self.terminatePause / 2, hard=True)
            backgroundManager.DestroyCurrentBackground()

            if clear:
                self.ClearScene()

            renpy.pause(self.terminatePause / 2, hard=True)

        def GoToNewScene(self, newDialogue):
            self.currentFile = newDialogue
            self.ResetDialogueManager()
            self.LoadDialogue()
            self.PrepareDialogues()

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