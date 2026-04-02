
label mycustom:
    "aguanile"
    
    show bg dark forest onlayer effects:
        alpha 0.5
    show rafarencio onlayer characters with dissolve
    "aguanile guanila"

    menu:
        "yes":
            $ dialogueManager.customScriptResponse = 'uwu'
        "no":
            $ dialogueManager.customScriptResponse = 'nada'


    $ dialogueManager.endGame = True