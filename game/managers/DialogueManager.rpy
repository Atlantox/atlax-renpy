init python:
    class DialogueManager:
        def __init__(self, fileName):
            self.minHeaderCount = 10
            self.rawDialogues = []
            self.dialogues = []
            self.currentDialogue = -1

            with open(renpy.loader.transfn("dialogues/" + fileName), mode="r", encoding='utf-8') as f:
                lines = f.readlines()
                f.close()

            self.headers = [s.strip().replace('\ufeff', '') for s in lines[0].split(';')]
            self.rawDialogues = lines[1:] # Ignoramos la primera fila que es la leyenda

        def PrepareDialogues(self):
            for dialogue in self.rawDialogues:
                splittedDialogue = [d.strip() for d in dialogue.split(';')]
                result = dict()

                if len(splittedDialogue) < self.minHeaderCount:
                    error = 'El diálogo {0} no cumple con el mínimo número de columnas'.format(splittedDialogue[0])
                    raise ZeroDivisionError(error)

                headerIdx = 0
                for header in self.headers:
                    result[header] = splittedDialogue[headerIdx].strip()
                    headerIdx += 1
                    
                self.dialogues.append(result)


        def GetNextDialogue(self):
            self.currentDialogue += 1
            return self.dialogues[self.currentDialogue]            