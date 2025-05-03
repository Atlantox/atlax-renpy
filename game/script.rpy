define currentLanguage = 'Spanish'
define config.fadeout_audio = 3

$ import backgroundsDefine
$ import charactersDefine

$ import RouterManager
$ import DialogueManager
$ import BackgroundManager
$ import AudioManager
$ import EffectManager
$ import EventManager
$ import DelayManager

$ import animations.animations


label start:
    $ globalPoints = dict()
    $ globalDecisions = []
    $ globalDialogues = []

    $ currentKey = None
    $ currentDialogue = None    
    $ firstDialogue = 'my_scene1'

    $ routerManager = RouterManager()
    $ dialogueManager = DialogueManager(firstDialogue)
    $ dialogueManager.PrepareDialogues()
    $ backgroundManager = BackgroundManager()
    $ audioManager = AudioManager()
    $ effectManager = EffectManager()
    $ eventManager = EventManager()
    $ delayManager = DelayManager()

    while True:

        if dialogueManager.dialogueFinished:
            $ dialogueManager.HandleDialogueEnd()
            

        $ dialogue = dialogueManager.GetNextDialogue()
        
            
        $ currentKey = dialogue['Key']
        #  STATEMENT PREPARATION 

        if dialogue['Background'] != '':
            $ backgroundManager.PrepareBackground(dialogue['Background'])

        if dialogue['Music'] != '':
            $ audioManager.PrepareMusic(dialogue['Music'])

        if dialogue['Sound'] != '':
            $ audioManager.PrepareSound(dialogue['Sound'])

        if dialogue['Single effect'] != '':
            $ effectManager.PrepareSingleEffect(dialogue['Single effect'])
        
        if dialogue['Continuous effect'] != '':
            $ effectManager.PrepareContinuousEffect(dialogue['Continuous effect'])

        if dialogue['Events'] != '':
            $ eventManager.PrepareEvents(dialogue['Events'])

        if dialogue['Delay'] != '':
            $ delayManager.PrepareDelay(dialogue['Delay'])

        #  STATEMENT EXECUTION  

        if backgroundManager.prepared:
            $ backgroundManager.HandleBackground()       

        if eventManager.prepared:
            $ eventManager.HandleEvents()

        if audioManager.prepared:
            $ audioManager.HandleSFX()

        if effectManager.prepared:
            $ effectManager.HandleEffects()        

        if len(backgroundManager.postHandleEvents) > 0:
            $ backgroundManager.HandlePostEventsEffects()

        if delayManager.prepared:
            $ delayManager.HandleDelay()
        
        $ sentence = dialogue[currentLanguage]
        if delayManager.textSpeedDelay != False:
            $ sentence = '{cps=' + str(delayManager.textSpeedDelay) + '}' + sentence + '{/cps}'

        $ renpy.say(dialogue['Emisor'], sentence)

        $ delayManager.textSpeedDelay = False

    # Finaliza el juego:

    return