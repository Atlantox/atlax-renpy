define saijo = Character('Saijo', color='#8709B4')
define mutou = Character('Mutou', color='#2595d2')

define currentLanguage = 'Spanish'
define config.fadeout_audio = 3

$ import backgroundsDefine

$ import DialogueGenerator
$ import BackgroundManager
$ import AudioManager
$ import EffectManager
$ import EventManager

label start:
    python:
        dialogueGenerator = DialogueGenerator('my_scene1.csv')
        backgroundManager = BackgroundManager()
        audioManager = AudioManager()
        effectManager = EffectManager()
        eventManager = EventManager()

        for i in range(5):
            dialogue = next(dialogueGenerator.generator)

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

            
            renpy.say(saijo, dialogue[currentLanguage])
    
    # Finaliza el juego:

    return