init -10 python:
    class ConfigManager:
        def __init__(self):
            self.configPath = '/config2.csv' # the CSV config file path
            self.allLanguages = []
            self.firstScene = None

            self.basePaths = {
                'path_background': None,
                'path_sound': None,
                'path_music': None,
                'path_scene': None,
                'path_displayable': None
            }

            self.characterDefinitions = {
                '*': None,
                '': None,
            }
            self.configHeaders = []

        def Loadconfig(self):
            rawConfig = self.OpenCSVFile(self.configPath)

            lines = rawConfig.strip().split('\n')
            heading = lines[0] # The first line are the headers
            lines = lines[1:] # The rest of the lines

            self.configHeaders = [s.strip().replace('\ufeff', '') for s in heading.split(';')]

            for header in self.configHeaders:
                if header not in ['Key', 'Value1', 'Value2']:
                    if header not in self.allLanguages:
                        self.allLanguages.append(header)

            for line in lines:
                if line[0] == '#':
                    continue

                configPrompt = self.GetHeadedContent(line)

                if configPrompt['Key'] in self.basePaths:
                    self.basePaths[configPrompt['Key']] = configPrompt['Value1']
                elif configPrompt['Key'] == 'background':
                    bgName = configPrompt['Value1']
                    renpy.image('bg ' + bgName, self.basePaths['path_background'] + bgName + '.png')
                elif configPrompt['Key'] == 'begin':
                    firstScene = configPrompt['Value1']
                    self.firstScene = firstScene
                elif configPrompt['Key'] == 'character':
                    self.ProcessCharacter(configPrompt)                    

            self.CheckAllPathsExists()

        def ProcessCharacter(self, prompt):
            appearTimes = 0
            firstAppear = None
            for language in self.allLanguages:
                if language in prompt:
                    if prompt[language] != '':
                        appearTimes += 1
                        if firstAppear is None:
                            firstAppear = language

            if appearTimes == 0 and firstAppear is None:
                error = 'El personaje ' + prompt['Value1'] + ' no tiene ni una variación de nombre. '
                error += 'Datos: ' + str(prompt)
                raise Exception(error)

            characterConfig = {'Original': Character(prompt[firstAppear], color=prompt['Value2'])}

            for language in self.allLanguages:
                if prompt[language] != '': # If a language variation is empty, take the first one
                    characterConfig[language] = Character(prompt[language], color=prompt['Value2'])

            self.characterDefinitions[prompt['Value1']] = characterConfig            

        def GetHeadedContent(self, line):
            result = {}
            splittedContent = line.split(';')
            for i in range(len(splittedContent)):
                if i > len(self.configHeaders) - 1:
                    error = 'Una fila del archivo de control presenta un número de columnas distintas al de la cabecera. '
                    error += 'Fila: ' + str(splittedContent)
                    raise Exception(error)

                result[self.configHeaders[i]] = splittedContent[i]

            return result

        def CheckAllPathsExists(self):
            for key, value in self.basePaths.items():
                if value is None:
                    error = 'Una ruta base está sin definir: ' + key
                    raise Exception(error)                    

        def OpenCSVFile(self, path):
            if renpy.mobile:
                rawContent = renpy.file(path, encoding="utf-8")
                rawContent = rawContent.read()
            else:
                with open(renpy.loader.transfn(path), mode="r", encoding="utf-8") as f:
                    rawContent = f.read()
                    f.close()

            return rawContent
