import xml.etree.ElementTree as ET

for i in range(1, 75):
    tree = ET.parse(f'addresses_tract{i}.osm')
    root = tree.getroot()

    for node in root:
        for tag in node:
            key = tag.attrib['k']
            value = tag.attrib['v']
            if key == 'note:addr':
                node.remove(tag)
    tree.write(f'addresses_tract{i}.osm')

