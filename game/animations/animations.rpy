transform Jump(x, intensity):
    animation
    xalign x
    anchor (0.5, 0.0)
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
    animation
    xalign x
    anchor (0.5, 0.0)

    linear 0.05:
        anchor (0.52, 0.0)

    linear 0.05:
        anchor (0.48, 0.0)

    repeat times
    anchor (0.5, 0.0)
    

transform Trembling(x):
    xalign x
    anchor (0.5, 0.0)
    animation

    linear 0.05:
        anchor (0.52, 0.0)

    linear 0.05:
        anchor (0.48, 0.0)

    repeat

transform HitR(x, intensity):
    animation    
    ypos -0.059
    xalign x
    anchor (0.5, 0.0)
    linear 0.1:
        rotate intensity

    linear 0.1:
        rotate 0

    
transform HitL(x, intensity):
    animation    
    ypos -0.059
    xalign x
    anchor (0.5, 0.0)
    linear 0.1:
        rotate (intensity * -1)

    linear 0.1:
        rotate 0    

transform MyZoom(x, factor, duration):
    animation
    xalign x
    anchor (0.5, 0.0)
    linear duration zoom factor


transform KnockR(x, duration):
    animation
    xalign x
    ypos -0.059
    anchor (0.5, 0.0)
    linear duration:
        yanchor -1.0
        rotate 90

transform KnockL(x, duration):
    animation
    xalign x
    ypos -0.059
    anchor (0.5, 0.0)
    linear duration:
        yanchor -1.0
        rotate -90   
    
transform RaiseR(x, duration):
    animation
    xalign x
    ypos -0.059
    anchor (0.5, -1.0)
    rotate 90    
    linear duration:
        rotate 0    
        anchor (0.5, 0.0)

transform RaiseL(x, duration):
    animation
    xalign x
    ypos -0.059
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
    #pause 2.0
    #linear 1.0 rotate 0