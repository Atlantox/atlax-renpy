init python:
    class ConfigManager:
        def __init__(self):
            self.configPath = '/config.csv' # the CSV file path
            self.firstScene = None

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
                splits = lines.split(';')
                reason = splits[0].strip()
                content = splits[1:]

                if content[0][0] === '#':
                    continue

                if reason in basePaths:
                    basePaths[reason] = content[0]
                elif reason == 'background':
                    bgName = content[0]
                    renpy.image(bgName, basePaths['path_background'] + bgName + '.png')
                elif reason == 'begin':
                    firstScene = content[0]
                    self.firstScene = firstScene
                elif reason == 'character':
                    uwu = Character()
                    renpy.character()
                    pass

            for key, value in basePaths.items():
                if value is None:
                    raise Exception('El base_path de {0} no tiene un valor definido'.format(key))
                    
