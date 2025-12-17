init python:
    class DelayManager:
        def __init__(self):
            self.prepared = False
            self.dialogueDelay = False
            self.textSpeedDelay = False
            self.defaultTextSpeed = False

        def PrepareDelay(self, delayPrompt):
            self.prepared = True

            delaySplits = [s.strip() for s in delayPrompt.split(':')]

            if len(delaySplits) > 0:
                self.dialogueDelay = float(delaySplits[0])

            if len(delaySplits) > 1:
                self.textSpeedDelay = float(delaySplits[1])

        def HandleDelay(self):
            renpy.pause(self.dialogueDelay)
            self.dialogueDelay = False
            self.prepared = False
