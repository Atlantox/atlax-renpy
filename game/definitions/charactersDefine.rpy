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
define worker = Character('Obrero', color='#396c97')

define characters = {
    '*': None,
    '': None,

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
    'obrero': worker,
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