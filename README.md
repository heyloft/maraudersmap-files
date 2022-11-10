# Marauder's Map Tile Server

*Tile server for the [Marauder's Map Project](https://github.com/heyloft/maraudersmap)*

[![Built with FastAPI](https://img.shields.io/badge/FastAPI-005571?&logo=fastapi)](https://fastapi.tiangolo.com)
![Python Version](https://img.shields.io/badge/python-3.10-brightgreen)
![License](https://img.shields.io/github/license/heyloft/maraudersmap?color=blue)

> A tile server provides a directory of PNG files that each make out a portion of a map. This can be used to render a web map by stitching together multiple portions based on the users viewing position and zoom level.
>
> See ["Tiled web map" on Wikipedia](https://en.wikipedia.org/wiki/Tiled_web_map)

## 🗺️ Tiles API endpoint
```
/tiles/{z}/{x}/{y}.png
```
> Follows the [Slippy Map file naming conventions](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)

## ✨ Setup
1. Install `Python 3.10` (see [Python docs](https://docs.python.org/3.10/using/index.html))
2. Install [Poetry](https://python-poetry.org/)
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    > see [Poetry docs](https://python-poetry.org/docs/#installation) for alternative installation methods
3. (Optional, but recommended)
    
    Tell Poetry to create the virtual environment inside the project directory
    ```
    poetry config --local virtualenvs.in-project true
    ```
    > this makes it easier for development environments like VS Code to recognize the correct Python intepreter for the project
4. Install project dependencies
    ```
    poetry install
    ```

## 🚀 Launch
```
poetry run uvicorn main:app
```

## ✂️ Tiles production
Got a custom map as SVG/PNG/JPG and want to create tiles for it?

See [TILES_PRODUCTION.md](TILES_PRODUCTION.md)

When you're done, make sure your new tiles are placed in the `tiles` directory.

## 🌐 Deployment
The tile server can be deployed in a lot of places. We currently use [Fly.io](https://fly.io/) for quick prototyping.
1. Install [`flyctl`](https://fly.io/docs/hands-on/install-flyctl/)
2. Create an account with `fly auth signup` or login with `fly auth login`
3. Deploy
    ```
    fly launch --copy-config --now --name <some-unique-and-colorful-app-name>
    ```