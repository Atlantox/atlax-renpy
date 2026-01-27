init python:
    class BackgroundManager:
        def __init__(self):
            self.baseBgPath = 'images/backgrounds/'
            self.defaultTransition = Dissolve
            self.defaultDuration = 2.0
            self.defaultParams = {
                'dissolve': [2.0],
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


            backgroundPath = self.baseBgPath + f'{bgName}.png'

            self.currentBgPath = backgroundPath
            self.currentBgName = bgName
            self.targetTransition = currentTransition
            self.params = params

        def HandleBackground(self):
            self.prepared = False

            commandString = 'bg ' + self.currentBgName

            transforms = [AdjustImage()]
            for ker, value in self.transformsToApply.items():
                transforms.append(value)

            renpy.show(commandString, at_list=transforms, layer='master', tag='bg')             

            if not self.backgroundPlaced: # Placing the background without transition             
                self.backgroundPlaced = True
            else:
                renpy.transition(self.targetTransition(*self.params))

                totalPause = 0.5
                if self.targetTransition in [Dissolve, PushMove, Swing, Pixellate]:
                    totalPause = self.params[0]
                elif self.targetTransition == Fade:
                    for param in self.params:
                        totalPause += param

                renpy.pause(totalPause)

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
            renpy.show(bgName, at_list=displayTransform, layer='master')

        def DestroyOverlayImage(self, bgName):
            renpy.show(bgName, at_list=[HidingImage()])
            renpy.pause(1.4)
            renpy.hide(bgName)

        def BlinkImage(self, imageToShow, times, duration):
            for _ in range(times):
                renpy.show('bg red_2', layer='screens')
                renpy.pause(duration)                
                renpy.hide(imageToShow, layer="screens")
                renpy.pause(duration)

        def ResetBackgroundManager(self):
            self.targetTransition = None
            self.currentBgPath = None
            self.currentBgName = None
            self.params = None
            self.transformsToApply = {}

            self.postHandleEvents = []
            self.postHandleParams = []

        def DestroyCurrentBackground(self):
            if self.currentBgName is None:
                return
            
            commandString = 'bg ' + self.currentBgName
            renpy.hide(commandString, layer='master')   
            self.ResetBackgroundManager()