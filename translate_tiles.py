from dataclasses import dataclass
import shutil
import os
import sys


@dataclass
class Tile:
    z: int
    x: int
    y: int


def subtiles(tile):
    return {
        "nw": Tile(tile.z + 1, 2 * tile.x, 2 * tile.y),
        "sw": Tile(tile.z + 1, 2 * tile.x, 2 * tile.y + 1),
        "se": Tile(tile.z + 1, 2 * tile.x + 1, 2 * tile.y + 1),
        "ne": Tile(tile.z + 1, 2 * tile.x + 1, 2 * tile.y),
    }


def translate_tiles(
    relative_tile: Tile,
    global_tile: Tile,
    global_max_zoom: int,
):
    translations = [(relative_tile, global_tile)]
    if global_tile.z >= global_max_zoom:
        return translations
    relative_subtiles = subtiles(relative_tile)
    global_subtiles = subtiles(global_tile)
    for relative_quadrant, global_quadrant in [
        ("nw", "nw"),
        ("sw", "ne"),
        ("se", "se"),
        ("ne", "sw"),
    ]:
        translations.extend(
            translate_tiles(
                relative_subtiles[relative_quadrant],
                global_subtiles[global_quadrant],
                global_max_zoom,
            )
        )
    return translations


def translate_and_write_tiles(
    source_path: str,
    output_path: str,
    relative_tile: Tile,
    global_tile: Tile,
    global_max_zoom: int,
):
    translations: list[tuple[Tile, Tile]] = translate_tiles(
        relative_tile, global_tile, global_max_zoom
    )
    os.makedirs(output_path, exist_ok=True)
    shutil.copy(f"{source_path}/blank.png", f"{output_path}/blank.png")
    for relative_tile, global_tile in translations:
        relative_tile_path = (
            f"{source_path}/{relative_tile.z}/{relative_tile.x}/{relative_tile.y}.png"
        )
        if not os.path.isfile(relative_tile_path):
            # Tile is not part of tileset, ignore
            continue
        dest_dir = f"{output_path}/{global_tile.z}/{global_tile.x}"
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy(relative_tile_path, f"{dest_dir}/{global_tile.y}.png")


if __name__ == "__main__":
    translate_and_write_tiles(
        source_path=sys.argv[5],
        output_path=sys.argv[6],
        relative_tile=Tile(0, 0, 0),
        global_tile=Tile(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])),
        global_max_zoom=int(sys.argv[4]),
    )
