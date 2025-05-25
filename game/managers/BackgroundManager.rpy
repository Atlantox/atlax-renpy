init python:
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

            commandString = 'bg ' + self.currentBgName

            transforms = []
            for ker, value in self.transformsToApply.items():
                transforms.append(value)

            renpy.show(commandString, at_list=transforms)             

            if not self.backgroundPlaced: # Placing the background without transition             
                self.backgroundPlaced = True
            else:
                renpy.transition(self.targetTransition(*self.params))
                currentTransition = self.defaultTransition
                params = [self.defaultDuration]

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

        def DisplayOverlayImage(self, bgName, opacity):
            renpy.show(bgName, at_list=[Transform(alpha=opacity)], layer='background', tag='bg')

        def DestroyOverlayImage(self, bgName):
            renpy.hide(bgName)

        def BlinkImage(self, imageToShow, times, duration):
            for _ in range(times):
                renpy.show(imageToShow, layer='background', tag="bg")
                renpy.pause(duration)
                renpy.show('bg ' + backgroundManager.currentBgName, layer='background', tag='bg')
                renpy.pause(duration)

        def ResetBackgroundManager(self):
            self.targetTransition = None
            self.currentBgPath = None
            self.currentBgName = None
            self.params = None
            self.transformsToApply = {}

            self.postHandleEvents = []
            self.postHandleParams = []