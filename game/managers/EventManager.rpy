init python:
    class EventManager:
        def __init__(self):
            self.prepared = False
            self.characterSpawnEvents = ['appear', 'pop']
            self.characterActionsEvents = ['move', 'jump', 'shake', 'destroy', 'zoom']
            self.defaultCharacterSpawn = self.characterSpawnEvents[0]
            self.defaultCharacterSpawnTime = 2
            self.defaultCharacterXPos = 50

            self.onScreenCharacters = []
            self.newCharacterQueue = []
            self.onScreenCharacterQueue = []
        
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

                fullname = (character_name + ' ' + sprite).strip()
                
                if not renpy.has_image(fullname):
                    raise Exception('El sprite "' + sprite + '" del personaje "' + character_name + '" no existe') 

                currentEvent = {
                    'character_name': character_name,
                    'fullname': fullname,
                    'splits': splits[1:],
                }  

                if character_name not in self.onScreenCharacters:
                    self.PrepareNewCharacter(currentEvent)
                else:
                    self.PrepareCharacterOnScreen(currentEvent)

                params = []
                if len(splits) > 2:
                    params =  splits[2:]

                currentEvent = {
                    'character_name': character_name,
                    'fullname': fullname,
                    'sprite': sprite,
                    'params': params,
                }

                if character_name not in self.onScreenCharacters:
                    # The character aren't on the screen
                           
                    
                else:
                    # The character are on screen

                    

                currentEvent['action'] = action
                self.eventQueue.append(currentEvent)

        def PrepareNewCharacter(eventData):
            spawnMethod = self.defaultCharacterSpawn

            if len(eventData['params']) >= 1:
                spawnMethod = eventData['params'][0]

            if spawnMethod not in self.characterSpawnEvents:
                raise Exception('El método de aparición "' + action + '" para el personaje "' + character_name + '" no existe')             

            self.newCharacterQueue.append(eventData)

        def PrepareCharacterOnScreen(eventData):
            if len(eventData['params']) == 0:
                # It's a sprite change
                self.onScreenCharacterQueue.append(eventData)
                return

            if len(eventData['params']) === 1:
                if eventData['params'].isnumeric():
                    # It's a sprite change
                    self.onScreenCharacterQueue.append(eventData)
                    return

            action = eventData['params'][0]
            if action not in self.characterActionsEvents:
                raise Exception('La acción "' + action + '" para el personaje "' + character_name + '" no existe')

            self.onScreenCharacterQueue.append(eventData)

        def HandleEvents(self):
            self.prepared = False

            for event in self.eventQueue:
                if event['character_name'] not in self.onScreenCharacters:
                    # The character aren't on the screen
                    xposition = self.defaultCharacterXPos
                    dissolveTime = self.defaultCharacterSpawnTime

                    if len(event['params']) == 1:
                        xposition = float(event['params'][0])

                    if len(event['params']) == 2:
                        dissolveTime = float(event['params'][1])

                    if event['action'] == 'pop':
                        dissolveTime = 0

                    animation = Dissolve(dissolveTime)
                    position = Position(xalign=xposition / 100, yalign=1)

                    
                    renpy.show(event['fullname'], at_list=[position])
                    renpy.with_statement(animation)
                    self.onScreenCharacters.append(event['character_name'])
                else:
                    # The character are on screen
                    if 'action' not in event:
                        # It's a sprite change
                        renpy.show(event['fullname'])
                        return

                    
                    movement = Transform(xalign=100, duration=1.5)
                    renpy.show('saijo', at_list=[movement])

            
            self.eventQueue = []