define currentLanguage = 'Spanish'
define config.fadeout_audio = 3

$ import backgroundsDefine
$ import charactersDefine

$ import DialogueManager
$ import BackgroundManager
$ import AudioManager
$ import EffectManager
$ import EventManager

$ import animations.animations


label start:
    $ currentKey = None
    $ dialogueManager = DialogueManager('my_scene1.csv')
    $ dialogueManager.PrepareDialogues()
    $ backgroundManager = BackgroundManager()
    $ audioManager = AudioManager()
    $ effectManager = EffectManager()
    $ eventManager = EventManager()

    while True:
        $ dialogue = dialogueManager.GetNextDialogue()
            
        $ currentKey = dialogue['Key']
        #  STATEMENT PREPARATION 

        if(dialogue['Background'] != ''):
            $ backgroundManager.PrepareBackground(dialogue['Background'])

        if(dialogue['Music'] != ''):
            $ audioManager.PrepareMusic(dialogue['Music'])

        if(dialogue['Sound'] != ''):
            $ audioManager.PrepareSound(dialogue['Sound'])

        if(dialogue['Single effect'] != ''):
            $ effectManager.PrepareSingleEffect(dialogue['Single effect'])
        
        if(dialogue['Continuous effect'] != ''):
            $ effectManager.PrepareContinuousEffect(dialogue['Continuous effect'])

        if(dialogue['Events'] != ''):
            $ eventManager.PrepareEvents(dialogue['Events'])


        #  STATEMENT EXECUTION  

        if(backgroundManager.prepared):
            $ backgroundManager.HandleBackground()

        if len(backgroundManager.postHandleEvents) > 0:
            $ backgroundManager.HandlePostEventsEffects()

        if(audioManager.prepared):
            $ audioManager.HandleSFX()

        if(effectManager.prepared):
            $ effectManager.HandleEffects()

        if(eventManager.prepared):
            $ eventManager.HandleEvents()

        
        $ renpy.say(dialogue['Emisor'], dialogue[currentLanguage])

    # Finaliza el juego:

    return