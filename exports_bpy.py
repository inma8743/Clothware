import bpy
import os
import sys

def export_3d_path(product_idx):
    return os.path.join('./uploads/stylechain/product', '3d', product_idx)

def exports_3dModeling(product_idx, garment_type):
    export_file_path = export_3d_path(product_idx)
    obj_file_path = os.path.join('./uploads/stylechain/product', '3d', product_idx, 'digital_TShirt.obj')
    if garment_type == 'pants':
        obj_file_path = os.path.join('./uploads/stylechain/product', '3d', product_idx, 'digital_pants.obj')

    # 기존에 불러온 모든 객체 제거
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create a new material
    material = bpy.data.materials.new(name="default_mat")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')

    # Set up the texture node if BSDF is present
    if bsdf is not None:
        texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(os.path.join(export_file_path, 'texture.png'))
        material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    # Import OBJ file
    bpy.ops.import_scene.obj(filepath=obj_file_path)

    # Assuming the imported object is the only one or the last in the collection
    # Update this logic based on how you determine which object was just imported
    if bpy.context.scene.objects:
        clothes_obj = bpy.context.scene.objects[-1]  # Assuming the last object in the scene is the imported one
        # Set material to the imported object, check if it has a material slot first
        if clothes_obj.data.materials:
            clothes_obj.data.materials[0] = material
        else:
            clothes_obj.data.materials.append(material)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.shade_smooth()

    bpy.ops.export_scene.fbx(filepath=os.path.join(export_file_path, f"{product_idx}.fbx"))
    bpy.ops.export_scene.gltf(filepath=os.path.join(export_file_path, f"{product_idx}.glb"), export_format="GLB")

product_idx = sys.argv[1]
garment_type = sys.argv[2]

exports_3dModeling(product_idx, garment_type)

