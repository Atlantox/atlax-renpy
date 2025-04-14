transform Jump(x, intensity):
    animation
    xalign x
    linear 0.1 ypos (intensity * -1)
    linear 0.1 ypos 0.

transform HitR(x, intensity):
    animation
    ypos -0.059
    linear 0.1:         
        rotate intensity

    linear 0.1:
        rotate 0

    
transform HitL(x, intensity):
    animation
    ypos -0.059
    linear 0.1:         
        rotate (intensity * -1)

    linear 0.1:
        rotate 0
    


transform Tremble(x, times):
    animation
    xalign x

    linear 0.05:
        xalign (x + .005)

    linear 0.05:
        xalign (x - .005)

    repeat times
    

transform Trembling(x):
    animation
    xalign x

    linear 0.05:
        xalign (x + .005)

    linear 0.05:
        xalign (x - .005)

    repeat