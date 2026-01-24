define saijo = Character('Saijo', color='#8709B4')
define mutou = Character('Mutou', color='#2595d2')
define dereck = Character('Dereck', color='#e4e159')
define keiko = Character('Keiko', color='#b1b1b1')

define berto = Character('Berto', color='#8709B4')

# Ejemplo1
define katy = Character('Katy', color='#ff3d3d')
define mesero = Character('Mesero', color='#19f060')
define tableman = Character('Tableman', color='#19f060')
define mechero = Character('Mechero', color='#19f060')

# Ejemplo2
define rafarencio = Character('Rafarencio', color='#ffad65')
define unknown = Character('???', color='#ffffff')
define instructor = Character('Instructor', color='#c6c6c6')
define furious_soldier = Character('Soldado furioso', color='#ff6060')
define soldier = Character('Soldado', color='#ff6060')
define flint = Character('Flint', color='#396c97')
define flint = Character('Flint', color='#396c97')

define characters = {
    '*': None,
    '': None,

    'saijo': saijo,
    'mutou': mutou,
    'dereck': dereck,
    'keiko': keiko,

    'berto': berto,

    # Ejemplo1
    'katy':katy,
    'mesero': mesero,
    'tableman': tableman,
    'mechero': mechero,

    # Ejemplo2
    'rafarencio': rafarencio,
    'instructor': instructor,
    '???': unknown,
    'obrero': flint,
    'flint': flint,
    'soldado furioso': furious_soldier,
    'soldado': soldier,
}

define languageDependingNames = {
    'mesero': {
        'Spanish': 'mesero',
        'English': 'tableman',
        'Chinese': 'mechero'
    },

    'instructor': {
        'Spanish': 'instructor',
        'English': 'instructor',
        'Chinese': 'instructor'
    },
    
}