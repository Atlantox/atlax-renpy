transform AdjustImage:
    fit "contain"

transform SetCharacterProperties(x, y, z, zoomFactor):
    xalign x
    ypos y
    zpos z
    zoom zoomFactor