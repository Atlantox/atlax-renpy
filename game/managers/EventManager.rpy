init python:
    class EventManager:
        def __init__(self):
            self.prepared = False
            self.characterSpawnEvents = ['appear', 'pop']
            self.characterAnimations = ['jump', 'tremble', 'zoom', 'hitl', 'hitr', 'knockl', 'knockr', 'raiser', 'raisel', 'movey', 'dodge', 'attack']           
            self.characterContinuousEvents = ['jumping', 'trembling']
            self.characterActionsEvents = ['move', 'destroy', 'behind'] + self.characterAnimations + self.characterContinuousEvents
            self.fixedHeight = Transform(size=(None, config.screen_height), anchor=(0.5, 0.0),)

            #  Default spawn values
            self.defaultCharacterSpawn = self.characterSpawnEvents[0]
            self.defaultCharacterSpawnTime = 2
            self.defaultCharacterAppearTime = 1.25
            self.defaultCharacterAppearPosition = 0.5

            #  Default event values
            self.defaultSpriteChangeTime = 0
            self.defaultMovementTime = 1
            self.defaultCharacterMovementTime = 1.5
            self.defaultJumpIntensity = 0.025
            self.defaultTrembleTimes = 10
            self.defaultHitIntensity = 10
            self.defaultKnockDuration = 0.5
            self.defaultRaiseDuration = 0.5
            self.defaultMoveYDuration = 0.5
            self.defaultZoomFactor = 2
            self.defaultZoomDuration = 2
            self.defaultDestroyCharacterTime = 0
            self.defaultZPosition = 0

            self.multiCharacterAppearPositions = {
                '1': [0.5],
                '2': [0.25, 0.75],
                '3': [0.1, 0.5, 0.9],
                '4': [0.0, 0.35, 0.7, 1.0]
            }

            self.oneParameterEvents = {
                'jump' : Jump, 
                'tremble': Tremble, 
                'hitl': HitL, 
                'hitr': HitR, 
                'knockl': KnockL, 
                'knockr': KnockR, 
                'raisel': RaiseL, 
                'raiser': RaiseR,

                
            }

            self.twoParameterEvents = {
                'zoom': MyZoom,
                'dodge': Dodge,
                'attack': Attack
            }

            self.onScreenCharacters = []
            self.characterProperties = {}
            self.continuousEvents = {}

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
                raise Exception('La acción "' + action + '" para los personajes "' + str(buffer['characters']) + '" no existe')

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

                positionId = 0
                spawnPositions = self.multiCharacterAppearPositions[str(len(event['characters']))]
                for character in event['characters']:
                    if(len(event['characters']) == 1):
                        fixedPosition = appearPosition
                    else:
                        fixedPosition = spawnPositions[positionId]
                        positionId += 1

                    position = Position(xalign=fixedPosition)
                    self.ShowCharacter(character['fullname'], [position, self.fixedHeight])

                    if(len(event['characters']) == 1):
                        renpy.with_statement(Dissolve(appearTime))

                    self.onScreenCharacters.append(character['name'])
                    self.characterProperties[character['name']] = {}
                    self.characterProperties[character['name']]['x'] = fixedPosition
                    self.characterProperties[character['name']]['y'] = 0.0
                    self.characterProperties[character['name']]['behind'] = []
                    self.characterProperties[character['name']]['zoom'] = 1.0
                
                if(len(event['characters']) > 1):
                    renpy.with_statement(Dissolve(multiAppearTime))

            self.newCharactersQueue = []               

        def HandleActionEvents(self):
            for event in self.onScreenCharactersQueue:
                if event['action'] in self.oneParameterEvents:
                    self.HandleOneParameterEvent(event)
                elif event['action'] in self.twoParameterEvents:
                    self.HandleTwoParametersEvent(event)
                elif event['action'] == 'sprite':
                    self.HandleSpriteChange(event)
                elif event['action'] == 'move':
                    self.HandleMovement(event)
                elif event['action'] == 'movey':
                    self.HandleMoveY(event)
                elif event['action'] == 'destroy':
                    self.HandleDestroy(event)
                elif event['action'] == 'behind':
                    self.HandleBehind(event)

                if event['action'] in self.characterContinuousEvents:
                    self.HandleContinuousEffect(event)
                    
            self.onScreenCharactersQueue = []

        def HandleSpriteChange(self, event):
            changeTime = self.defaultSpriteChangeTime

            if len(event['params']) > 0:
                changeTime = float(event['params'][0])

            for character in event['characters']:
                self.ShowCharacter(character['fullname'])

            renpy.with_statement(Dissolve(changeTime))

        def HandleMovement(self, event):            
            movements = {}
            characterCount = len(event['characters'])
            duration = self.defaultCharacterMovementTime
            

            if characterCount == 1:
                position = float(event['params'][1]) / 100
                newPosition = Position(xalign=position)
                
                if len(event['params']) > 2:
                    duration = float(event['params'][2])

                character = event['characters'][0]
                movements[character['fullname']] = dict(newPosition=newPosition, x=position)
            else:
                i = 0
                params = event['params'][1:]
                for character in event['characters']:
                    position = float(params[i]) / 100
                    newPosition = Position(xalign=position)

                    movements[character['fullname']] = dict(newPosition=newPosition, x=position)
                    i += 1

                if len(params) > i:
                    duration = float(params[i])
            

            for character, positionData in movements.items():
                self.ShowCharacter(character, [positionData['newPosition'], self.fixedHeight])
                characterName = character.split(' ')[0]
                self.characterProperties[characterName]['x'] = positionData['x']

            renpy.with_statement(MoveTransition(duration, enter_time_warp=_warper.easein, leave_time_warp=_warper.easein))
        
        def HandleOneParameterEvent(self, event):            
            params = self.GetDefaultParametersOfAnimation(event['action'])

            if len(event['params']) > 1:
                params[0] = float(event['params'][1])

            for character in event['characters']:
                self.DestroyCharacter(character['name'])
                params = [self.characterProperties[character['name']]['x']] + params
                animation = self.oneParameterEvents[event['action']](*params)
                self.ShowCharacter(character['fullname'], [animation, self.fixedHeight])

        def HandleTwoParametersEvent(self, event):            
            params = self.GetDefaultParametersOfAnimation(event['action'])

            if len(event['params']) > 1:
                params[0] = float(event['params'][1])

            if len(event['params']) > 2:
                params[1] = float(event['params'][2])

            for character in event['characters']:
                animation = self.twoParameterEvents[event['action']](*params)
                self.ShowCharacter(character['name'], [animation])

                if event['action'] == 'zoom':
                    self.characterProperties[character['name']]['zoom'] = params[1]

        def HandleBehind(self, event):
            behind = []
            if len(event['params']) > 1:
                behind = [p.strip() for p in event['params'][1].split(',')]                

            for character in event['characters']:
                self.characterProperties[character['name']]['behind'] = behind
                self.ShowCharacter(character['name'])

        def GetDefaultParametersOfAnimation(self, animation):
            params = []

            if animation == 'jump':
                params.append(self.defaultJumpIntensity)
            elif animation == 'tremble':
                params.append(self.defaultTrembleTimes)
            elif animation in ['hitr', 'hitl']:
                params.append(self.defaultHitIntensity)
            elif animation in ['knockr', 'knockl']:
                params.append(self.defaultKnockDuration)
            elif animation in ['raiser', 'raisel']:
                params.append(self.defaultRaiseDuration)
            elif animation == 'zoom':
                params.append(self.defaultZoomFactor)
                params.append(self.defaultZoomDuration)

            return params

        def HandleMoveY(self, event):
            yPos = float(event['params'][1])
            duration = self.defaultMovementTime

            if len(event['params']) > 2:
                duration = float(event['params'][2])

            for character in event['characters']:
                self.DestroyCharacter(character['name'])
                movement = MoveY(
                    self.characterProperties[character['name']]['x'],
                    self.characterProperties[character['name']]['y'],
                    yPos, 
                    duration)
                
                self.ShowCharacter(character['name'], [movement, self.fixedHeight])
                self.characterProperties[character['name']]['y'] = yPos

        def HandleDestroy(self, event):
            duration = self.defaultDestroyCharacterTime

            if len(event['params']) > 1:
                duration = float(event['params'][1])
            
            for character in event['characters']:
                self.DestroyCharacter(character['name'], duration)
                del self.characterProperties[character['name']]
                del self.onScreenCharacters[self.onScreenCharacters.index(character['name'])]

        def DestroyCharacter(self, character, duration = 0):
            renpy.show(character, at_list=[DisappearCharacter(duration)])
            renpy.pause(duration * 1.1)
            renpy.hide(character)

        def HandleContinuousEffect(self, event):
            for character in event['characters']:
                self.DestroyCharacter(character['name'])                

            if event['action'] == 'jumping':
                self.HandleJumping(event)
            elif event['action'] == 'trembling':
                self.HandleTrembling(event)

            for character in event['characters']:
                if character['name'] in self.continuousEvents:
                    del self.continuousEvents[character['name']]
                else:
                    self.continuousEvents[character['name']] = event['action']                    

        def HandleJumping(self, event):
            intensity = self.defaultJumpIntensity

            if len(event['params']) > 1:
                intensity = float(event['params'][1])

            for character in event['characters']:
                if character['name'] in self.continuousEvents:
                    self.ResetCharacterPosition(character)
                else:
                    animation = Jumping(self.characterProperties[character['name']]['x'], intensity)
                    self.ShowCharacter(character['name'], [animation, self.fixedHeight])
            
        def HandleTrembling(self, event):
            for character in event['characters']:
                if character['name'] in self.continuousEvents:
                    self.ResetCharacterPosition(character)
                else:
                    animation = Trembling(self.characterProperties[character['name']]['x'])
                    self.ShowCharacter(character['name'], [animation, self.fixedHeight])

        def ResetCharacterPosition(self, character):
            position = Position(xalign=self.characterProperties[character['name']]['x'])
            self.ShowCharacter(character['fullname'], [position, self.fixedHeight])
            renpy.with_statement(Dissolve(0))

        def ShowCharacter(self, character, at_list = []):
            final_at_list = at_list
            behind = []

            if character in self.onScreenCharacters:
                characterProperties = self.characterProperties[character]
                behind = characterProperties['behind']
                
                initialPosition = SetCharacterProperties(
                    characterProperties['x'],
                    characterProperties['y'],
                    characterProperties['zoom'],
                )
                final_at_list = [initialPosition] + at_list

            renpy.show(character, at_list=final_at_list, behind=behind)


        def DestroyAllCharacters(self):
            for character in self.onScreenCharacters:
                eventManager.DestroyCharacter(character, 2)

        def ResetEventManager(self):
            self.onScreenCharacters = []
            self.characterProperties = {}
            self.continuousEvents = {}