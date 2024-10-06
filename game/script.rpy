# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego como en el ejemplo:

define saijo = Character('Saijo', color='#8709B4')
define mutou = Character('Mutou', color='#2595d2')

define currentLanguage = 'Spanish'

image bg sex_dungeon = 'images/backgrounds/sex dungeon.png'
image bg madera = 'images/backgrounds/madera.jpg'


$ import globals
#$ import scenes.example.my_scene1

label start:
    $ dialogueGenerator = DialogueGenerator('my_scene1.csv')
    #show sex dungeon
    #show saijo

    python:
        for i in range(5):
            dialogue = next(dialogueGenerator.generator)

            # First, the backgrounds
            if(dialogue['Background'] != ''):
                backgroundManager.ChangeBackground(dialogue['Background'])
            
            renpy.say(saijo, dialogue[currentLanguage])
    
    

    # Finaliza el juego:

    return