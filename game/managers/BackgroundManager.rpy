init python:
    class BackgroundManager:
        def __init__(self):
            self.defaultTransition = Dissolve
            self.defaultDuration = 3.0
            self.blackScreenDuration = 7.0
            self.defaultParams = {
                'dissolve': [3.0],
                'fade': [1, 0.5, 1],
                'pixel': [3, 18],
                'pushup': [1.5, 'pushup'],
                'pushright': [1.5, 'pushright'],
                'pushdown': [1.5, 'pushdown'],
                'pushleft': [1.5, 'pushleft'],
                'rup': [1.5, True, False],
                'rright': [1.5, False, False],
                'rdown': [1.5, True, True],
                'rleft': [1.5, False, True]
            }

            self.prepared = False
            self.backgroundPlaced = False
            self.params = None
            self.backgroundQueue = []
            self.ResetBackgroundManager()

        def ResetBackgroundManager(self):
            self.targetTransition = None
            self.currentBgPath = None
            self.currentBgName = None
            self.reloadBackground = False
            self.params = None
            
            self.transformsToApply = {}

            self.postHandleEvents = []
            self.postHandleParams = []

        def PrepareBackground(self, bgPrompt):
            self.prepared = True

            backgrounds = [b.strip() for b in bgPrompt.split(',')]
            for bg in backgrounds:
                self.backgroundQueue.append(self.GetBackgroundData(bg))          
            
            lastBg = self.backgroundQueue[-1]

            self.currentBgPath = lastBg['path']
            self.currentBgName = lastBg['name']
            self.targetTransition = lastBg['transition']
            self.params = lastBg['params']

        def GetBackgroundData(self, prompt):
            currentTransition = self.defaultTransition
            params = [self.defaultDuration]
                
            promptSplits = prompt.split(':')
            bgName = promptSplits[0]            

            if len(promptSplits) >= 2:
                recievedTransition = promptSplits[1].lower()

                if recievedTransition in self.defaultParams:
                    params = self.defaultParams[recievedTransition]

                if recievedTransition == 'fade':
                    currentTransition = Fade
                elif recievedTransition == 'pixel':
                    currentTransition = Pixellate
                elif recievedTransition in ['pushup', 'pushright', 'pushdown', 'pushleft']:
                    currentTransition = PushMove
                elif recievedTransition in ['rup', 'rright', 'rdown', 'rleft']:
                    currentTransition = Swing
            
            if len(promptSplits) == 3:
                recievedParams = [float(s.strip()) for s in promptSplits[2].split(':') if s != '']
                if recievedTransition in ['rup', 'rright', 'rdown', 'rleft', 'pushup', 'pushright', 'pushdown', 'pushleft']:
                    params[0] = recievedParams[0]
                else:
                    params = recievedParams   

            return {
                'path': configManager.basePaths['path_background'] + f'{bgName}.png',
                'name': bgName,
                'transition': currentTransition,
                'params': params
            }

        def HandleBackground(self):
            self.prepared = False

            for currentBg in self.backgroundQueue:
                self.LoadBackground(currentBg)

            self.backgroundQueue = []

        def LoadBackground(self, currentBg):
                commandString = currentBg['name']

                transforms = [AdjustImage()]
                
                if len(self.transformsToApply) > 0:
                    transforms.append(Transform(**self.transformsToApply))

                renpy.show(commandString, at_list=transforms, layer='background', tag='bg')   

                if not self.backgroundPlaced: # Placing the background without transition             
                    self.backgroundPlaced = True
                    renpy.transition(Fade(2, 2, 2))
                    renpy.pause(6)
                else:
                    renpy.transition(currentBg['transition'](*currentBg['params']))

                    totalPause = 0.5
                    if currentBg['transition'] in [Dissolve, PushMove, Swing, Pixellate]:
                        totalPause = currentBg['params'][0]
                    elif currentBg['transition'] in [Fade]:
                        for param in currentBg['params']:
                            totalPause += param

                    renpy.pause(totalPause)

        def ApplyTransformsToCurrentBackground(self):
            commandString = self.currentBgName

            transforms = [AdjustImage()]
            if len(self.transformsToApply) > 0:                    
                transforms.append(Transform(**self.transformsToApply))
            renpy.show(commandString, at_list=transforms, layer='background', tag='bg')  

        def HandlePostEventsEffects(self):
            for i in range(len(self.postHandleEvents)):
                # Calling functions with corresponded params
                if self.postHandleEvents[i] == 'DisplayOverlayImage':
                    self.DisplayOverlayImage(*self.postHandleParams[i])
                elif self.postHandleEvents[i] == 'DestroyOverlayImage':
                    self.DestroyOverlayImage(*self.postHandleParams[i])
                elif self.postHandleEvents[i] == 'BlinkImage':
                    self.BlinkImage(*self.postHandleParams[i])

            self.postHandleEvents = []
            self.postHandleParams = []        

        def DisplayOverlayImage(self, bgName, opacity, isBackground):
            if isBackground:
                displayTransform = [FromHideToShow(opacity)]
            else:
                displayTransform = [ItemOnScreen(opacity)]
                
            # que aparezca con alpha 0 hasta el indicado            
            renpy.show(bgName, at_list=displayTransform, layer='effects')

        def DestroyOverlayImage(self, bgName):
            renpy.show(bgName, at_list=[HidingImage()], layer='effects')
            renpy.pause(1.4)
            renpy.hide(bgName)

        def BlinkImage(self, imageToShow, times, duration, opacity):
            for _ in range(times):
                renpy.show(imageToShow, layer='screens', at_list=[Transform(alpha=opacity)])
                renpy.pause(duration)                
                renpy.hide(imageToShow, layer="screens")
                renpy.pause(duration)

        def TurnScreenToBlack(self):
            renpy.show('bg blackout', layer='screens', tag='black_screen')
            renpy.transition(Dissolve(self.blackScreenDuration))
            renpy.pause(self.blackScreenDuration, hard=True)

        def ShowMainMenuBackground(self):
            renpy.show('bg main_menu_background', layer='screens', tag='black_screen')
            renpy.transition(Dissolve(self.blackScreenDuration))
            renpy.pause(self.blackScreenDuration, hard=True)

        def DestroyCurrentBackground(self):
            if self.currentBgName is None:
                return
            
            commandString = 'bg ' + self.currentBgName 
            renpy.hide(commandString, layer='background', tag="bg")   
            self.ResetBackgroundManager()