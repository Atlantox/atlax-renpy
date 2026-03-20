init python:
    class ConfigManager:
        def __init__(self):
            self.configPath = '/config.csv' # the CSV file path
            self.firstDialogue = None

        def Loadconfig(self):
            if renpy.mobile:
                rawConfig = renpy.file(self.configPath, encoding="utf-8")
                rawConfig = rawConfig.read()
            else:
                with open(renpy.loader.transfn(self.configPath), mode="r", encoding="utf-8") as f:
                    rawConfig = f.read()
                    f.close()

            lines = sceneContent.strip().split('\n')

            for line in lines:
                self.ProcessConfigStatement(line)

        def ProcessConfigStatement(self, prompt):
            splits = prompt.split(';')
            reason = splits[0].strip()
            content = splits[1:]

            if reason == 'background':
                pass
            elif reason == 'begin':
                pass
            elif reason == 'character':
                pass
            
