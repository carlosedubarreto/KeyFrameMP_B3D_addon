import bpy
from . keyframe_connect import Set_offset_kfp #,check_sync #para pegar o numero do offset e usar no label

class Panel_kfp(bpy.types.Panel):
    bl_idname = "KEYFRAME_PT_Panel"
    bl_label = "KeyFrameMP"
    bl_category = "KeyFrameMP"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    
    global percent_render_var
    def draw(self, context):
        global percent_render_var
        layout = self.layout
        #salva opcoes na cena (por enquanto apenas o booleano esta sendo guardado)
        scene = context.scene
        # mytool = scene.my_tool
        percentage = scene.percentage
        percent_render_var = percentage.percentage
        

        layout.label(text=" Basics:")
        row = layout.row()
        row.operator('view3d.open_software', text="Open Keyframe")
        row.operator('import_test.some_data', text='Open File')
        
        
        layout.label(text=" Control:")
        row = layout.row()
        row.operator('view3d.play', text='Play')
        row.operator('view3d.stop', text="Stop")
        row = layout.row()
        row.operator('view3d.prev_frame', text='<')
        row.operator('view3d.next_frame', text='>') 
        layout.separator() 
        layout.separator()      
        row = layout.row()
        row.operator('view3d.first_frame', text='|<<')
        row.operator('view3d.last_frame', text='>>|')
        # layout.label(text=" Bookmark:")
        # row = layout.row()
        # row.operator('view3d.prev_bookmark', text="<")
        # row.operator('view3d.next_bookmark', text=">")
        layout.label(text=" Frame:")
        row = layout.row()
        row.operator('view3d.frame_bl_to_kfp', text="From Blender to Keyframe")
        row.operator('view3d.frame_kfp_to_bl', text="From KeyFrame to Blender")

        layout.label(text=" Offset :"+Set_offset_kfp.send_offset())
        row = layout.row()
        # row.operator('view3d.set_offset_bl', text="Offset on Blender")
        row.operator('view3d.set_offset_kfp', text="On KeyFrame")
        row.operator('view3d.clear_offset', text="Clear")
        layout.separator()
        # layout.label(text=" Sync:"+str(check_sync))
        layout.label(text=" Sync:")
        row = layout.row()
        row.operator('view3d.register_timer', text="Sync")
        row.operator('view3d.unregister_timer', text="Unsync")

        layout.label(text="ViewPort Animation:")
        layout.label(text="Frame Preview:"+ str(bpy.context.scene.use_preview_range))
        row = layout.row()
        row.operator('view3d.viewport_animation', text="Render")

        layout.prop(percentage, "percentage", text="Percentage")
        



        # row = self.layout.row() #exemplo passando state por botao
        # row.operator('view3d.frame_kfp_to_bl', text='Deselect').state = False
        # row.operator('view3d.frame_kfp_to_bl', text='Select').state = True
        
        # layout.prop(mytool, "bool_sound", text="Sound")
        
        # check if bool property is enabled
        # if (mytool.bool_sound == True):
        #     print ("Sound Enabled")
        # else:
        #     print ("Sound Disabled")
        
    
    # def send_bool_sound(self,context):
    #     scene = context.scene
    #     mytool = scene.my_tool
    #     bool_snd = mytool.bool_sound
    #     print("resultado bool_smns", bool_snd)
    #     return bool_snd

    def send_percent_render():
        global percent_render_var
        return int(percent_render_var)

from bpy.props import (#StringProperty,
                       BoolProperty,
                      IntProperty,
                      FloatProperty,
#                       FloatVectorProperty,
#                       EnumProperty,
                    #    PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

class MySettings(PropertyGroup):
    bool_sound : BoolProperty(
        name="Enable or Disable",
        description="Enable or disable sound",
        default = False
        )

class MySettingsPerc(PropertyGroup):
    percentage: IntProperty(name="percent", description="Percentage", default=50, min=0, max=100)