import xml.etree.ElementTree as ET
import addr_formatting

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
            housenumber_field = ''
            street = ''
            unit = ''
            city = ''
            zip = ''
            for tag in node:
                if 'k' not in tag.attrib:
                    continue
                key = tag.attrib['k']
                value = tag.attrib['v']
                if key == 'addr:housenumber':
                    housenumber_field = value
                if key == 'addr:street':
                    street = value
                if key == 'addr:city':
                    city = value
                if key == 'addr:unit':
                    unit = value
                if key == 'addr:postcode':
                    zip = addr_formatting.cut_zip(value)
            
            for housenumber in housenumber_field.split(','):
                addr = housenumber.strip() + ' ' + street
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
        print(f'\naddresses_tract{i}.osm:')
        tree = ET.parse(f'addresses_tract{i}.osm')
        root = tree.getroot()
        
        for node in root:
            housenumber_field = ''
            street = ''
            unit = ''
            city = ''
            has_note = False
            for tag in node:
                if 'k' not in tag.attrib:
                    continue
                key = tag.attrib['k']
                value = tag.attrib['v']
                if key == 'addr:housenumber':
                    housenumber_field = value
                if key == 'addr:street':
                    street = value
                if key == 'addr:city':
                    city = value
                if key == 'addr:unit':
                    unit = value
                if key == 'addr:postcode':
                    zip = addr_formatting.cut_zip(value)
                if key == 'note:addr':
                    has_note = True
            for housenumber in housenumber_field.split(','):
                addr = housenumber + ' ' + street
                if len(unit) > 0:
                    addr = addr + ' Unit ' + unit
                if len(city) > 0:
                    addr = addr + ' ' + city
                if addr in addresses and not has_note:
                    ET.SubElement(node, 'tag', {'k': 'note:addr', 'v': 'This address exists in two places'})
                    print(housenumber, street)
        tree.write(f'addresses_tract{i}.osm')


def main():
    find_dupes()

if __name__ == '__main__':
    main()