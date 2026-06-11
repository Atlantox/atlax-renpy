$ import definitions.customConfig
$ import definitions.customStyles
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
    audioManager = None
    backgroundManager = None
    configManager = None
    delayManager = None    
    effectManager = None
    eventManager = None
    dialogueManager = None
    simultaneousSounds = 5

    globalPoints = dict()
    globalScenes = []   

    configManager = ConfigManager()
    configManager.Loadconfig()

    if preferences.language is None:
        preferences.language = configManager.allLanguages[0]
        Language(preferences.language)

    for i in range(1, simultaneousSounds + 1):
        renpy.music.register_channel('sfx{0}'.format(i), 'sfx')

label start:        
    $ backgroundManager = BackgroundManager()
    $ audioManager = AudioManager()
    $ effectManager = EffectManager()
    $ eventManager = EventManager()
    $ delayManager = DelayManager()
    $ dialogueManager = DialogueManager(configManager.firstScene)

    $ globalPoints = dict()
    $ dialogueManager.keysWalked = []

    if dialogueManager.currentDialogueIsCustomScript:
        $ dialogueManager.CallCustomScript()
        $ dialogueManager.ProcessCustomScriptResponse()        
    else:
        $ dialogueManager.PrepareDialogues()

    while True:
        if dialogueManager.dialogueFinished:
            $ dialogueManager.HandleDialogueEnd()

            if dialogueManager.endGame:
                $ dialogueManager.endGame = False
                return

            if dialogueManager.customScriptResponse is not None:
                $ dialogueManager.ProcessCustomScriptResponse()

        $ dialogue = dialogueManager.GetNextDialogue()        
            
        ########  STATEMENT PREPARATION ########

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

        ########  STATEMENT EXECUTION ########

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

        $ dialogueManager.DisplayDialogue(dialogue[preferences.language], dialogue['Emisor'])

        $ delayManager.ResetDelayManager()

    # Game end

    return