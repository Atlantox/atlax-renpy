    # copy and paste all this file content into game/screens.rpy inside screen preferences():
    # near of line code 756
    #begin language_picker

                vbox:
                    style_prefix "radio"
                    label _("Language")

                    textbutton "English" text_font "playtime.ttf" action [ Language('english'), If(dialogueManager is None, false=RestartStatement())]
                    textbutton "Español" text_font "playtime.ttf" action [ Language('spanish'), If(dialogueManager is None, false=RestartStatement())]
