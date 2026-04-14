import os


def main():
    print(PathIsCorrect())

def PathIsCorrect():
    return ( 
        os.path.isdir('game') 
        and 
        os.path.exists(os.path.join(os.getcwd(), 'game/screens.rpy')) 
    )

if __name__ == '__main__':
    main()