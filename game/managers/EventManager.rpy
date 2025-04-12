init python:
    class EventManager:
        def __init__(self):
            self.prepared = False
            self.characterSpawnEvents = ['appear', 'pop']
            self.characterActionsEvents = ['move', 'jump', 'shake', 'destroy', 'zoom']

            self.defaultCharacterSpawn = self.characterSpawnEvents[0]
            self.defaultCharacterSpawnTime = 2
            self.defaultCharacterAppearTime = 1.25
            self.defaultCharacterAppearPosition = 50

            self.defaultSpriteChangeTime = 0
            self.defaultMovementTime = 1
            self.defaultCharacterMovementTime = 1.5


            self.multiCharacterAppearPositions = {
                '2': [25, 75],
                '3': [20, 50, 80],
                '4': [10, 40, 70, 90]
            }            

            self.onScreenCharacters = []
            self.characterPositions = {}

            self.newCharactersQueue = []
            self.onScreenCharactersQueue = []
        
        def PrepareEvents(self, eventPrompt:str):
            self.prepared = True
            recievedEvents = [e.strip() for e in eventPrompt.split(',')]

            for event in recievedEvents:
                splits = [e.strip() for e in event.split(':')]
                first_split = splits[0]

                final_characters = []
                characters = [s.strip() for s in first_split.split('&')]
                for character in characters:                    
                    character_data = [s.strip() for s in character.split(' ')]
                    character_name = character_data[0]

                    if(character_name not in globals()):
                        raise Exception('El personaje "' + character_name + '" no está definido, verifica que el nombre está bien escrito')

                    sprite = ''
                    if len(character_data) > 1:
                        sprite = ''.join(character_data[1:])

                    fullname = (character_name + ' ' + sprite).strip()
                
                    if not renpy.has_image(fullname):
                        raise Exception('El sprite "' + sprite + '" del personaje "' + character_name + '" no existe') 

                    final_characters.append({
                        'name': character_name,
                        'fullname': fullname,    
                    })

                currentEvent = {
                    'characters': final_characters,
                    'params': splits[1:],
                }  

                if final_characters[0]['name'] not in self.onScreenCharacters:
                    self.PrepareNewCharacter(currentEvent)
                else:
                    self.PrepareCharacterOnScreen(currentEvent)

        def PrepareNewCharacter(self, eventData):
            spawnMethod = self.defaultCharacterSpawn

            if len(eventData['params']) >= 1:
                spawnMethod = eventData['params'][0]

            if spawnMethod not in self.characterSpawnEvents:
                raise Exception('El método de aparición "' + action + '" para el personaje "' + character_name + '" no existe')             

            buffer = eventData
            buffer['spawnMethod'] = spawnMethod
            self.newCharactersQueue.append(buffer)

        def PrepareCharacterOnScreen(self, eventData):
            buffer = eventData
            buffer['action'] = 'sprite'

            if len(buffer['params']) == 0:
                # It's a sprite change
                self.onScreenCharactersQueue.append(buffer)
                return

            if len(buffer['params']) == 1:
                if buffer['params'][0].isnumeric(): # The param is the sprite change duration
                    # It's a sprite change
                    self.onScreenCharactersQueue.append(buffer)
                    return

            action = buffer['params'][0]
            if action not in self.characterActionsEvents:
                raise Exception('La acción "' + action + '" para el personaje "' + character_name + '" no existe')

            buffer['action'] = action
            self.onScreenCharactersQueue.append(buffer)

        def HandleEvents(self):
            self.prepared = False

            self.HandleSpawnEvents()
            self.HandleActionEvents()

        def HandleSpawnEvents(self):
            for event in self.newCharactersQueue:
                appearTime = self.defaultCharacterAppearTime
                multiAppearTime = self.defaultCharacterAppearTime
                appearPosition = self.defaultCharacterAppearPosition                
                
                if event['spawnMethod'] == 'pop':
                    appearTime = 0
                    multiAppearTime = 0
                    if len(event['params']) > 1:
                        appearPosition = float(event['params'][1])
                else:
                    if len(event['params']) > 1:
                        appearPosition = int(event['params'][1])
                        multiAppearTime = appearPosition                     

                    if len(event['params']) > 2:
                        appearTime = float(event['params'][2])                       

                
                if(len(event['characters']) == 1):
                    fixedPosition = appearPosition / 100
                    position = Position(xalign=fixedPosition)
                    character = event['characters'][0]
                    renpy.show(character['fullname'], at_list=[position])
                    renpy.with_statement(Dissolve(appearTime))
                    self.onScreenCharacters.append(character['name'])
                    self.characterPositions[character['name']] = fixedPosition
                else:
                    spawnPositions = self.multiCharacterAppearPositions[str(len(event['characters']))]
                    positionId = 0                    
                    for character in event['characters']:
                        fixedPosition = spawnPositions[positionId] / 100
                        position = Position(xalign=fixedPosition)
                        renpy.show(character['fullname'], at_list=[position])
                        positionId += 1
                        self.onScreenCharacters.append(character['name'])
                        self.characterPositions[character['name']] = fixedPosition

                    renpy.with_statement(Dissolve(multiAppearTime))

            self.newCharactersQueue = []               


        def HandleActionEvents(self):
            for event in self.onScreenCharactersQueue:
                if event['action'] == 'sprite':
                    self.HandleSpriteChange(event)
                elif event['action'] == 'move':
                    self.HandleMovement(event)

                    
            self.onScreenCharactersQueue = []

        def HandleSpriteChange(self, event):
            changeTime = self.defaultSpriteChangeTime

            if len(event['params']) > 0:
                changeTime = float(event['params'][0])

            for character in event['characters']:
                renpy.show(character['fullname'])

            renpy.with_statement(Dissolve(changeTime))

        def HandleMovement(self, event):
            newPosition = float(event['params'][1]) / 100
            newPosition = Position(xalign=newPosition)
            
            duration = self.defaultCharacterMovementTime

            if len(event['params']) > 2:
                duration = float(event['params'][2])

            for character in event['characters']:
                currentPosition = self.characterPositions[character['name']]
                
                #currentPosition = Position(xalign=currentPosition, yalign=1)
                #movement = Interpolator(currentPosition, newPosition, duration)
                renpy.show(character['fullname'], at_list=[newPosition])
                renpy.show('mutou', at_list=[newPosition])
                renpy.with_statement(MoveTransition(duration))
                
            