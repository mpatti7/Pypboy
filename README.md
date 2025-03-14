# Pypboy
Pipboy 3000 Interface from the Fallout Series

Based on this: https://github.com/sabas1080/pypboy

## Running on WSL:
Follow this tutorial to get it working: https://medium.com/@youngtuo/run-pygame-through-wsl2-in-3-steps-2ee0b776dbaa

## Additional Installations:
Install VLC: `sudo apt install vlc`

Install library for VLC: `sudo apt install libvlc-dev`

Install GDAL Development Libraries on Pi: `sudo apt install -y gdal-bin libgdal-dev`

If there are issues with installing GDAL, it may need to be built from source if versions are wrong

**Important** 
May need to change the version of pyproj in `requirements.txt` to `3.6.1`

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

## Building SDL and Pygame with NEON Optimization
This warning will pop up every time when running the code on the pi. You can try building the SDL and Pygame libraries with
NEON optimizations to help with performance, but in my experience, nothing changes. I made a test virtual environment where
I installed `pip install -r requirements.txt` then did `pip uninstall pygame`. You may need to do `pip install cython`.

Refer to these resources:

[GitHub Discussion](https://github.com/pygame/pygame/issues/2455)

[SDL Info](https://wiki.libsdl.org/SDL2/README/raspberrypi)

Clone the SDL repo, make a new directory in it, `mkdir build` and navigate to it, then 

`export CFLAGS="-mfpu=neon -mfloat-abi=hard"`

`cmake .. -DCMAKE_BUILD_TYPE=Release -DSDL_ARM_NEON=ON -G "Ninja"`

`ninja`

`sudo ninja install`

Now for Pygame:

`export CFLAGS="-mfpu=neon -mfloat-abi=hard"`

`export PYGAME_DETECT_AVX2=1`

`git clone https://github.com/pygame/pygame.git`

Navigate to the repo `cd pygame`

According to the GitHub discussion linked above,  run `python setup.py install -enable-arm-neon`

## Resources:

[Google Maps Themes](https://snazzymaps.com/)

[Vault Boy Icons](https://fallout.fandom.com/wiki/Category:Vault_Boy_images)

[FM Stream](https://fmstream.org/index.php?c=FT) and [Radio Browser](https://www.radio-browser.info/) for radio station stream URLs
