$ import definitions.languageDefine
$ import definitions.configDefine
$ import definitions.backgroundsDefine
$ import definitions.charactersDefine
$ import definitions.stylesDefine
$ import definitions.AtlaxEncryptionKey

$ import animations.animations

$ import DialogueManager
$ import BackgroundManager
$ import AudioManager
$ import EffectManager
$ import EventManager
$ import DelayManager

define config.layers = ['master',  'background', 'characters', 'effects', 'transient',  'screens', 'overlay', ]

label start:    
    $ globalPoints = dict()
    $ globalDecisions = []
    $ globalScenes = []

    $ currentKey = None
    $ currentDialogue = None    
    $ firstDialogue = 'ejemplo2/ejemplo2_001_training_field'
    $ lastEmisor = ''

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

            if dialogueManager.returnToTitleScreen:
                $ renpy.call('Credits')
                return
                '''
                $ dialogueManager.returnToTitleScreen = False
                $ backgroundManager.TurnScreenToBlack()
                $ backgroundManager.ShowMainMenuBackground()
                return
                '''

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

        $ dialogueManager.DisplayDialogue(dialogue[currentLanguage], dialogue['Emisor'])

    # Finaliza el juego:

    return