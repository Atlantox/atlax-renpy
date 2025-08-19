transform AdjustImage:
    fit "contain"

transform SetCharacterProperties(x, y, zoomFactor):
    xalign x
    ypos y
    zoom zoomFactor

transform EmisorEmphasis:
    ease 1:
        zoom 2

    ease 1:
        zoom 1
        