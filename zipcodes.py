import xml.etree.ElementTree as ET

def main():
    tree = ET.parse('Address_Points.osm')
    root = tree.getroot()

    for node in root:
        for tag in node:
            key = tag.attrib['k']
            value = tag.attrib['v']
            if key == 'addr:postcode':
                if len(value) == 9:
                    tag.set('v', value[:5] + '-' + value[5:])
    tree.write('Address_Points2.osm')
if __name__ == '__main__':
    main()