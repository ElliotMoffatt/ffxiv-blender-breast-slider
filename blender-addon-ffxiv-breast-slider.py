bl_info = {
    "name": "XIV Breast Slider",
    "author": "munkfish",
    "description": "Panel with slider for resizing the breasts of the default FFXIV armature, accurate to ingame slider",
    "version": (1,0,1),
    "location": "3D View > Sidebar",
    "blender": (3, 0, 0),
    "category": "Object",
    "doc_url": "https://github.com/ElliotMoffatt/ffxiv-blender-breast-slider",
    "tracker_url": "https://github.com/ElliotMoffatt/ffxiv-blender-breast-slider/issues"
}

import bpy
from mathutils import Vector
import math
import numpy as np

c_mune_l_name = "j_mune_l"
c_mune_r_name = "j_mune_r"


class BREASTSCALER_PT_BreastScalerPanel(bpy.types.Panel):
    bl_idname = 'BREASTSCALER_PT_breast_scaler_panel'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "XIV Breast slider"
    bl_category = "XIV Breast slider"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col_a = layout.column()
        col_a.prop(scene, 'selectedArmature')
        
        col_d = layout.column()
        col_d.prop(scene, 'isAutomaticBoneOrientationUsed')
        
        col_b = layout.column()
        col_b.prop(scene, 'breastScalePercentage', text="Breast scale (%)", slider=True )
        
        col_c = layout.column()
        col_c.operator('breastscaler.breast_size_reset_operator', text="Reset breast size")
  
  
        
class BREASTSCALER_OT_BreastSizeResetOperator(bpy.types.Operator):
    bl_idname = 'breastscaler.breast_size_reset_operator'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Breast scaler reset"
    bl_description = "Reset breast scale to 50%"
    bl_category = "Breast scaler"
    
    def execute(self, context):
        context.scene.breastScalePercentage = 50
        return {'FINISHED'}

def get_breast_bone_names():
    return [c_mune_l_name, c_mune_r_name]


def get_breast_bones(skeleton):
    bones = []
    for name in get_breast_bone_names():
        bones.append(skeleton.pose.bones[name])
    return bones

def get_new_breast_width(scale):
    return (0.16 * scale + 92) / 100

def get_new_breast_depth(scale):
    return (0.368 * scale + 81.6) / 100

def get_new_breast_height(scale):
    return (0.4 * scale + 80) / 100

def get_new_breast_size_vector(scale, isAutomaticBoneOrientationUsed):
    newWidth = get_new_breast_width(scale)
    newDepth = get_new_breast_depth(scale)
    newHeight = get_new_breast_height(scale)
    
    if isAutomaticBoneOrientationUsed:
        return Vector((newHeight, newWidth, newDepth))
    else:
        return Vector((newWidth, newDepth, newHeight))
    


    
def update_breast_size_on_armature(armature, breastScalePercentage, isAutomaticBoneOrientationUsed):
    if armature:
        bones = get_breast_bones(armature)
        
        for bone in bones:
            bone.scale = get_new_breast_size_vector(breastScalePercentage, isAutomaticBoneOrientationUsed)
    


def do_update_breast_size( self, context ):
    update_breast_size_on_armature(context.scene.selectedArmature, self.breastScalePercentage, self.isAutomaticBoneOrientationUsed)
    

def register():
        
    bpy.types.Scene.selectedArmature = bpy.props.PointerProperty(
        type = bpy.types.Object,
        name = "Armature to scale Breasts",
        update = do_update_breast_size
    )
    
    bpy.types.Scene.isAutomaticBoneOrientationUsed = bpy.props.BoolProperty(
        default = False,
        name = "'Automatic bone orientation' used",
        description = "Select this if you selected the 'Armature > Automatic Bone Orientation' option when importing",
        update = do_update_breast_size
    )
    
    
    bpy.types.Scene.breastScalePercentage = bpy.props.FloatProperty(
        name = "Breast scale (%)", 
        description = "0% to 300%. Backspace to reset to 50%", 
        min = 0.0, 
        max = 300, 
        default = 50,
        step = 100,
        subtype = 'PERCENTAGE',
        update=do_update_breast_size )
        
    bpy.utils.register_class(BREASTSCALER_OT_BreastSizeResetOperator)
    bpy.utils.register_class(BREASTSCALER_PT_BreastScalerPanel)

def unregister():
    bpy.utils.unregister_class(BREASTSCALER_PT_BreastScalerPanel)
    bpy.utils.unregister_class(BREASTSCALER_OT_BreastSizeResetOperator)
    del bpy.types.Scene.breastScalePercentage
    del bpy.types.Scene.selectedArmature
    del bpy.types.Scene.isAutomaticBoneOrientationUsed
