init python:
    class DialogueGenerator:
        def __init__(self, fileName):
            self.minHeaderCount = 10
            self.dialogues = []
            f = open(renpy.loader.transfn("dialogues/" + fileName), mode="r", encoding='utf-8')
            lines = f.readlines()
            f.close()

            self.headers = [s.strip().replace('\ufeff', '') for s in lines[0].split(';')]

            self.dialogues = lines[1:] # Ignoramos la primera fila que es la leyenda
            f.close()
            self.generator = self.getNextDialogue()

        def getNextDialogue(self):
            for dialogue in self.dialogues:
                splittedDialogue = [d.strip() for d in dialogue.split(';')]
                result = dict()
                if len(splittedDialogue) < self.minHeaderCount:
                    error = 'El diálogo {0} no cumple con el mínimo número de columnas'.format(splittedDialogue[0])
                    raise ZeroDivisionError(error)

                headerIdx = 0
                for header in self.headers:
                    result[header] = splittedDialogue[headerIdx].strip()
                    headerIdx += 1
                    
                yield result