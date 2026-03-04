image creditTitle = ParameterizedText(size=40)

transform appear:
    alpha 0.0
    align (0.5, 0.5)


    linear 2.0:
        alpha 1.0

screen info_screen(message):
    text message at appear 


label Credits:
    show bg blackout onlayer background with Dissolve(3)
    #show text "Hecho por Campanella Studios" at truecenter
    show screen info_screen("Hecho por Campanella Studios")
    #show creditTitle "Hecho por Campanella Studios" at appear
    pause


