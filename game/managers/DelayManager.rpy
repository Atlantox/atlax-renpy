init python:
    class DelayManager:
        def __init__(self):
            self.ResetDelayManager()

        def ResetDelayManager(self):
            self.textSpeedDelay = False
            self.dialogueDelay = False
            self.prepared = False
            self.autopass = False

        def PrepareDelay(self, delayPrompt):
            self.prepared = True

            delaySplits = [s.strip() for s in delayPrompt.split(':')]

            if 'pass' in delaySplits:
                self.autopass = True
                idx = delaySplits.index('pass')
                del delaySplits[idx]                

            if len(delaySplits) > 0:

                self.dialogueDelay = float(delaySplits[0])

            if len(delaySplits) > 1:
                self.textSpeedDelay = float(delaySplits[1])            

        def HandleDelay(self):
            renpy.pause(self.dialogueDelay)