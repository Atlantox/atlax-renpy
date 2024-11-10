define saijo = Character('Saijo', color='#8709B4')
define mutou = Character('Mutou', color='#2595d2')

define currentLanguage = 'Spanish'
define config.fadeout_audio = 3

image bg sex_dungeon = 'images/backgrounds/sex dungeon.png'
image bg madera = 'images/backgrounds/madera.png'
image bg flash = 'images/backgrounds/flash.png'
image bg blackout = 'images/backgrounds/blackout.png'


$ import globals

label start:
    $ dialogueGenerator = DialogueGenerator('my_scene1.csv')

    python:
        for i in range(5):
            dialogue = next(dialogueGenerator.generator)

            '''  STATEMENT PREPARATION  '''

            if(dialogue['Background'] != ''):
                backgroundManager.PrepareBackground(dialogue['Background'])

            if(dialogue['Music'] != ''):
                audioManager.PrepareMusic(dialogue['Music'])

            if(dialogue['Sound'] != ''):
                audioManager.PrepareSound(dialogue['Sound'])

            if(dialogue['Effect'] != ''):
                effectManager.PrepareEffects(dialogue['Effect'])


            '''  STATEMENT EXECUTION  '''

            if(backgroundManager.prepared):
                backgroundManager.HandleBackground()

            if len(backgroundManager.postHandleEvents) > 0:
                backgroundManager.HandlePostEventsEffects()

            if(audioManager.prepared):
                audioManager.HandleSFX()

            if(effectManager.prepared):
                effectManager.HandleEffects()

            
            renpy.say(saijo, dialogue[currentLanguage])
    
    # Finaliza el juego:

    return