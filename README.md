# Canadian National Fire Database (CNFDB) Shiny App

This application provides an interactive interface to visualize and filter data from the Canadian National Fire Database (CNFDB). It uses a Shiny interface powered by MapLibre for mapping and a Martin tile server for serving vector tiles. This application is  intended to be a minimal working example incorporting Shiny for python with a custom tile server.

---

## Table of Contents
- [Canadian National Fire Database (CNFDB) Shiny App](#canadian-national-fire-database-cnfdb-shiny-app)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
    - [Install Python](#install-python)
    - [Set Up `uv`](#set-up-uv)
    - [Install Dependencies](#install-dependencies)
    - [Install GDAL](#install-gdal)
      - [On Linux](#on-linux)
      - [On macOS](#on-macos)
      - [On Windows](#on-windows)
    - [Install Martin Tile Server](#install-martin-tile-server)
  - [Running the Application](#running-the-application)
    - [Start the Martin Tile Server](#start-the-martin-tile-server)
    - [Run the Shiny App](#run-the-shiny-app)
  - [Notes](#notes)

---

## Features
- Filter CNFDB data by year using an interactive slider.
- Display vector tiles with fire polygons styled dynamically.
- Map-based tooltips and navigation controls.

---

## Installation

### Install Python
1. Download and install Python 3.9 or later from the [official Python website](https://www.python.org/downloads/).
   - Ensure that you add Python to your system PATH during installation.
2. Verify installation:
   ```bash
   python --version
   ```

### Set Up `uv`
1. Install the `uv` package manager:
   ```bash
   pip install uv
   ```
2. Verify `uv` installation:
   ```bash
   uv --version
   ```

### Install Dependencies
1. Clone this repository or download its contents.
2. Navigate to the project directory:
   ```bash
   cd path/to/project
   ```
3. Install the required dependencies:
   ```bash
   uv install
   ```

### Install GDAL
The app requires GDAL for geospatial data handling. Install it as follows:

#### On Linux
```bash
sudo apt update
sudo apt install gdal-bin libgdal-dev
```

#### On macOS
Install GDAL using Homebrew:
```bash
brew install gdal
```

#### On Windows
Download and install GDAL from [GIS Internals](https://www.gisinternals.com/).

Verify GDAL installation:
```bash
gdalinfo --version
```

### Install Martin Tile Server
Martin is required for serving vector tiles.

Generate PM tiles

```bash
ogr2ogr -f GeoJson ./data/nfdb.geojson ./data/NFDB_poly/NFDB_poly_20210707.shp -t_srs "EPSG:4326" -overwrite
tippecanoe -zg -o ./data/nfdb.mbtiles --drop-densest-as-needed ./data/nfdb.geojson --force --layer nfdb 
```

## Running the Application

### Start the Martin Tile Server
1. Set up your vector tile database.
2. Start the Martin server:
   ```bash
    martin ./tiles/nfdb.pmtiles -l localhost:3000
   ```
   Replace `user`, `password`, and `dbname` with your PostgreSQL credentials and database name.

### Run the Shiny App
1. Start the Shiny app:
   ```bash
   uv run
   ```
2. Open the app in your web browser at `http://127.0.0.1:8000`.

---

## Notes
- Ensure the vector tile source URL in the app matches your Martin tile server's endpoint.
- For additional customization or troubleshooting, consult the documentation for [GDAL](https://gdal.org/) and [Martin](https://github.com/maplibre/martin).

Enjoy exploring the Canadian National Fire Database!
