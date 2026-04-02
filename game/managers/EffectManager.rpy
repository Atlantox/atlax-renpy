init python:
    class EffectManager:
        def __init__(self):
            self.prepared = False
            self.imagesBasePath = 'images/displayables/'
            self.backgroundDeformEffects = ['blur', 'rotate', 'hwarp', 'vwarp']
            self.availableSingleEffects = ['vpunch', 'hpunch']

            self.defaultShakeIntensity = 20
            self.defaultBlurIntensity = 15.0
            self.defaultRotationDegrees = 45
            self.defaultWarp = 1.1
            self.defaultSingleEffetDuration = 0.1
            self.defaultBlinkTimes = 4
            self.defaultBlinkOpacity = 1
            self.defaultOverlayOpacity = 1.0

            self.continuousEffectQueue = []
            self.effectQueue = []

            self.currentContinuousEffects = []        

        def PrepareSingleEffect(self, effectPrompt):
            self.prepared = True

            recievedEffects = [e.strip() for e in effectPrompt.split(',')]

            for effect in recievedEffects:
                effectSplits = [e.replace('_', ' ').strip() for e in effect.split(':')]
                effectName = effectSplits[0]

                if effectName in self.availableSingleEffects:
                    if effectName in ['vpunch', 'hpunch']:
                        self.PrepareShake(effectSplits)
                else:
                    exists = renpy.exists(configManager.basePaths['path_background'] + effectName + '.png')
                    self.PrepareImageBlink(effectSplits, exists)

        def PrepareShake(self, shakeSplits):
            intensity = self.defaultShakeIntensity

            if len(shakeSplits) >= 2:
                intensity = int(shakeSplits[1])

            if shakeSplits[0] == 'vpunch':
                shakeTransition = Move((0, intensity), (0, intensity * -1), self.defaultSingleEffetDuration, bounce=True, repeat=True, delay=.275)
                
            if shakeSplits[0] == 'hpunch':
                shakeTransition = Move((intensity, 0), (intensity * -1, 0), self.defaultSingleEffetDuration, bounce=True, repeat=True, delay=.275)

            self.effectQueue.append(shakeTransition)

        def PrepareImageBlink(self, effectSplits, imageExists = True):
            if imageExists is False: return
            effectName = effectSplits[0]
            duration = self.defaultSingleEffetDuration
            times = self.defaultBlinkTimes
            opacity = self.defaultBlinkOpacity

            if len(effectSplits) > 1:
                duration = float(effectSplits[1])

            if len(effectSplits) > 2:
                times = int(effectSplits[2])

            if len(effectSplits) > 3:
                opacity = float(effectSplits[3])

            imageToShow = 'bg ' + effectName.replace(' ', '_')                    
            backgroundManager.postHandleEvents.append('BlinkImage')
            backgroundManager.postHandleParams.append([imageToShow, times, duration, opacity])
        
        def PrepareContinuousEffect(self, effectPrompt):
            self.prepared = True

            recievedEffects = [e.strip() for e in effectPrompt.split(',')]

            for effect in recievedEffects:
                effectSplits = [e.strip() for e in effect.split(':')]
                effectName = effectSplits[0]

                if effectName in self.backgroundDeformEffects:
                    self.PrepareBackgroundTransform(effectSplits)
                else:
                    bg_exists = renpy.exists(configManager.basePaths['path_background'] + effectName + '.png')
                    if bg_exists:
                        self.PrepareDisplayImageOverBackground(effectSplits, True)
                    else:                        
                        self.PrepareDisplayImageOverBackground(effectSplits, False)

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

                backgroundManager.transformsToApply[effectName] = targetEffect

        def PrepareDisplayImageOverBackground(self, effectSplits, isBackbround = True):
            imageName = effectSplits[0]
            opacity = self.defaultOverlayOpacity

            if len(effectSplits) > 1:
                opacity = float(effectSplits[1])

            if imageName in self.currentContinuousEffects:
                effectIdx = self.currentContinuousEffects.index(imageName)
                del self.currentContinuousEffects[effectIdx]
                targetFunction = 'DestroyOverlayImage'
                params = [imageName]
            else:
                self.currentContinuousEffects.append(imageName)
                targetFunction = 'DisplayOverlayImage'
                params = [imageName, opacity, isBackbround]
            
            backgroundManager.postHandleEvents.append(targetFunction)
            backgroundManager.postHandleParams.append(params)           

        def HandleEffects(self):
            self.prepared = False
            if len(self.effectQueue) > 0:
                for e in self.effectQueue:                    
                    renpy.transition(e)
                    #renpy.with_statement(e)
                    renpy.pause(.5)

                self.effectQueue = []

            if len(self.continuousEffectQueue) > 0:
                pass