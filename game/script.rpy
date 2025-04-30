define currentLanguage = 'Spanish'
define config.fadeout_audio = 3

$ import backgroundsDefine
$ import charactersDefine

$ import DialogueManager
$ import BackgroundManager
$ import AudioManager
$ import EffectManager
$ import EventManager
$ import DelayManager

$ import animations.animations


label start:
    $ currentKey = None
    $ dialogueManager = DialogueManager('my_scene1.csv')
    $ dialogueManager.PrepareDialogues()
    $ backgroundManager = BackgroundManager()
    $ audioManager = AudioManager()
    $ effectManager = EffectManager()
    $ eventManager = EventManager()
    $ delayManager = DelayManager()

    while True:
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

        if len(backgroundManager.postHandleEvents) > 0:
            $ backgroundManager.HandlePostEventsEffects()

        if audioManager.prepared:
            $ audioManager.HandleSFX()

        if effectManager.prepared:
            $ effectManager.HandleEffects()

        if eventManager.prepared:
            $ eventManager.HandleEvents()

        if delayManager.prepared:
            $ delayManager.HandleDelay()
        
        $ to_say = dialogue[currentLanguage]
        if delayManager.textSpeedDelay != False:
            $ to_say = '{cps=' + str(delayManager.textSpeedDelay) + '}' + to_say + '{/cps}'

        $ renpy.say(dialogue['Emisor'], to_say)

        $ delayManager.textSpeedDelay = False

    # Finaliza el juego:

    return