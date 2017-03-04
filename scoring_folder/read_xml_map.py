#!/usr/bin/python

import xml.etree.ElementTree as ET
from scoring_folder.scoring import Score
from src.map import Map


def xml_data():
    tree = ET.ElementTree(file='../scoring_folder/testmap2.xml')
    maps = tree.getroot()
    clean_maps = []
    clean_map = {}
    for map in maps.iter():
        if map.tag == "Map":
            if clean_map:
                clean_maps.append(clean_map)
            clean_map = {}
            clean_map['Columns'] = map.attrib['Columns']
            clean_map['Rows'] = map.attrib['Rows']
            clean_map['Humans'], clean_map['Werewolves'], clean_map['Vampires'] = [], [], []
        elif map.tag == "Humans":
            humans = [map.attrib['X'], map.attrib['Y'], map.attrib['Count'], 0, 0]
            clean_map['Humans'].append(humans)
        elif map.tag == "Werewolves":
            werewolves = [map.attrib['X'], map.attrib['Y'], 0, 0, map.attrib['Count']]
            clean_map['Werewolves'].append(werewolves)
        elif map.tag == "Vampires":
            vampires = [map.attrib['X'], map.attrib['Y'], 0, map.attrib['Count'], 0]
            clean_map['Vampires'].append(vampires)
    clean_maps.append(clean_map)
    return clean_maps


def build_maps(clean_maps):
    maps = []
    for map in clean_maps:
        # Initialize map with initial coords and map
        new_map = Map(vampires=[], werewolves=[], humans=[], size_x=map['Columns'], size_y=map['Rows'])
        map_infos = map['Humans'] + map['Vampires'] + map['Werewolves']
        new_map.initialize_map(map_infos)
        # team = new_map.find_grp(initial_x, initial_y)
        maps.append(new_map)
    return maps

if __name__ == "__main__":
    clean_maps = xml_data()
    maps = build_maps(clean_maps)
    i = 1
    for map in maps:
        print("Map", i, ", score : ", Score.scoring(Score(map, 1)))
        i += 1
