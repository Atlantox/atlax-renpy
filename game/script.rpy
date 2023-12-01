# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego como en el ejemplo:

define saijo = Character('Saijo', color='#8709B4')
define mutou = Character('Mutou', color='#2595d2')

define currentLanguage = 0


$ import globals
$ import scenes.example.my_scene1

label start:
    call start_my_scene11
    
    

    # Finaliza el juego:

    return