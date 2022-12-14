from fileinput import filename
import xml.etree.ElementTree as ET
from find_address import format_housenumber

def process_housenumbers(filename):
    '''
    add the extension to the housenumbers on all houses
    '''
    tree = ET.parse(filename)
    root = tree.getroot()

    #a dictionary of addresses, with a list of extensions
    for node in root:
        number = ''
        ext = ''
        for tag in node:
            key = tag.attrib['k']
            value = tag.attrib['v']
            if key == 'addr:housenumber':
                number = value
            if key == 'HOUSESX':
                ext = value

        for tag in node:
            if tag.attrib['k'] == 'addr:housenumber':
                tag.set('v', format_housenumber(number, ext))
            if tag.attrib['k'] == 'HOUSESX':
                node.remove(tag)

    tree.write(filename)

def main():
    for i in range(1, 75):
        process_housenumbers(f'addresses_tract{i}.osm')

if __name__ == '__main__':
    main()