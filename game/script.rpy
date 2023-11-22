# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego como en el ejemplo:

define e = Character("Eileen")
define saijo = Character('Saijo', color='#8709B4')
define kike = Character('Mutou', color='#2595d2')

define currentLanguage = 0

label start:
    # Muestra una imagen de fondo: Aquí se usa un marcador de posición por
    # defecto. Es posible añadir un archivo en el directorio 'images' con el
    # nombre "bg room.png" or "bg room.jpg" para que se muestre aquí.

    scene sex dungeon

    # Muestra un personaje: Se usa un marcador de posición. Es posible
    # reemplazarlo añadiendo un archivo llamado "eileen happy.png" al directorio
    # 'images'.

    show saijo

    # Presenta las líneas del diálogo.

    #for d in dialogues:
        #saijo "{d}
    init python:
        sentences = []
        f = open(renpy.loader.transfn("001_Demo_Ch1.csv"),"r")
        sentences = f.readlines()
        f.close()

        def getNextDialogue():
            for sentence in sentences[1:]:
                yield str(sentence.split(';'))

        dialogueGenerator = getNextDialogue()
    
    while True:
        $ dialogue = next(dialogueGenerator)
        $ sentence = dialogue[currentLanguage + 2]
        $ speaker = dialogue[1]
        call speaker "[speaker] [sentence]"
        


    # Finaliza el juego:

    return

