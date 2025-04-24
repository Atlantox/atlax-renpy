define currentLanguage = 'Spanish'
define config.fadeout_audio = 3

$ import backgroundsDefine
$ import charactersDefine

$ import DialogueGenerator
$ import BackgroundManager
$ import AudioManager
$ import EffectManager
$ import EventManager

$ import animations.animations


label start:
    $ currentKey = None
    python:
        dialogueGenerator = DialogueGenerator('my_scene1.csv')
        backgroundManager = BackgroundManager()
        audioManager = AudioManager()
        effectManager = EffectManager()
        eventManager = EventManager()

        if currentKey is not None:

        while True:
            dialogue = next(dialogueGenerator.generator)

            if currentKey is not None:
                if currentKey != dialogue['Key']:
                    continue

            
            currentKey = dialogue['Key']
            '''  STATEMENT PREPARATION  '''

            if(dialogue['Background'] != ''):
                backgroundManager.PrepareBackground(dialogue['Background'])

            if(dialogue['Music'] != ''):
                audioManager.PrepareMusic(dialogue['Music'])

            if(dialogue['Sound'] != ''):
                audioManager.PrepareSound(dialogue['Sound'])

            if(dialogue['Single effect'] != ''):
                effectManager.PrepareSingleEffect(dialogue['Single effect'])
            
            if(dialogue['Continuous effect'] != ''):
                effectManager.PrepareContinuousEffect(dialogue['Continuous effect'])

            if(dialogue['Events'] != ''):
                eventManager.PrepareEvents(dialogue['Events'])


            '''  STATEMENT EXECUTION  '''

            if(backgroundManager.prepared):
                backgroundManager.HandleBackground()

            if len(backgroundManager.postHandleEvents) > 0:
                backgroundManager.HandlePostEventsEffects()

            if(audioManager.prepared):
                audioManager.HandleSFX()

            if(effectManager.prepared):
                effectManager.HandleEffects()

            if(eventManager.prepared):
                eventManager.HandleEvents()

            
            renpy.say(dialogue['Emisor'], dialogue[currentLanguage])
            print('terminando dialogo', dialogue['Key'])
    # Finaliza el juego:

    return