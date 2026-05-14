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
image text1 = Text("Your project title", style="credit_text_title")
image text2 = Text("Some text", style="credit_text")
image text3 = Text("Mooore text", style="credit_text")

image madeBy = Text("Creado por", style="credit_text_title")
image company = Text("Your company", style="credit_text")

image direction = Text("Director", style="credit_text_title")
image directionTeam = Text("name1", style="credit_text")

image writters = Text("Escritores", style="credit_text_title")
image writtersTeam = Text("name1\nname2\nname3", style="credit_text")

image artists = Text("Artistas", style="credit_text_title")
image artistTeam = Text("name1\nname2\nname3", style="credit_text")

image programming = Text("Programación", style="credit_text_title")
image programmingTeam = Text("name1\nname2\nname3", style="credit_text")

image musicians = Text("Música", style="credit_text_title")
image musiciansTeam = Text("name1\nname2\nname3", style="credit_text")

image editors = Text("Editores", style="credit_text_title")
image editorsTeam = Text("name1\nname2\nname3", style="credit_text")

image legalSupport = Text("Soporte legal", style="credit_text_title")
image legalSupportTeam = Text("name1\nname2\nname3", style="credit_text")

image thanks = Text("Gracias por su increíble apoyo", style="credit_text")

image poweredBy = Text('Hecho en', style="credit_text_title")
image poweredByText = Text('Atlax Renpy', style="credit_text")

# Credit images
image projectIcon = 'images/displayables/example project image.png'
image atlaxRenpyLogo = 'images/displayables/Atlax Renpy.png'

label my_credits:
    python:
        def TeamMembersWait(membersNumber):
            return 2.5 + (0.2 * membersNumber)

    $ dialogueManager.endGame = True
    $ quick_menu = False
    $ defaultPause = 6.0
    $ linePause = 0.4
    $ imagePause = 0.7

    scene creditsBackground onlayer background
    hide black_screen onlayer screens with Dissolve(2) # This line removes the black screen placed before the credits. So keep it.

    show text1 onlayer screens at scroll_text()
    $ renpy.pause(imagePause)
    show projectIcon onlayer screens at scroll_image(300, 300)
    $ renpy.pause(defaultPause)
    hide text1   

    show text2 onlayer screens at scroll_text()
    $ renpy.pause(defaultPause)
    hide text2

    show text3 onlayer screens at scroll_text()
    $ renpy.pause(defaultPause)
    hide text3

    show madeBy onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show company onlayer screens at scroll_text()
    $ renpy.pause(4)

    show direction onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show directionTeam onlayer screens at scroll_text(40 * 1) # 40 Times the quantity of members
    $ renpy.pause(TeamMembersWait(1)) # Place here the correct quantity of members

    show writters onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show writtersTeam onlayer screens at scroll_text(40 * 3) # 40 Times the quantity of members
    $ renpy.pause(TeamMembersWait(3)) # Place here the correct quantity of members

    show artists onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show artistTeam onlayer screens at scroll_text(40 * 3) # 40 Times the quantity of members
    $ renpy.pause(TeamMembersWait(3)) # Place here the correct quantity of members

    show programming onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show programmingTeam onlayer screens at scroll_text(40 * 3) # 40 Times the quantity of members
    $ renpy.pause(TeamMembersWait(3)) # Place here the correct quantity of members

    show musicians onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show musiciansTeam onlayer screens at scroll_text(40 * 3)  # 40 Times the quantity of members
    $ renpy.pause(TeamMembersWait(3)) # Place here the correct quantity of members

    show editors onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show editorsTeam onlayer screens at scroll_text(40 * 3)  # 40 Times the quantity of members
    $ renpy.pause(TeamMembersWait(3)) # Place here the correct quantity of members

    show legalSupport onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show legalSupportTeam onlayer screens at scroll_text(40 * 3)  # 40 Times the quantity of members
    $ renpy.pause(defaultPause)

    show poweredBy onlayer screens at scroll_text()
    $ renpy.pause(linePause)
    show poweredByText onlayer screens at scroll_text()
    $ renpy.pause(imagePause)
    show atlaxRenpyLogo onlayer screens at scroll_image(300, 300)
    $ renpy.pause(defaultPause * 2)

    show thanks onlayer screens at scroll_text_to_middle()

    $ renpy.pause(15)
    scene bg blackout onlayer screens with Dissolve(5)
    scene bg main_menu_background onlayer screens with Dissolve(5)
    return