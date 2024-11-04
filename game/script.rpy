# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego como en el ejemplo:

define saijo = Character('Saijo', color='#8709B4')
define mutou = Character('Mutou', color='#2595d2')

define currentLanguage = 'Spanish'
define config.fadeout_audio = 3

image bg sex_dungeon = 'images/backgrounds/sex dungeon.png'
image bg madera = 'images/backgrounds/madera.png'
#image bg madera_blur = Transform(Image('images/backgrounds/madera.png'), blur=15.0)


$ import globals
#$ import scenes.example.my_scene1

label start:
    $ dialogueGenerator = DialogueGenerator('my_scene1.csv')
    #show sex dungeon
    #show saijo

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

            if(audioManager.prepared):
                audioManager.HandleSFX()

            if(effectManager.prepared):
                effectManager.HandleEffects()

            
            
            renpy.say(saijo, dialogue[currentLanguage])
    
    

    # Finaliza el juego:

    return