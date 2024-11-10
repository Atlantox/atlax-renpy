init python:
    class DialogueGenerator:
        def __init__(self, fileName):
            self.dialogues = []
            f = open(renpy.loader.transfn("dialogues/" + fileName),"r")
            lines = f.readlines()
            f.close()

            self.headers = [s.strip() for s in lines[0].split(';')]

            self.dialogues = lines[1:] # Ignoramos la primera fila que es la leyenda
            f.close()
            self.generator = self.getNextDialogue()

        def getNextDialogue(self):
            for dialogue in self.dialogues:
                splittedDialogue = dialogue.split(';')
                result = dict()
                if len(splittedDialogue) != len(self.headers):
                    raise ZeroDivisionError('El diálogo {0} tiene distintas columnas que la cabecera'.format(splittedDialogue[0]))

                headerIdx = 0
                for header in self.headers:
                    result[header] = splittedDialogue[headerIdx].strip()
                    headerIdx += 1
                    
                yield result