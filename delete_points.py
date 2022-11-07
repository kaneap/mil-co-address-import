
import csv

from cv2 import add
from fileinput import filename
import xml.etree.ElementTree as ET

def delete_points(del_points_filename):
    tree = ET.parse(del_points_filename)
    root = tree.getroot()

    del_list = {}
    for node in root:
        lat = node.attrib['lat']
        lon = node.attrib['lon']
        del_list[lat+lon] = True

    num_deletions = 0
    for i in range(1, 75):
        tree = ET.parse(f'addresses_tract{i}.osm')
        root = tree.getroot()
        
        for node in root:
            lat = node.attrib['lat']
            lon = node.attrib['lon']
            if lat+lon in del_list:
                num_deletions += 1
                root.remove(node)
        tree.write(f'addresses_tract{i}.osm')

def main():
    delete_points('points_to_delete.osm')

if __name__ == '__main__':
    main()