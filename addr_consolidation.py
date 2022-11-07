import csv

from cv2 import add
import xml.etree.ElementTree as ET
import find_address

def extend_street_abrev(abreviation):
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
    abrev_dict = {'N': "North", 'S': 'South', 'E': 'East', 'W': 'West', 'NE': "Northeast", 'SE': 'Southeast', 'SW': 'Southwest', 'NW': 'Northwest'}
    return abrev_dict[abreviation.upper()]

def format_street(street, streettype = '', direction = '', p_direction = ''):
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
    if extension == '':
        return housenumber
    if extension == '1/2':
        extension = ' 1/2'
    return housenumber + extension

def cut_zip(zipcode):
    if len(zipcode) == 9:
        return zipcode[:5]
    return zipcode
    
def format_zip(zipcode):
    if len(zipcode) == 9:
        return zipcode[:5] + '-' + zipcode[5:]
    return zipcode

def get_housenum_value(housenumber):
    housenumber = housenumber.strip()
    if housenumber.isnumeric():
        return int(housenumber)
    if housenumber[-4:] == ' 1/2':
        return get_housenum_value(housenumber[:-4]) + 0.5
    return get_housenum_value(housenumber[:-1]) + 0.1


def combine_housenumbers(housenumbers):
    housenumbers = (','.join(housenumbers)).split(',')
    housenumbers = [x.strip() for x in housenumbers]
    housenumbers = list(set(housenumbers))
    housenumbers.sort(key=get_housenum_value)
    return ','.join(housenumbers)

def combine_zips(zips):
    if len(zips) == 0:
        return ''
    if len(zips) == 1:
        return zips[0]
    zip1 = zips[0]
    zip2 = combine_zips(zips[1:])
    if zip1 == zip2:
        return zip1
    if len(zip1) not in [5,10]:
        return ''
    if len(zip2) not in [5,10]:
        return ''
    if len(zip1) == len(zip2) == 5:
        return ''
    if len(zip1) == len(zip2) == 10:
        if zip1[:5] == zip2[:5]:
            return zip1[:5]
        return 0
    longer = zip1 if len(zip1) > len(zip2) else zip2
    shorter = zip1 if len(zip1) < len(zip2) else zip2

    if longer[:5] == shorter:
        return shorter
    return ''


def combine_units(units):
    units = (','.join(units)).split(',')
    units = [x.strip() for x in units]
    units = list(set(units))
    units.sort(key=get_housenum_value)
    return ','.join(units)


def combine_cities(cities):
    if len(set(cities)) == 1:
        return cities[0]
    return ''

def find_dupes_csv():
    # opening the CSV file
    with open('Address_Points.csv', mode ='r') as file:   
            
        # reading the CSV file
        csvFile = csv.DictReader(file)
        stack_counts = {}
        # displaying the contents of the CSV file
        for lines in csvFile:
            location = lines['X'] + lines['Y']
            stack_counts.setdefault(location, 0)
            stack_counts[location] += 1

        for key in list(stack_counts):
            if stack_counts[key] < 2:
                del stack_counts[key]

    stacked_addrs = {}
    stacked_addrs_list = []
    loc_dict = {}
    name_dict = {}
    with open('Address_Points.csv', mode ='r') as file:   
        # reading the CSV file
        csvFile = csv.DictReader(file)
        # displaying the contents of the CSV file
        for lines in csvFile:
            location = lines['X'] + lines['Y']
            if len(location) == 0:
                continue
            if location not in stack_counts:
                continue
            if len(lines['STREET']) == 0 or len(lines['HOUSENO']) == 0: 
                continue
            housenumber = format_housenumber(lines['HOUSENO'], lines['HOUSESX'])
            street = format_street(lines['STREET'], lines['STTYPE'], lines['DIR'], lines['PDIR'])
            unit = lines['UNIT']
            city = lines['MUNI']
            zip = cut_zip(lines['ZIP_CODE'])
            addr_entry = {'housenumber': housenumber, 'street': street, 'unit': unit, 'city': city, 'zip': zip, 'location': location}
            stacked_addrs_list.append(addr_entry)
            loc_dict.setdefault(location, [])
            loc_dict[location].append(addr_entry)
            name_dict[housenumber+street+unit+city] = addr_entry
            
            '''
            stacked_addrs.setdefault(location, {'housenumber': [], 'street': [], 'unit': [], 'city': [], 'zip': []})
            if housenumber not in stacked_addrs[location]['housenumber']:
                stacked_addrs[location]['housenumber'].append(housenumber)
            if street not in stacked_addrs[location]['street']:
                stacked_addrs[location]['street'].append(street)
            if len(unit) > 0:
                stacked_addrs[location]['unit'].append(unit)
            if city not in stacked_addrs[location]['city']: 
                stacked_addrs[location]['city'].append(city)
            if zip not in stacked_addrs[location]['zip']:
                stacked_addrs[location]['zip'].append(zip)
            '''
    nodeid = -750000
    lowerbound, upperbound = 1, 75
    new_addrs_list_list = [[] for x in range(upperbound)]
    for i in range(lowerbound, upperbound):
        tree = ET.parse(f'addresses_tract{i}.osm')
        root = tree.getroot()
        
        for node in root:
            housenumber = street = unit = city = ''
            skip = False
            for tag in node:
                key = tag.attrib['k']
                value = tag.attrib['v']
                if key == 'addr:housenumber':
                    housenumber = value
                if key == 'addr:street':
                    street = value
                if key == 'addr:city':
                    city = value
                if key == 'addr:unit':
                    unit = value
                if key == 'note:addr':
                    skip = True
            if skip:
                continue
            new_addrs = []
            if (housenumber+street+unit+city) in name_dict :
                location = name_dict[housenumber+street+unit+city]['location']
                addrs = loc_dict[location]
                streets = set([x['street'] for x in addrs])
                
                for new_street in streets:
                    addrs_same_street = [x for x in addrs if x['street'] == new_street]
                    new_housenumber = combine_housenumbers([x['housenumber'] for x in addrs_same_street])
                    if len(new_housenumber) > 255:
                        raise Exception(f'House number too long: {housenumber} {street}: {new_housenumber} Look in {find_address.search_addr(housenumber, street)}')
                    new_city = combine_cities([x['city'] for x in addrs_same_street])
                    new_zip = combine_zips([x['zip'] for x in addrs_same_street])
                    new_addrs.append({'housenumber': new_housenumber, 'street': new_street, 'city': new_city, 'zip': new_zip})
            if len(new_addrs) < 1:
                continue
            # for the first address, put the changes into the old node
            for tag in node:
                key = tag.attrib['k']
                value = tag.attrib['v']
                if key == 'addr:housenumber':
                    tag.set('v', new_addrs[0]['housenumber'])
                if key == 'addr:street':
                    tag.set('v', new_addrs[0]['street'])
                if key == 'addr:unit':
                    # Combining unit information would be very messy and unreliable
                    # Best to leave it out
                    node.remove(tag)
                if key == 'addr:city':
                    tag.set('v', new_addrs[0]['city'])
                if key == 'addr:postcode':
                    tag.set('v', new_addrs[0]['zip'])

            for j in range(1,len(new_addrs)):
                new_addr = new_addrs[j]
                lat, lon = float(node.attrib['lat']), float(node.attrib['lon'])
                lat += (j // 2) * -0.00005
                lon += (j % 2) * -0.00005
                new_addr['lat'] = str(lat)
                new_addr['lon'] = str(lon)
                new_addr['id'] = str(nodeid)
                nodeid += 1
                new_addrs_list_list[i].append(new_addr)
        tree.write(f'addresses_tract{i}.osm')
    for i in range(lowerbound, upperbound):            
        add_addrs(new_addrs_list_list[i], f'addresses_tract{i}.osm')


            
    #diff_street_with_unit = [x for x in stacked_addrs.values() if len(x['street']) > 1 and len(x['unit']) > 1]
    #print(diff_street_with_unit)
    #filtered = [x for x in stacked_addrs.values() if '541' in x['housenumber'] and 'East Erie Street' in  x['street']]
    #print(filtered)
    #find_dup_stacked(stacked_addrs_list)
        
def add_addrs(newaddrs_list, filename):
    if len(newaddrs_list) < 1:
        return
    tree = ET.parse(filename)
    root = tree.getroot()
    
    for new_addr in newaddrs_list:
        print(new_addr['housenumber'], new_addr['street'])
        new_node = ET.SubElement(root, 'node', {'id': new_addr['id'], 'action': 'modify', 'lat': new_addr['lat'], 'lon': new_addr['lon']})
        ET.SubElement(new_node, 'tag', {'k': 'addr:housenumber', 'v': new_addr['housenumber']})
        ET.SubElement(new_node, 'tag', {'k': 'addr:street', 'v': new_addr['street']})
        ET.SubElement(new_node, 'tag', {'k': 'addr:city', 'v': new_addr['city']})
        ET.SubElement(new_node, 'tag', {'k': 'addr:state', 'v': 'WI'})
        ET.SubElement(new_node, 'tag', {'k': 'addr:postcode', 'v': new_addr['zip']})
    tree.write(filename)   


def find_dup_stacked(stacked_addrs_list):       
    for i in range(1, 75):
        tree = ET.parse(f'addresses_tract{i}.osm')
        root = tree.getroot()
        
        for node in root:
            housenumber = ''
            street = ''
            unit = ''
            city = ''
            zip = ''
            duplicated = False
            for tag in node:
                key = tag.attrib['k']
                value = tag.attrib['v']
                if key == 'addr:housenumber':
                    housenumber = value
                if key == 'addr:street':
                    street = value
                if key == 'addr:city':
                    city = value
                if key == 'addr:unit':
                    unit = value
                if key == 'note:addr' and value == 'Address is shared by multiple address points':
                    duplicated = True
            if duplicated:
                filtered_stacked = [x for x in stacked_addrs_list if x['housenumber'] == housenumber and x['street'] == street]
                if len(filtered_stacked) > 0:
                    print(f'Duplicated address and address is stacked: {housenumber} {street}')

        


def main():
    find_dupes_csv()

if __name__ == '__main__':
    main()