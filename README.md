# python-raycaster
A simple raycaster written in Python using Pygame.

## Preview
![Preview](preview/preview.gif)

## Installation
Clone the repository.
```bash
git clone https://www.github.com/pietrykovsky/python-raycaster.git
```

Create a virtual environment and install the dependencies.
```bash
python -m venv venv
```

Activate the virtual environment.
```bash
# unix based:
source venv/bin/activate
# windows:
venv\Scripts\activate
```

Install the dependencies.
```bash
pip install -r requirements.txt
```

## Usage
Run the program from the project root.
```bash
python -m raycaster
```

## Controls
- `W` - Move forward
- `S` - Move backward
- `A` - Move left
- `D` - Move right
- `ARROW LEFT` - Turn left
- `ARROW RIGHT` - Turn right
- `SPACE` - Shoot
- `ESC` - Quit

## Settings
The settings can be found in `raycaster/core/settings.py`.

To change the resolution, modify the following variables:
```python
# GAME RELATED
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 ```

 Change the volume:
```python
# SOUND RELATED
MASTER_VOLUME = 1.0
MUSIC_VOLUME = 0.25
EFFECTS_VOLUME = 0.5
```

If you suffer low FPS, try to change the `RAY_COUNT` variable and decrease the ray count:
```python
RAY_COUNT = 200
```