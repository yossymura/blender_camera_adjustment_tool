'''
Adjust Camera Settings Addon (C) 2021 yossymura
Created by yossymura
License : GNU General Public License version3 (http://www.gnu.org/licenses/)
'''

bl_info = {
    "name" : "Camera Adjustment Tool",
    "author" : "yossymura",
    "version" : (1, 0, 0),
    "blender" : (2, 91, 0),
    "location" : "3D View",
    "description" : "Adjust Camera Settings",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "UI"
}

import bpy
from bpy.props import *
from bpy.types import Operator, AddonPreferences, Panel, PropertyGroup
import math


class CAT_MT_AddonPref(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Link:")
        row.operator( "wm.url_open", text="yossymura_3d", icon="URL").url = "https://twitter.com/yossymura_3d"


class CAT_PT_Panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'カメラ'
    bl_label = "カメラ調整"

    def draw(self, context):
        layout = self.layout
        props = context.scene.props
        wm = context.window_manager.props

        def set_cam_list(collection, cam_list):
            if collection.children:
                for child in collection.children:
                    set_cam_list(child, cam_list)
            camera_names = [cam.name for cam in collection.objects if cam.type=='CAMERA']
            if camera_names:
                camera_names.sort(key=str.lower)
                cam_list.append((collection.name, camera_names))
        
        cam_list=[]
        collections = context.scene.collection
        set_cam_list(collections, cam_list)
        cam_list.sort()

        if not cam_list:
            row = layout.row(align=False)
            row.alignment = "CENTER"
            row.alert = True
            row.label(text="カメラがありません", icon= "ERROR")
        else:
            row = layout.row(align=False)
            row.label(text="カメラ選択")
            
            box = layout.box()
            row = box.row(align=False)
            row.label(text="コレクション")
            row.prop(props, 'disp_collection', expand=True)
            disp_collection = props.disp_collection

            for coll in cam_list:
                if disp_collection == "on":
                    row = box.row(align=False)
                    row.label(text=coll[0])
                for cam in coll[1]:
                    row = box.row(align=True)
                    row.operator("cameras.select_object", text=cam, icon="VIEW_CAMERA"
                    if context.object == context.scene.objects[cam] else "CAMERA_DATA").camera = cam

            box = layout.box()
            row = box.row(align = False)
            row.label(text="カメラビュー切替")
            row.operator(
                "cameras.off_camera_view" if context.area.spaces[0].region_3d.view_perspective == 'CAMERA' else "cameras.on_camera_view",
                text="ON / OFF",
                icon="CHECKBOX_HLT" if context.area.spaces[0].region_3d.view_perspective == 'CAMERA' else "CHECKBOX_DEHLT")

            row = layout.row(align = True)
            row.alignment = "LEFT"
            row.prop(wm, "ui_direct", icon="TRIA_DOWN" if wm.ui_direct else "TRIA_RIGHT", emboss=False)
            if wm.ui_direct:
                objects = context.selected_objects
                if len(objects) == 1 and objects[0].type == 'CAMERA':
                    box = layout.box()
                    row = box.row(align=False)
                    if context.area.spaces[0].region_3d.view_perspective == 'CAMERA':
                        row = box.row(align=False)
                        row.operator("cameras.fly_mode", text="角度(フライモード)")

                    row = box.row(align=False)
                    row.operator("cameras.position_manual", text="位置")
                    
                    row = box.row(align=False)
                    row.operator("cameras.rotate_manual", text="回転")

                    row = box.row(align=False)
                    row.operator("cameras.zoom_manual", text="ズーム")
                else:
                    row = layout.row(align=False)
                    row.alignment = "CENTER"
                    row.alert = True
                    row.label(text="調整するカメラを選択してください", icon= "ERROR")

            row = layout.row(align = True)
            row.alignment = "LEFT"
            row.prop(wm, "ui_to_target", icon="TRIA_DOWN" if wm.ui_to_target else "TRIA_RIGHT", emboss=False)

            if wm.ui_to_target:
                objects = context.selected_objects
                if len(objects) == 1 and objects[0].type == 'CAMERA':

                    box = layout.box()
                    row = box.row(align=False)
                    row.prop(props,"target_Pointer",text="ターゲット")
                    row = box.row(align=False)
                    row.label(text="距離(m):")
                    row.prop(props,"angle_distance",text="")
                    row = box.row(align=False)
                    row.label(text="向き")
                    row.prop(props, 'angle_direction', expand=True)
                    
                    row = box.row(align=False)
                    angle_left_up = row.operator("cameras.to_target", text="↘").direction = "left_up"
                    angle_up = row.operator("cameras.to_target", text="↓").direction = "up"
                    angle_right_up = row.operator("cameras.to_target", text="↙").direction = "right_up"

                    row = box.row(align=False)
                    angle_left = row.operator("cameras.to_target", text="→").direction = "left"
                    angle_center = row.operator("cameras.to_target", text="正面").direction = "center"
                    angle_right = row.operator("cameras.to_target", text="←").direction = "right"

                    row = box.row(align=False)
                    angle_left_down = row.operator("cameras.to_target", text="↗").direction = "left_down"
                    angle_down = row.operator("cameras.to_target", text="↑").direction = "down"
                    angle_right_down = row.operator("cameras.to_target", text="↖").direction = "right_down"

                    row = box.row(align=False)
                    angle_side_left = row.operator("cameras.to_target", text="→→").direction = "side_left"
                    angle_side_right = row.operator("cameras.to_target", text="←←").direction = "side_right"

                else:
                    row = layout.row(align=False)
                    row.alignment = "CENTER"
                    row.alert = True
                    row.label(text="調整するカメラを選択してください", icon= "ERROR")

            row = layout.row(align = True)
            row.alignment = "LEFT"
            row.prop(wm, "ui_others", icon="TRIA_DOWN" if wm.ui_others else "TRIA_RIGHT", emboss=False)

            if wm.ui_others:
                objects = context.selected_objects
                if len(objects) == 1 and objects[0].type == 'CAMERA':
                    
                    layout.label(text="一定間隔でズーム")
                    box = layout.box()
                    row = box.row(align=False)
                    row.label(text="移動距離(m):")
                    row.prop(props,"move_distance",text="")

                    row = box.row(align=False)
                    row.operator("cameras.zoom", text="ズームイン").in_out = 'in'
                    row.operator("cameras.zoom", text="ズームアウト").in_out = 'out'

                    layout.label(text="角度")
                    box = layout.box()
                    row = box.row(align=False)
                    row.operator("cameras.set_horizen", text="水平に")

                else:
                    row = layout.row(align=False)
                    row.alignment = "CENTER"
                    row.alert = True
                    row.label(text="調整するカメラを選択してください", icon= "ERROR")


class CAT_WindowManager(PropertyGroup):
    ui_to_target : BoolProperty(name="ターゲットへ向ける")
    ui_direct : BoolProperty(name="直接調整")
    ui_others : BoolProperty(name="その他")


class CAT_Props(PropertyGroup):
    target_Pointer  : bpy.props.PointerProperty(name="Target Object",type=bpy.types.Object)
    angle_distance  : bpy.props.FloatProperty(default=5.00, name="Float",min=0)
    change_angle    : bpy.props.FloatProperty(default=5.00, name="Float",min=0)
    angle_direction : bpy.props.EnumProperty(default="front",name="Enum", items=[("front", "前から", "ターゲットの前から映す", "", 0),("back", "後ろから", "ターゲットの後ろから映す","", 1)])
    disp_collection : bpy.props.EnumProperty(default="off",name="Enum", items=[("on", "表示", "コレクション名を表示", "", 1),("off", "非表示", "コレクション名を非表示","", 0)])
    move_distance  : bpy.props.FloatProperty(default=1.00, name="Float",min=0)


class Set_Camera_To_Target(bpy.types.Operator):
    bl_idname = 'cameras.to_target'
    bl_label = 'Set Camera To Target'
    bl_description = "Set Camera To Target"
    bl_options = {'UNDO'}
    direction: bpy.props.StringProperty(default="")

    def execute(self,context):
        if context.scene.props.target_Pointer is not None:
            camera = context.selected_objects[0]
            
            target = context.scene.props.target_Pointer
            camera.location = target.location
            camera.rotation_euler = target.rotation_euler
            
            angle_direction = context.scene.props.angle_direction
            angle_distance = context.scene.props.angle_distance

            front_back, up_down, left_right, side = 1, 0, 0, 1
            
            if 'front' == angle_direction:
                front_back = 1
            if 'back' == angle_direction:
                front_back = -1
                
            if 'up' in self.direction:
                up_down = 1
            if 'down' in self.direction:
                up_down = -1
            if 'left' in self.direction:
                left_right = 1
            if 'right' in self.direction:
                left_right = -1
            if 'side' in self.direction:
                side = 0

            x = (front_back * -1) * left_right * angle_distance
            y = (front_back * -1) * angle_distance * side
            z = up_down * angle_distance
            bpy.ops.transform.translate(value=(x, y, z), orient_type='LOCAL')

            target.select_set(True)
            bpy.context.view_layer.objects.active = target
            bpy.ops.object.track_set(type='TRACKTO')
            bpy.ops.object.track_clear(type='CLEAR_KEEP_TRANSFORM')
            target.select_set(False)
            bpy.context.view_layer.objects.active = camera

        return{'FINISHED'}


class Set_Camera_Level(bpy.types.Operator):
    bl_idname = 'cameras.set_horizen'
    bl_label = 'Set Horizen'
    bl_description = "set horizen"
    bl_options = {'UNDO'}

    def execute(self,context):
        camera = context.selected_objects[0]
        z = camera.rotation_euler.z
        camera.rotation_euler = (math.radians(90), 0, z)

        return{'FINISHED'}


class Select_Camera(bpy.types.Operator):
    bl_idname = 'cameras.select_object'
    bl_label = 'Select Camera'
    bl_description = "Select camera"
    bl_options = {'UNDO'}

    camera: bpy.props.StringProperty()

    def execute(self,context):
        if context.object:
            if context.object.select_get():
                context.object.select_set(state=False)
        cam = bpy.data.objects[self.camera]
        cam.select_set(state=True)
        context.view_layer.objects.active = cam
        context.scene.camera = cam
        
        return{'FINISHED'}


class On_Camera_View(bpy.types.Operator):
    bl_idname = 'cameras.on_camera_view'
    bl_label = 'Camera View On'
    bl_description = "Camera View On"
    bl_options = {'UNDO'}

    def execute(self,context):
        context.area.spaces[0].region_3d.view_perspective = 'CAMERA'
        
        return{'FINISHED'}


class Off_Camera_View(bpy.types.Operator):
    bl_idname = 'cameras.off_camera_view'
    bl_label = 'Camera View Off'
    bl_description = "Camera View Off"
    bl_options = {'UNDO'}

    def execute(self,context):
        context.area.spaces[0].region_3d.view_perspective='PERSP'

        return{'FINISHED'}

class Fly_Mode(bpy.types.Operator):
    bl_idname = 'cameras.fly_mode'
    bl_label = 'Fly mode'
    bl_description = "'Fly mode"
    bl_options = {'UNDO'}

    def execute(self,context):
        bpy.ops.view3d.navigate('INVOKE_DEFAULT')

        return{'FINISHED'}
        

class Zoom_Camera(bpy.types.Operator):
    bl_idname = 'cameras.zoom'
    bl_label = 'Zoom in/out'
    bl_description = "Zoom in/out"
    bl_options = {'UNDO'}
    in_out: bpy.props.StringProperty(default="")

    def execute(self,context):
        camera = context.selected_objects[0]
        move_distance = context.scene.props.move_distance

        if 'in' == self.in_out:
            bpy.ops.transform.translate(value=(0, 0, -move_distance), orient_type='LOCAL')
        else:
            bpy.ops.transform.translate(value=(0, 0, move_distance), orient_type='LOCAL')

        return{'FINISHED'}


class Zoom_Camera_Manual(bpy.types.Operator):
    bl_idname = 'cameras.zoom_manual'
    bl_label = 'Zoom in/out manual'
    bl_description = "Zoom in/out manual"
    bl_options = {'UNDO'}

    def execute(self,context):
        bpy.ops.transform.translate('INVOKE_DEFAULT', constraint_axis=(False, False, True), orient_type='LOCAL')

        return{'FINISHED'}


class Translate_Camera_Manual(bpy.types.Operator):
    bl_idname = 'cameras.position_manual'
    bl_label = 'Position manual'
    bl_description = "Position manual"
    bl_options = {'UNDO'}

    def execute(self,context):
        bpy.ops.transform.translate('INVOKE_DEFAULT')

        return{'FINISHED'}


class Rotate_Camera_Manual(bpy.types.Operator):
    bl_idname = 'cameras.rotate_manual'
    bl_label = 'Rotate manual'
    bl_description = "Rotate manual"
    bl_options = {'UNDO'}

    def execute(self,context):
        bpy.ops.transform.rotate('INVOKE_DEFAULT')

        return{'FINISHED'}


classes = (
CAT_MT_AddonPref,
CAT_Props,
CAT_WindowManager,
CAT_PT_Panel,
Set_Camera_To_Target,
Set_Camera_Level,
Select_Camera,
Off_Camera_View,
On_Camera_View,
Fly_Mode,
Zoom_Camera,
Zoom_Camera_Manual,
Translate_Camera_Manual,
Rotate_Camera_Manual,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.props = PointerProperty(type=CAT_WindowManager)
    bpy.types.Scene.props = bpy.props.PointerProperty(type = CAT_Props)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.props
    del bpy.types.WindowManager.props


if __name__ == "__main__":
    register()