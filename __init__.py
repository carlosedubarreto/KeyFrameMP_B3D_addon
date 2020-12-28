# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# beta 0.3
# - frame navigation (next,previous, first and last frame)
# - slider to ajust quality for viewport rendering (to speed the render)
# - now you dont need to change the output to video format to make the render button work

bl_info = {
    "name" : "KeyframeMP Connector",
    "author" : "Carlos Barreto",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 3),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}
import bpy
from . keyframe_connect import (
                        Stop_video, 
                        Play_video, 
                        ImportSomeData, 
                        frame_bl_to_kfp, 
                        frame_kfp_to_bl, 
                        Open_keyframe,
                        Register_Timer,
                        Unregister_Timer,
                        Set_offset_kfp,
                        Clear_offset,
                        Prev_bookmark,
                        Next_bookmark,
                        Render_Viewport,
                        First_frame,
                        Last_frame,
                        Prev_frame,
                        Next_frame,
                        # ,Set_offset_kfp
                        # Set_offset_bl
                        )
from . panel import Panel_kfp, MySettingsPerc,MySettings

from bpy.props import (#StringProperty,
                    #    BoolProperty,
                      IntProperty,
                      FloatProperty,
#                       FloatVectorProperty,
#                       EnumProperty,
                       PointerProperty,
                       )




classes = (
    MySettings,
    MySettingsPerc,
    Panel_kfp,
    Stop_video, 
    Play_video, 
    Register_Timer,
    Unregister_Timer,
    ImportSomeData, 
    frame_bl_to_kfp, 
    frame_kfp_to_bl,
    Open_keyframe,
    # Set_offset_bl,
    Set_offset_kfp,
    Clear_offset,
    Prev_bookmark,
    Next_bookmark,
    Render_Viewport,
    First_frame,
    Last_frame,
    Prev_frame,
    Next_frame
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)
    bpy.types.Scene.percentage = PointerProperty(type=MySettingsPerc)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls) 


# def register():
#     bpy.utils.register_class(Open_keyframe)
#     bpy.utils.register_class(Stop_video)
#     bpy.utils.register_class(ImportSomeData)
#     bpy.utils.register_class(frame)
#     bpy.utils.register_class(Play_video)
#     bpy.utils.register_class(Panel_kfp)

# def unregister():
#     bpy.utils.unregister_class(Open_keyframe)
#     bpy.utils.unregister_class(Stop_video)
#     bpy.utils.unregister_class(ImportSomeData)
#     bpy.utils.unregister_class(frame)
#     bpy.utils.unregister_class(Play_video)
#     bpy.utils.unregister_class(Panel_kfp)
