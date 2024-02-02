import bpy
import os

def export_3d_path(product_idx):
    return os.path.join('./uploads/stylechain/product', '3d', product_idx)

def exports_3dModeling(product_idx):
    export_file_path = export_3d_path(product_idx)
    obj_file_path = os.path.join('./uploads/stylechain/product', '3d', product_idx, 'digital_TShirt.obj')

    # 기존에 불러온 모든 객체 제거
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # face OBJ 파일 불러오기
    bpy.ops.import_scene.obj(filepath=obj_file_path)

    bpy.ops.object.select_all(action='SELECT')
    # 불러온 객체에 쉐이드 스무스 적용
    bpy.ops.object.shade_smooth()

    material = bpy.data.materials.new(name="default_mat")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    if bsdf is not None:
        texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(os.path.join(export_file_path, 'texture.png'))
        material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    # 불러온 객체에 재질 적용
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if len(obj.data.materials) == 0:
                obj.data.materials.append(material)
            else:
                obj.data.materials[0] = material



    bpy.ops.export_scene.fbx(filepath=os.path.join(export_file_path, f"{product_idx}.fbx"))
    bpy.ops.export_scene.gltf(filepath=os.path.join(export_file_path, f"{product_idx}.glb"), export_format="GLB")

