transform scroll_text(height = 40, x = 0.5):
    ysize height
    xsize config.screen_width
    fit "contain"
    anchor (0.5, 0.0)
    xpos x

    ypos config.screen_height
    linear ((config.screen_height + height) / 100) ypos -height

transform scroll_text_to_middle(height = 40, x = 0.5):
    ysize height
    xsize config.screen_width
    fit "contain"
    anchor (0.5, 0.0)
    xpos x

    ypos config.screen_height
    ease ((config.screen_height + height) / 100) ypos 0.5

transform scroll_image(width, height, x = 0.5):
    xsize width
    ysize height
    anchor (0.5, 0.0)
    xpos x

    ypos config.screen_height
    linear ((config.screen_height + height) / 100) ypos -height


style credit_text:
    size 40
    color "#000000"
    text_align 0.5
    xalign 0.5

style credit_text_big:
    size 60
    color "#000000"
    text_align 0.5
    xalign 0.5

style credit_text_title:
    size 60
    bold True
    kerning 3
    color "#000000"
    text_align 0.5
    xalign 0.5

image creditsBackground = Solid('#FFF1CA')    

# Credits texts
image text1 = Text("En esta vida, todos somos anécdotas en el tiempo", style="credit_text")
image text2 = Text("Son las cosas que hacemos las que pueden dejar huella en los demás", style="credit_text")
image text3 = Text("Y mientras perduren esas acciones, esas cosas que hacemos, nuestra memoria también lo hará...", style="credit_text")
image text4 = Text("Para siempre", style="credit_text_big")
image text5 = Text("En recuerdo amoroso de", style="credit_text")
image text6 = Text("Nunca olvidaremos cada cosa que ustedes han creado", style="credit_text")
image text7 = Text("Katawa Shoujo The Next Step\n{b}DEMO{/b}", style="credit_text")

image madeBy = Text("Creado por", style="credit_text_title")
image company = Text("Campanella Studios", style="credit_text")

image direction = Text("Director", style="credit_text_title")
image directionTeam = Text("Deimos\nRickle89", style="credit_text")

image writters = Text("Escritores", style="credit_text_title")
image writtersTeam = Text("ElRafauricio\nLevi4tan\nCodeNameSix\nMuddyP\nRickle89", style="credit_text")

image artists = Text("Artistas", style="credit_text_title")
image artistTeam = Text("Xiloh\nDan_Snogard\nDemienR", style="credit_text")

image programming = Text("Programación", style="credit_text_title")
image programmingTeam = Text("Atlantox", style="credit_text")

image musicians = Text("Música", style="credit_text_title")
image musiciansTeam = Text("Mauryiskami\nSillxB97\nElRafauricio\nDereckNijima", style="credit_text")

image editors = Text("Editores", style="credit_text_title")
image editorsTeam = Text("AJ\nRickle89\nLancelot76", style="credit_text")

image legalSupport = Text("Soporte legal", style="credit_text_title")
image legalSupportTeam = Text("Steven-G\nShegall\nDex89", style="credit_text")

image text8 = Text("Esto es solo un comienzo...", style="credit_text")
image text9 = Text("Gracias por su increíble apoyo", style="credit_text")

image raideText = Text("Raide", style="credit_text")
image dereckText = Text("Dereck Nijima", style="credit_text")

# Credit images
image campanellaLogo = 'images/displayables/campanella.png'
image theNextStepLogo = 'images/displayables/the next step logo.png'
image dereckImage = 'images/displayables/dereck.png'
image raideImage = 'images/displayables/raide.png'

label my_credits:
    $ quick_menu = False
    $ defaultPause = 6.0

    scene creditsBackground onlayer background with Dissolve(2)
    
    show text1 onlayer screens at scroll_text()
    $ renpy.pause(defaultPause)
    hide text1

    

    show text2 onlayer screens at scroll_text()
    $ renpy.pause(defaultPause)
    hide text2

    show text3 onlayer screens at scroll_text()
    $ renpy.pause(defaultPause)
    hide text3

    show text4 onlayer screens at scroll_text(height=60)
    $ renpy.pause(defaultPause)
    hide text4
    
    show text5 onlayer screens at scroll_text()
    $ renpy.pause(0.7)
    show raideText onlayer screens at scroll_text(x=0.33)
    show dereckText onlayer screens at scroll_text(x=0.66)
    $ renpy.pause(0.5)
    show raideImage onlayer screens at  scroll_image(300, 230, 0.33)
    show dereckImage onlayer screens at scroll_image(300, 230, 0.66)

    $ renpy.pause(3.0)
    hide text5
    hide raideText
    hide dereckText
    hide raideImage
    hide dereckImage

    show text6 onlayer screens at scroll_text()
    $ renpy.pause(defaultPause)
    hide text6

    show text7 onlayer screens at scroll_text(height=80)
    $ renpy.pause(0.25)
    show theNextStepLogo onlayer screens at scroll_image(500, 400)
    $ renpy.pause(defaultPause)
    hide text7
    hide theNextStepLogo


    $ creditsPause = 0.4
    show madeBy onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show company onlayer screens at scroll_text()
    $ renpy.pause(4)

    show direction onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show directionTeam onlayer screens at scroll_text(40 * 2)
    $ renpy.pause(2.5 + (0.2 * 2))

    show writters onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show writtersTeam onlayer screens at scroll_text(40 * 5)
    $ renpy.pause(2.5 + (0.2 * 5))

    show artists onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show artistTeam onlayer screens at scroll_text(40 * 3)
    $ renpy.pause(2.5 + (0.2 * 3))

    show programming onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show programmingTeam onlayer screens at scroll_text()
    $ renpy.pause(2.5 + (0.2 * 1))

    show musicians onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show musiciansTeam onlayer screens at scroll_text(40 * 4)
    $ renpy.pause(2.5 + (0.2 * 4))

    show editors onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show editorsTeam onlayer screens at scroll_text(40 * 3)
    $ renpy.pause(2.5 + (0.2 * 3))

    show legalSupport onlayer screens at scroll_text()
    $ renpy.pause(creditsPause)
    show legalSupportTeam onlayer screens at scroll_text(40 * 3)
    $ renpy.pause(defaultPause)

    show text8 onlayer screens at scroll_text()
    $ renpy.pause(defaultPause)
    show text9 onlayer screens at scroll_text_to_middle()

    $ renpy.pause(15)
    scene bg blackout onlayer screens with Dissolve(5)
    scene bg main_menu_background onlayer screens with Dissolve(5)
    return


