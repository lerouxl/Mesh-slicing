import bpy
import bmesh
import os
from pathlib import Path

"""
This script is made for  Blender 2.92 and use the MeshSlicer (https://github.com/TomekSc/MeshSlicer).
To install the add-on:
    1- Downlowd MeshSlicer.py from the github
    2- On blender 2.92, go to Edit/Preference/Add-ons
    3- Click on Install add-on and select MeshSlicer.py
    4- Activate the add on by ticking his box on the add-ons list


To use it, put your files to preprocess on a folder and attribute it's path to FILES_FOLDER. 
The sliced results will be save in SAVE_FOLDER/name_mesh/

Writed by Leopold Le Roux, 21/10/2021
"""

FILE_PATH = ""
FILES_FOLDER = Path("WHERE ARE THE STL FILES")
SAVE_FOLDER = Path("WHERE TO STORE THE STL FILES")
Z_MAX = 0
Z_MIN = 0
SLICE_Zs = []
SLIDE_HEIGHT = 2



def slice_a_file(name_file, input_path, output_path):
    "Will load the stl from the FILE_PATH and slice it, the slided mesh are save in SAVE_FOLDER"

    # if the results folder do not exist, create it
    if not os.path.exists(str(output_path)):
        os.makedirs(output_path)
    # Clean the results folder
    for file in output_path.glob("*.stl"):
        file.unlink()
        
    # Clear workspace
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Found the Z size
    bpy.ops.import_mesh.stl(filepath=input_path)
    obj = bpy.context.active_object
    Z_MAX = max([v[-1] for v in obj.bound_box])
    Z_MIN = min([v[-1] for v in obj.bound_box])

    # Compute the Z height of the slides
    NUMBER_OF_SLICE = int((Z_MAX - Z_MIN) / SLIDE_HEIGHT)
    SLICE_Zs = []
    z = Z_MIN
    while z < Z_MAX:
        SLICE_Zs.append(z)
        z += SLIDE_HEIGHT
    SLICE_Zs.append(Z_MAX)


    for slide_number in range(NUMBER_OF_SLICE):

        # Clear workspace
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Ask for 1 plan to slice
        bpy.data.scenes["Scene"].my_tool.slicerSize = 60
        bpy.ops.generate.operator(variant=0)

        # Add a second plan
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Slicer'].select_set(True)

        # Create a // plan
        bpy.ops.object.duplicate_move()
        bpy.data.objects['Slicer.001'].location = [0,0, SLICE_Zs[slide_number]]
        bpy.data.objects['Slicer'].location = [0,0, SLICE_Zs[slide_number+1]]

        # Import mesh
        bpy.ops.object.select_all(action='DESELECT')
        #bpy.ops.mesh.primitive_cube_add(size=30.0,location=(0,0,0))
        bpy.ops.import_mesh.stl(filepath=input_path)
        objects = bpy.context.selected_objects
        name_mesh = objects[0].name

        # Slice
        bpy.ops.object.select_all(action='DESELECT')

        bpy.data.objects['Slicer.001'].select_set(True)
        bpy.data.objects['Slicer'].select_set(True)

        bpy.data.objects[name_mesh].select_set(True)
        bpy.ops.slice.operator()



        # Extract the good layer
        bpy.ops.object.select_all(action='DESELECT')
        if slide_number == 0:
            bpy.data.objects["Bool result 0"].select_set(True)
        else:
            bpy.data.objects["Bool result 1"].select_set(True) # Select the part between the 2 plan
            
        
        bpy.ops.export_mesh.stl(filepath=str(output_path / f"{name_file}_slide_{slide_number}.stl"), use_selection=True)
        

# List file to process
raw_files = list(FILES_FOLDER.glob("*.stl"))
for file in raw_files:
    output_path =  SAVE_FOLDER / file.stem
    slice_a_file(file.stem, str(file), output_path)
    