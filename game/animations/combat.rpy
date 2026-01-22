transform Dodge(x):
    linear 0.2: 
        zoom 0.9
        alpha 0.8

    linear 0.2: 
        zoom 1
        alpha 1.0

transform Attack(x):
    linear 0.1:
        zoom 1.15

    linear 0.2: 
        zoom 1

transform Damage(x):
    xalign x
    linear 0.1 xalign (x + 0.02)
    linear 0.1 xalign x