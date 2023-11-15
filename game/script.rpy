# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego como en el ejemplo:

define e = Character("Eileen")
define saijo = Character('Saijo', color='#8709B4')

define dialogues = [
    "Pareces tener mala cara, acuéstate donde quieras para revisarte bien", 
    "XDXDXD"
]

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
        #saijo "{d}"
    $ i = 0
    while i < len(dialogues):
        $ crtDialogue = dialogues[i]
        saijo "[crtDialogue]"
        $ i+=1


    # Finaliza el juego:

    return
