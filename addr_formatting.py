def extend_street_abrev(abreviation):
    '''
    Return the full name for a street abreviation
    '''
    abrev_dict = {'AVE': "Avenue", 
        'BLVD': 'Boulevard',
        'CIR': 'Circle',
        'CT': 'Court',
        'DR': 'Drive',
        'LN': 'Lane',
        'LOOP': 'Loop',
        'PASS': 'Pass',
        'PKWY': 'Parkway',
        'PL': 'Place',
        'RD': 'Road',
        'RDGE': 'Ridge',
        'RUN': 'Run',
        'ROW': 'Row',
        'ST': 'Street',
        'SQ': 'Square',
        'TER': 'Terrace',
        'TERR': 'Terrace',
        'TRL': 'Trail',
        'WAY': 'Way'}
    return abrev_dict[abreviation.upper()]

def extend_dir_abrev(abreviation):
    '''
    Return the full name for a cardinal direction
    '''
    abrev_dict = {'N': "North", 'S': 'South', 'E': 'East', 'W': 'West', 'NE': "Northeast", 'SE': 'Southeast', 'SW': 'Southwest', 'NW': 'Northwest'}
    return abrev_dict[abreviation.upper()]

def format_street(street, streettype = '', direction = '', p_direction = ''):
    '''
    Given the name of the street, and a possible streettype (Street, Avenue, etc), direction, and post direction
    Give the name of the street to go into OSM
    '''
    if street[0].isnumeric():
        street = street.lower()
    else:
        street = street.title()
    full_name = ''
    if direction != '':
        full_name += extend_dir_abrev(direction) + ' '
    full_name += street
    if streettype != '':
        full_name += ' ' + extend_street_abrev(streettype)
    if p_direction != '':
        full_name += ' ' + extend_dir_abrev(p_direction)
    return full_name

def format_housenumber(housenumber, extension = ''):
    '''
    Given a housenumber and a possible extension, return the housenumber for OSM
    '''
    if extension == '':
        return housenumber
    if extension == '1/2':
        extension = ' 1/2'
    return housenumber + extension

def cut_zip(zipcode):
    '''
    Given a zip+4 return a 5 digit zip code
    '''
    if len(zipcode) == 9:
        return zipcode[:5]
    return zipcode
    
def format_zip(zipcode):
    '''
    Correct the formattting of zip+4 zip codes
    '''
    if len(zipcode) == 9:
        return zipcode[:5] + '-' + zipcode[5:]
    return zipcode