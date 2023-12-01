label start_my_scene11:
    $ dialogueGenerator = DialogueGenerator('my_scene1.csv')
    show sex dungeon
    show saijo
    
    $ d = next(dialogueGenerator.generator)
    saijo "[d]"
    $ d = next(dialogueGenerator.generator)
    saijo "[d]"
    $ d = next(dialogueGenerator.generator)
    saijo "[d]"
    $ d = next(dialogueGenerator.generator)
    saijo "[d]"