transform AdjustImage:
    rotate_pad False
    fit "contain"
    blur 0.0
    rotate 0
    xsize 1.0
    ysize 1.0

transform SetCharacterProperties(x, y, zoomFactor):
    xalign x
    ypos y
    anchor (0.5, 0.0)

transform EmisorEmphasis:
    ease 1:
        zoom 2

    ease 1:
        zoom 1
        
transform HorizontalFlip():
    xzoom -1.0