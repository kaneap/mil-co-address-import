from fileinput import filename
import xml.etree.ElementTree as ET

def process_housenumbers(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    #a dictionary of addresses, with a list of extensions
    addrs = {}
    for node in root:
        id = node.attrib['id']
        number = ''
        street = ''
        ext = ''
        for tag in node:
            key = tag.attrib['k']
            value = tag.attrib['v']
            if key == 'addr:street':
                street = value
            if key == 'addr:housenumber':
                number = value
            if key == 'HOUSESX':
                ext = value
        base_addr = number + ' ' + street
        addrs.setdefault(base_addr, [])
        extensions = addrs[base_addr]
        extensions.append({'id':id, 'ext': ext, 'housenumber': number})

    #exclude addresses with no extensions
    to_delete = []
    for base_addr in addrs:
        extensions = addrs[base_addr]
        if len(extensions) == 1 and extensions[0]['ext'] == '':
            to_delete.append(base_addr)
    for base_addr in to_delete:
        addrs.pop(base_addr)

    housenumber_updates = {}
    for base_addr in addrs:
        extensions = addrs[base_addr]
        has_unextended = any([extension['ext'] == '' for extension in extensions])
        if has_unextended:
            for element in extensions:
                if element['ext'] == '':
                    continue
                housenumber = element['housenumber']
                extension = element['ext']
                if extension == '1/2':
                    extension = ' 1/2'
                element['housenumber'] = housenumber + extension
                housenumber_updates[element['id']] = element
        elif len(extensions) == 1:
            for element in extensions:
                housenumber = element['housenumber']
                extension = element['ext']
                if extension == '1/2':
                    extension = ' 1/2'
                element['housenumber'] = housenumber + ',' + housenumber + extension
                housenumber_updates[element['id']] = element

    for node in root:
        id = node.attrib['id']
        if id in housenumber_updates:
            for tag in node:
                if tag.attrib['k'] == 'addr:housenumber':
                    tag.set('v', housenumber_updates[id]['housenumber'])
                if tag.attrib['k'] == 'HOUSESX':
                    node.remove(tag)


    tree.write(filename)

def main():
    for i in range(1, 75):
        process_housenumbers(f'addresses_tract{i}.osm')

if __name__ == '__main__':
    main()