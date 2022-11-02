import xml.etree.ElementTree as ET

def main():
    tree = ET.parse('Address_Points2.osm')
    root = tree.getroot()
    for node in root:
        street = ''
        dir = ''
        pdir = ''
        sttype = ''
        for tag in node:
            key = tag.attrib['k']
            value = tag.attrib['v']
            if key == 'addr:street':
                if value[0].isnumeric():
                    street = value.lower()
                else:
                    street = value.title()
            elif key == 'DIR':
                dir = value
            elif key == 'PDIR':
                pdir = value
            elif key == 'STTYPE':
                sttype = value
        full_name = ''
        if dir != '':
            full_name += dir + ' '
        full_name += street
        if sttype != '':
            full_name += ' ' + sttype
        if pdir != '':
            full_name += ' ' + pdir
        for tag in node:
            if tag.attrib['k'] == 'addr:street':
                tag.set('v', full_name)

        
    tree.write('Address_Points1.osm')
if __name__ == '__main__':
    main()