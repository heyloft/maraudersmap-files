Tileset production
==================

> assumes an SVG source (if PNG/JPG, this limits the possible resolution of the "tile master")

  

### 1. 🗺️ Use existing tile as reference

We need an existing tile from some public tile server to use as reference for correctly placing our custom content on the map. OpenStreetMap has a tool at [https://tile.openstreetmap.de/](https://tile.openstreetmap.de/) which lets you find your desired "source tile".

> It's easiest to use the smallest tile which contains the whole area to be mapped, so zoom out until the whole area is covered. Edge cases might force you to use multiple "source tiles", in which case you will need to repeat this process.

Simply navigate to your desired area at the appropriate zoom, right click on the map and `open tile url`.

This will give you a url on the following format:
```
https://tile.openstreetmap.de/{z}/{x}/{y}.png
```

Example:
```
https://tile.openstreetmap.de/17/69322/35423.png
```

The first number is the zoom level (`z`), the second is the `x` coordinate, and the third is the `y` coordinate.
Download the "source tile" and note the tilename, i.e. `(z,x,y)` coordinates. For the example, it would be `(17,69322,35423)`
  

### 2. 🗾 Create initial "source tile"

- Overlay map image on existing tile (e.g. matching building shapes) with a tool like `inkscape`

- Hide existing tile and export result to a new "source tile" SVG/PNG (`source.svg`)

  

### 3. 🔪 Slice high-res "source tile" into tiles pyramid

> requires [libvips](https://www.libvips.org/install.html)

With source tile as `source.svg` and output directory `relativeTiles`
```
vips dzsave 'source.svg[scale=32]' relativeTiles --layout google --suffix .png --tile-size 512 --vips-progress
```

> assuming `source.svg` is `256x256`, otherwise adjust so that highest global zoom level is `21` (a `react-native-maps` limit)

[reference](https://github.com/libvips/libvips/discussions/2826?sort=top)

  

### 4. 🌐 Translate relative to global tilenames (Z,X,Y)

Since `vips dzsave` produces a pyramid with `(0,0,0)` as initial tile, we need to "project" the tiles to the actual initial tile (from _Step 1_). The below script also fixes an issue where SW and NE tiles need to be switched.

[tileRelativeToGlobal.py](https://gist.github.com/mathiazom/66cc23db3934dc45948dd50e90043ef2)

```
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


def relativeMappings(r, g, mappings, maxGlobalZoom) -> tuple[Tile, Tile]:
    mappings.append((r, g))
    gs = subtiles(g)
    rs = subtiles(r)
    if gs["nw"].z > maxGlobalZoom:
        return
    relativeMappings(rs["nw"], gs["nw"], mappings, maxGlobalZoom)
    relativeMappings(rs["sw"], gs["ne"], mappings, maxGlobalZoom)
    relativeMappings(rs["se"], gs["se"], mappings, maxGlobalZoom)
    relativeMappings(rs["ne"], gs["sw"], mappings, maxGlobalZoom)


def copyToGlobalVersion(
    source, dest, relativeTile: Tile, globalTile: Tile, maxZoom: int
):
    mappings: list[tuple[Tile, Tile]] = []
    relativeMappings(relativeTile, globalTile, mappings, maxZoom)
    os.makedirs(dest, exist_ok=True)
    shutil.copy(f"{source}/blank.png", f"{dest}/blank.png")
    for r, g in mappings:
        src = f"{source}/{r.z}/{r.x}/{r.y}.png"
        if not os.path.isfile(src):
            continue
        destDir = f"{dest}/{g.z}/{g.x}"
        os.makedirs(destDir, exist_ok=True)
        shutil.copy(src, f"{destDir}/{g.y}.png")


def main():
    relativeTile = Tile(0, 0, 0)
    globalTile = Tile(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    copyToGlobalVersion(
        sys.argv[5], sys.argv[6], relativeTile, globalTile, int(sys.argv[4])
    )


if __name__ == "__main__":
    main()
```

Example usage with input directory `relativeTiles`, source tilename `(17,69322,35423)` and output directory `tiles`
```
python3 tileRelativeToGlobal.py 17 69322 35423 21 relativeTiles tiles
```

> uses calculations from [https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)



#### One-liner for slice and relativeToGlobal

```
vips dzsave 'source.svg[scale=32]' relativeTiles --layout google --suffix .png --tile-size 512 --vips-progress && python3 tileRelativeToGlobal.py 17 69322 35423 21 relativeTiles tiles
```


### 5. 📥️ Place tiles in `/tiles/{Z}/{X}/{Y}.png`