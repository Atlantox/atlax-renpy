$ import definitions.languageDefine
$ import definitions.configDefine
$ import definitions.backgroundsDefine
$ import definitions.charactersDefine
$ import definitions.stylesDefine
$ import definitions.AtlaxEncryptionKey

$ import animations.animations

$ import ConfigManager
$ import DialogueManager
$ import BackgroundManager
$ import AudioManager
$ import EffectManager
$ import EventManager
$ import DelayManager

define config.layers = ['master',  'background', 'characters', 'effects', 'transient',  'screens', 'overlay', ]

init -1 python:
    lobalPoints = dict()
    globalDecisions = []
    globalScenes = []   
    basePaths = {
        'path_background': None,
        'path_sound': None,
        'path_music': None,
        'path_scene': None,
        'path_displayable': None
    }

    configManager = ConfigManager()
    configManager.Loadconfig()


label start:    
    $ currentKey = None
    $ currentDialogue = None    
    $ lastEmisor = ''   

    $ dialogueManager = DialogueManager(configManager.firstScene)
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

        $ dialogueManager.DisplayDialogue(dialogue[configManager.currentLanguage], dialogue['Emisor'])

    # Finaliza el juego:

    return