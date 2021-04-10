# Notes, resources, links

Everything that does not seem right to put into comments, but could:

1. Help me pick up the project later on and implement some improvements/fix some bugs,
2. help others that find this project to understand how it was implemented and why.

## Scripts included

- `find_signs.py` - replace `world_directory` with path to your world save folder. Put the world directory into the same folder as this script (I know, but I also don't care). Run it and it will generate a `signs.json` file with all the signs, their location and text that players put on them.
- `create_sign_images.py` - reads `signs.json` and creates signs images (named `0.png` to `XYZ.png`). Texture used is in `res` folder, and it is oak sign. Oh, yeah, and accents are best-effort-delivery removed from the accented letters, because used Minecraft font does not support them and because accented characters are annoying.
- `classify_signs.py` - adds `category` property to the objects in `signs.json` that states what type of the sign it is - empty, plugin-related (starts with known plugin indicators - such as `[private]`, notempty). Run it. It will modify `signs.json`.

To modify what "categories" of signs will be produced on the output, open `create_sign_images.py` and update `INCLUDED_CATEGORIES` accordingly (supported options are listed).

## Anvil-parser

Minecraft uses NBT to store information about the world. An `anvil-parser` package is leveraged to help with parsing this format in a user friendly matter (shields you, as a developer from the need to work with raw bytes, figuring/reading out the offsets etc.)

API: https://anvil-parser.readthedocs.io/en/latest/api.html

_Note: There is a `chunk_location(x,z)` that returns `(0,0)` if the chunk has not been generated. This might be leveraged before trying to read the chunks to see whether we can skip some chunks. In code, I enumerate all possible chunks and `try-except` if the chunk does not exist._

## References

- https://gaming.stackexchange.com/questions/375188/how-to-replace-blocks-and-items-in-minecraft-mca-files
- https://minecraft.fandom.com/wiki/Region_file_format
- https://minecraft.fandom.com/wiki/Chunk_format
- https://nathanwilliams.github.io/2013/04/16/minecraft-region-files/
- https://www.spigotmc.org/threads/anvil-ntb-reading-chunks-blocks.341769
- https://minecraft.fandom.com/wiki/Talk:Chunk_format
- https://github.com/Querz/NBT
- https://minecraft.fandom.com/el/wiki/Chunk
- https://anvil-parser.readthedocs.io/en/latest/api.html
- https://pypi.org/project/anvil-parser/
- https://minecraft.fandom.com/wiki/Anvil_file_format

## Remnants of attempts at browsing the entire world block-by-block

Before I found out there is a `tile_entity` available at chunk bytes, I was considering iterating over all blocks to find signs. Following is the code I used and not utilized.

```py
SUPPRESSED_BLOCK_IDS = ["lava", "bedrock", "lapis_ore", "coal_ore", "dirt", "gravel", "air", "water", "sand", "stone", "gold_ore", "wall_torch", "grass", "grass_block", "diamond_ore", "granite", "diorite", "andesite", "snow", "cave_air", "infested_stone", "iron_ore", "dark_oak_leaves", "dark_oak_log", "redstone_ore", "oak_leaves", "oak_log" ]

BLOCKS_OF_INTEREST = ["oak_sign", "dark_oak_sign"]

# Needs chunk object to be retrieved from region - we are operating on chunk object
# Leverage 3D iteration to go through all the chunk blocks
xb = 0 ; zb = 0; yb = 0
for xb in range(16):
    for zb in range(16):
        for yb in range(50,70):
            block = chunk.get_block(xb, yb, zb)

            
            if block.id not in SUPPRESSED_BLOCK_IDS:
                print(f"Unsuppressed block @ local [{xb}, {yb}, {zb}]={block.id}")
                if block.properties:
                    print(block.properties)

            yb += 1
        zb += 1
    xb += 1
```