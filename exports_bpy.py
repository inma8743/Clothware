import bpy
import os

def export_3d_path(product_idx):
    return os.path.join('./uploads/stylechain/product', '3d', product_idx)

def exports_3dModeling(product_idx):
    export_file_path = export_3d_path(product_idx)
    obj_file_path = os.path.join('./uploads/stylechain/product', '3d', product_idx, 'digital_TShirt.obj')

    # 기존에 불러온 모든 객체 제거
    bpy.ops.wm.read_factory_settings(use_empty=True)

    material = bpy.data.materials.new(name="default_mat")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    if bsdf is not None:
        texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(os.path.join(export_file_path, 'texture.png'))
        material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    # face OBJ 파일 불러오기
    bpy.ops.import_scene.obj(filepath=obj_file_path)

    # 마지막으로 불러온 객체 선택
    clothes_obj = bpy.context.selected_objects[0]
    # 머티리얼 설정
    clothes_obj.data.materials[0] = material

    mesh_object = bpy.data.objects["tshirt"]  # 메쉬 오브젝트 이름으로 대체
    bpy.context.view_layer.objects.active = mesh_object
    mesh_object.select_set(True)

    bpy.ops.object.shade_smooth()

    bpy.ops.export_scene.fbx(filepath=os.path.join(export_file_path, f"{product_idx}.fbx"))
    bpy.ops.export_scene.gltf(filepath=os.path.join(export_file_path, f"{product_idx}.glb"), export_format="GLB")

