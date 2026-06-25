    # copy and paste all this file content into game/screens.rpy inside screen preferences():
    # near of line code 762
    #begin language_picker

                vbox:
                    style_prefix "radio"
                    label _("Language")

                    textbutton "English" action [ Language('english'), If(dialogueManager is None, false=RestartStatement())]
                    textbutton "Español"action [ Language('spanish'), If(dialogueManager is None, false=RestartStatement())]
