transform scroll_text(height, x = 0.5):
    ysize height
    anchor (0.5, 0.0)
    xpos x

    ypos config.screen_height
    linear ((config.screen_height + height) / 100) ypos -height

transform scroll_image(width, height, x = 0.5):
    xsize width
    ysize height
    anchor (0.5, 0.0)
    xpos x

    ypos config.screen_height
    linear ((config.screen_height + height) / 100) ypos -height


style credit_text:
    size 40
    color "#FFFFFF"
    text_align 0.5
    xalign 0.5
    


#text madeBy = Text()
image MadeBy = Text('Hecho por\nCampanella Studios', style="credit_text")

image campanellaLogo = 'images/displayables/dmc5.png'

label Credits:
    $ defaultPause = 6.0

    scene bg blackout onlayer background with Dissolve(2)
    

    show MadeBy  onlayer screens  at scroll_text(100)
    $ renpy.pause(0.85)
    show campanellaLogo as logo onlayer screens at scroll_image(300, 200)
    $ renpy.pause(defaultPause)
    hide MadeBy
    hide logo

    pause


