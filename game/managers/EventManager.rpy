init python:
    class EventManager:
        def __init__(self):
            self.prepared = False
            self.characterSpawnEvents = ['appear', 'pop']
            self.characterActionsEvents = ['move', 'jump', 'shake', 'destroy', 'zoom']
            self.defaultCharacterSpawn = self.characterSpawnEvents[0]
            self.defaultCharacterXPos = 50
            self.defaultCharacterYPos = 100

            self.onScreenCharacters = []
            self.eventQueue = []
        
        def PrepareEvents(self, eventPrompt:str):
            self.prepared = True
            recievedEvents = [e.strip() for e in eventPrompt.split(',')]

            for event in recievedEvents:
                splits = [e.strip() for e in event.split(':')]
                first_split = splits[0]

                character_data = [s.strip() for s in first_split.split(' ')]
                character_name = character_data[0]

                if(character_name not in globals()):
                    raise Exception('El personaje "' + character_name + '" no está definido, verifica que el nombre está bien escrito')

                sprite = ''
                if len(character_data) > 1:
                    sprite = first_split[len(character_name) + 1:]

                if not renpy.has_image((character_name + ' ' + sprite).strip()):
                    raise Exception('El sprite "' + sprite + '" del personaje "' + character_name + '" no existe')

                action = self.defaultCharacterSpawn
                if len(splits) == 3:
                    action = splits[2]

                params = []
                if len(splits) > 3:
                    params =  splits[3:]

                currentEvent = {
                    'character_name': character_name,
                    'sprite': sprite,
                    'action': action,
                    'params': params,                    
                }

                if character_name not in self.onScreenCharacters:
                    # The character aren't on the screen
                    spawnMethod = action
                    if spawnMethod not in self.characterSpawnEvents:
                        raise Exception('El método de aparición "' + spawnMethod + '" para el personaje "' + character_name + '" no existe')

                    currentEvent['spawnMethod'] = spawnMethod                   
                    
                else:
                    # The character are on screen
                    if currentEvent['action'] in self.characterSpawnEvents:
                        raise Exception('La acción de aparición "' + currentEvent['action'] + '" para el personaje "' + character_name + '" es inválida (ya está en escena)')

                    if currentEvent['action'] not in self.characterActionsEvents:
                        raise Exception('La acción "' + currentEvent['action'] + '" para el personaje "' + character_name + '" no existe')

                self.eventQueue.append(currentEvent)

        def HandleEvents(self):
            self.prepared = False

            for event in self.eventQueue:
                di = Dissolve(5)
                renpy.show(event['character_name'])
                renpy.with_statement(di)
                continue
                if event['character_name'] not in self.onScreenCharacters:
                    # The character aren't on the screen
                    pass
                else:
                    # The character are on screen
                    pass
                    '''
                    xposition = self.defaultCharacterXPos
                        yposition = self.defaultCharacterYPos
                        if len(params) >= 1:
                            xposition = float(params[0])

                        if len(params) >= 2:
                            yposition = float(params[1])

                        xposition /= 100
                        yposition /= 100

                        position = Position(xalign=xposition, yalign=yposition)
                        renpy.show(character + sprite, at_list=[position])
                    '''

            
            self.eventQueue = []