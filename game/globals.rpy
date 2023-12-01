init python:    
    class DialogueGenerator:
        def __init__(self, fileName):
            self.sentences = []
            f = open(renpy.loader.transfn("dialogues/" + fileName),"r")
            self.sentences = f.readlines()[1:] # Ignoramos la primera fila que es la leyenda
            f.close()
            self.generator = self.getNextDialogue()

        def getNextDialogue(self):
            for sentence in self.sentences:
                yield sentence.split(';')[currentLanguage + 2]