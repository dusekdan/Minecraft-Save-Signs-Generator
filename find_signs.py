import os
import json

import anvil

world_directory = "./region-test"
SIGNS_OUTPUT_FILE = "signs.json"

def load_json_from_TAG_string(string):
    """
    String contained within `TAG_string` is typically in JSON format.
    This function creates JSON object from such string.

    Default value returned matches expected deserialized object used
    for sign text.
    """
    try:
        actual_string = str(string)
        data = json.loads(actual_string)
        print(data)
        return data
    except json.JSONDecodeError as e:
        print(f"Couldn't load json data from TAG_string for {string}")
        return {'text': ''} # hh, sensible defaults

signs = []
i = 0

# Go through all regions
for region_file in os.listdir(world_directory):

    if region_file.endswith(".mcr"):
        print(f"Skipping {region_file} (is old format - duplicate)...")
        continue

    print(f"Reading {i} from {region_file}")
    region = anvil.Region.from_file(f"{world_directory}/{region_file}")
    
    # Now, in every region, there should be chunks between [0,0],[0,1]...[31,31] (format is [x,z])
    # and I need to loop through them. If they are not there, they have not been generated yet - 
    # handle this in try-catch.
    x = 0; z = 0
    for x in range(32):
        for z in range(32):
            try:
                chunk = region.get_chunk(x, z)
            except anvil.errors.ChunkNotFound as e:
                continue
            except KeyError as e:
                continue

            # There is actually a way of retrieving signs from tile entities (stored per chunk)
            try:
                """
                `entities` is list of TAG_Compound - a structure that carries 
                related tags for an entity
                """
                entities = chunk.tile_entities
                for entity_compound in entities:
                    """
                    Entity compound is a TAG_Compound record that may or may not 
                    have certain keys. Based on which are available, we are 
                    able to extract signs only. 
                    """
                    keys = entity_compound.keys()
                    if "id" in keys:
                        if "minecraft" in entity_compound["id"] and "sign" in entity_compound["id"]:
                            print(f"Sign found at [{entity_compound['x']},{entity_compound['y']},{entity_compound['z']}], saving...")
                            signs.append({
                                "x": int(str(entity_compound['x'])),
                                "y": int(str(entity_compound['y'])),
                                "z": int(str(entity_compound['z'])),
                                "line1": load_json_from_TAG_string(entity_compound['Text1'])['text'],
                                "line2": load_json_from_TAG_string(entity_compound['Text2'])['text'],
                                "line3": load_json_from_TAG_string(entity_compound['Text3'])['text'],
                                "line4": load_json_from_TAG_string(entity_compound['Text4'])['text']
                            })
            except Exception as e: 
                print("Something failed horribly during sign data extraction...")
                print(e)
            
            z += 1
        x += 1
    i += 1

"""
After everything is extracted, let's write the signs into the file

Will have to implement my own serialization routine -> using json.dump 
automatically converts accented characters into their codes, which I
do not want.
"""
with open(SIGNS_OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(signs, f)