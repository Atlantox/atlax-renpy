transform AdjustImage:
    fit "contain"

transform SetCharacterProperties(x, y, zoomFactor):
    xalign x
    ypos y
    anchor (0.5, 0.0)
    #zoom zoomFactor

transform EmisorEmphasis:
    ease 1:
        zoom 2

    ease 1:
        zoom 1
        
transform HorizontalFlip():
    xzoom -1.0