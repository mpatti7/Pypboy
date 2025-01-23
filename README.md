# Pypboy
Pipboy 3000 Interface from the Fallout Series

Based on this: https://github.com/sabas1080/pypboy

## Running on WSL:
Follow this tutorial to get it working: https://medium.com/@youngtuo/run-pygame-through-wsl2-in-3-steps-2ee0b776dbaa

## Additional Installations:
Install VLC: `sudo apt install vlc`

Install library for VLC: `sudo apt install libvlc-dev`

Install GDAL Development Libraries on Pi: `sudo apt install -y gdal-bin libgdal-dev`

On Pi: 
`export GDAL_CONFIG=/usr/bin/gdal-config`

`export GDAL_VERSION=$(gdal-config --version)`

Install library for NumPy on Pi: `sudo apt-get install libatlas-base-dev`

Install: `https://pypi.org/project/pyproj/3.6.1/`

Install: `sudo apt install python3-dev python3-pip libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev`

`export PYGAME_DETECT_NEON=1`

Then: `pip uninstall pygame`

`pip install pygame --no-binary :all:`

**Note:**

If there's still issues when installing fiona, trying running: `pip install gdal`

If issue with installing proj on the pi, there might be an outdated version and you'll need to install a newer one:

`sudo apt remove -y proj-bin libproj-dev`

## Bulding Proj from Source if issues arise
Installing requirements on pi might result in a failure when it gets to pyproj. It could be that the installed version is out of date and must be built from source.

**Note:** This is all done outside your venv and project folder until the very last step.

#### 1. Remove Old Version
First, remove the existing PROJ version to avoid conflicts:

`sudo apt remove -y proj-bin libproj-dev`

#### 2. Install the required dependencies:

`sudo apt update`

`sudo apt install -y build-essential cmake libsqlite3-dev curl`

#### 3. Download the latest PROJ source code:

`curl -LO https://download.osgeo.org/proj/proj-9.5.1.tar.gz`

#### 4. Extract the downloaded file:

`tar -xvzf proj-9.5.1.tar.gz` 

`cd proj-9.5.1`

#### 5. Next steps:
Now, follow the steps from here: https://proj.org/en/9.5/install.html#build-steps

#### 6. Final step:
**Note:** Run the final command with `sudo`. If there are any issues, try with `sudo`.

After, run the first command from here: https://pyproj4.github.io/pyproj/stable/installation.html#installation inside your venv.

`python -m pip install pyproj`

## Resources:

Google Maps Themes: https://snazzymaps.com/

Example Fallout Icons: https://www.behance.net/gallery/27377197/Weather-App-Fallout 

DB to find Radio Station Stream URLs: https://www.radio-browser.info/