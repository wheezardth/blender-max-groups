# Max Group Add-On for Blender

Max Group is a simple add-on that emulates 3ds Max's grouping functionality in Blender. It aids 3D artists and designers transitioning from 3ds Max to Blender by providing familiar grouping behavior.

## Features

- **Grouping**: Select multiple objects and group them using a bounding cube.
- **Bounding Cube**: Automatically calculates and creates a cube that encompasses all the selected objects.
- **Parenting**: Selected objects are parented to the bounding cube, providing an intuitive hierarchy in the outliner.

## Installation

1. Download the `blender-max-groups.py` script.
2. Open Blender and navigate to `Edit` > `Preferences`.
3. In the `Add-ons` tab, click `Install` and select the downloaded script.
4. Enable the add-on by checking the box next to "3D View: Max Group".

## Usage

1. In Object Mode, select the objects you want to group.
2. Press `Ctrl + Alt + G` or use the Max Group button in the 3D View's Tools Panel.
3. A bounding cube will be created, and the selected objects will be parented to it.
