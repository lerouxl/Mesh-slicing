# Mesh-slicing
This script use Blender to process meshes and cut them in slices like a 3D printer slicer do.
STL files had to be placed in a folder and all of them will be cut in multiple parts of a defined height.
The results of this will be save in a folder with the name of the part.

## Installation:
This script require the use of Blender 2.92 and of the [MeshSlicer](https://github.com/TomekSc/MeshSlicer) add-on.
To install the add-on:

    1- Download MeshSlicer.py from github
    2- On blender 2.92, go to Edit/Preference/Add-ons
    3- Click on Install add-on and select MeshSlicer.py
    4- Activate the add on by ticking his box on the add-ons list 

## Use:
To use this script, follow those 6 steps:

    1- Put your stl file in a folder
    2- Open Blender 2.92, go to Scripting
    3- Open Blender_slicer.py
    4- Set FILES_FOLDER to be the path to your stl folder(1)
    5- Set SAVE_FOLDER to where you want to save the mesh slides
    6- Set the SLIDE_HEIGHT. This is the height of the slides
![Image of the install step](https://raw.githubusercontent.com/hy-son/Mesh-slicing/main/Img/steps.png)

## Results:
Here is an example of the 2 slices you can obtain:

![Image of 2 slices](https://raw.githubusercontent.com/hy-son/Mesh-slicing/main/Img/2slides.png)