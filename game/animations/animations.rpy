transform Jump(x, intensity):    
    linear 0.1 ypos (intensity * -1)
    linear 0.1 ypos 0.

transform Jumping(x, intensity):
    animation
    xalign x
    anchor (0.5, 0.0)
    linear 0.1 ypos (intensity * -1)
    linear 0.1 ypos 0.
    0.8
    repeat

transform Tremble(x, times):
    xalign x
    linear 0.1:            
        xalign x + 0.002

    linear 0.1:
        xalign x - 0.002
    
    repeat times
    

transform Trembling(x):
    xalign x
    linear 0.1:            
        xalign x + 0.002

    linear 0.1:
        xalign x - 0.002
    
    repeat    

transform HitR(x, intensity):
    rotate_pad False
    transform_anchor False

    linear 0.1:
        rotate intensity

    linear 0.1:
        rotate 0

    
transform HitL(x, intensity):
    rotate_pad False
    transform_anchor False
       
    linear 0.1:
        rotate (intensity * -1)
        

    linear 0.1:
        rotate 0.



transform MyZoom(newFactor, duration):
    linear duration:
        zoom newFactor

transform KnockR(x, duration):
    rotate_pad False
    transform_anchor False
    linear duration:
        yanchor -1.0
        rotate 90

transform KnockL(x, duration):
    rotate_pad False
    transform_anchor False
    
    linear duration:
        yanchor -1.0
        rotate -90   
    
transform RaiseR(x, duration):
    ypos -0.053
    anchor (0.5, -1.0)
    rotate 90    
    linear duration:
        rotate 0    
        anchor (0.5, 0.0)

transform RaiseL(x, duration):
    ypos -0.053
    anchor (0.5, -1.0)
    rotate -90
    linear duration:
        rotate 0    
        anchor (0.5, 0.0)


transform MoveY(x, y, destination, duration):
    animation
    xalign x
    ypos y
    anchor (0.5, 0.0)
    linear duration ypos destination


transform FullCenter():
    anchor (0.5, 0.5)
    xalign 0.5
    yalign 0.5
    alpha 1.0

transform PassScene():   
    xysize (10, 600)
    rotate 0
    linear 3.0 rotate 180

transform CharacterTransform():
    zpos 100

transform BackgroundTransform():
    zpos 0

transform ItemOnScreen(opacity):
    alpha 0.0
    xalign 0.5
    yalign 1.0
    anchor (0.5, 0.5)

    ease 1.2:
        alpha opacity
        yalign 0.2

transform FromHideToShow(opacity):
    alpha 0.0

    linear 1:
        alpha opacity
    

transform DisappearCharacter(duration):
    linear duration:
        alpha 0


transform HidingImage:
    yalign 0.2

    ease 1.2:
        alpha 0
        yalign 1.0

# Import here your custom animations files
$ import animations.combat
$ import animations.movement