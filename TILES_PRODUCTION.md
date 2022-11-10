Tileset production
==================

> assumes an SVG source (if PNG/JPG, this limits the possible resolution of the "tile master")

  

### 1. 🗺️ Use existing tile as reference

We need an existing tile from some public tile server to use as reference for correctly placing our custom content on the map. OpenStreetMap has a tool at [https://tile.openstreetmap.de/](https://tile.openstreetmap.de/) which lets you find your desired "source tile".

> It's easiest to use the smallest tile which contains the whole area to be mapped, so zoom out until the whole area is covered. Edge cases might force you to use multiple "source tiles" (e.g. a map of Greenwich Park), in which case you will need to repeat this process.

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

- Overlay map image on existing tile (e.g. matching building shapes) with your favorite vector tool (e.g. [`inkscape`](https://inkscape.org/))

- Hide existing tile and export result to a new "source tile" SVG (`source.svg`)

> The source tile we have used for initial prototyping at DIGS is provided in this repository as [`digs_source.svg`](digs_source.svg). You can use this file if you just want to try out the next steps.

### 3. 🔪 Slice high-res "source tile" into tiles pyramid

> requires [libvips](https://www.libvips.org/install.html)

With source tile as `source.svg` and output directory `relative_tiles`
```
vips dzsave 'source.svg[scale=32]' relative_tiles --layout google --suffix .png --tile-size 512 --vips-progress
```

> assuming `source.svg` is `256x256`, otherwise adjust so that highest global zoom level is `21` (a `react-native-maps` limit)

[reference](https://web.archive.org/web/20221110085434/https://github.com/libvips/libvips/discussions/2826?sort=top)

  

### 4. 🌐 Translate relative to global tilenames (Z,X,Y)

Since `vips dzsave` produces a pyramid with `(0,0,0)` as initial tile, we need to "project" the tiles to the actual initial tile (from _Step 1_). We also need to switch the South-West and North-East tiles. For this, we use the script [translate_tiles.py](translate_tiles.py).



Example usage with input directory `relative_tiles`, source tilename `(17,69322,35423)` and output directory `tiles`
```
python3 translate_tiles.py 17 69322 35423 21 relative_tiles tiles
```

> uses calculations from [https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)