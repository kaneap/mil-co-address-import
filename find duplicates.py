import xml.etree.ElementTree as ET

def find_dupes():
    '''
    Find points with identical addresses and add a note to them
    '''
    # opening the osm file
    addresses = {}
    for i in range(1, 75):
        tree = ET.parse(f'addresses_tract{i}.osm')
        root = tree.getroot()
        
        for node in root:
            housenumber = ''
            street = ''
            unit = ''
            city = ''
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
            
            addr = housenumber + ' ' + street
            if len(unit) > 0:
                addr = addr + ' Unit ' + unit
            if len(city) > 0:
                addr = addr + ' ' + city
            addresses.setdefault(addr, 0)
            addresses[addr] += 1

    for key in list(addresses):
        if addresses[key] < 2:
            del addresses[key]
    print(f'Num duplicates: {len(addresses)}')

    for i in range(1, 75):
        tree = ET.parse(f'addresses_tract{i}.osm')
        root = tree.getroot()
        
        for node in root:
            housenumber = ''
            street = ''
            unit = ''
            city = ''
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
            
            addr = housenumber + ' ' + street
            if len(unit) > 0:
                addr = addr + ' Unit ' + unit
            if len(city) > 0:
                addr = addr + ' ' + city
            if addr in addresses:
                ET.SubElement(node, 'tag', {'k': 'note:addr', 'v': 'Address is shared by multiple address points'})
        tree.write(f'addresses_tract{i}.osm')

def main():
    find_dupes()

if __name__ == '__main__':
    main()