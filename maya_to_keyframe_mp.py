import datetime
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import traceback

# import maya.cmds as cmds
# import maya.mel as mel
# import maya.OpenMaya as om


# class MayaToKeyframeMP(object):

#     WINDOW_NAME = "MayaToKeyframeMP"
#     WINDOW_TITLE = "Maya to Keyframe MP"

#     VERSION = "2.9.1"

#     KEYFRAME_MP_PATH = ""
#     if sys.platform == "win32":
#         KEYFRAME_MP_PATH = "C:/Program Files/Keyframe MP 2/bin/KeyframeMP.exe"
#     elif sys.platform == "darwin":
#         KEYFRAME_MP_PATH = "/Applications/KeyframeMP2.app/Contents/MacOS/KeyframeMP2"
#     else:
#         om.MGlobal.displayError("MayaToKeyframeMP is not supported on the current platform ({0})".format(sys.platform))

#     PORT = 17174

#     SYNC_SCRIPT_NODE_NAME = "MayaToKeyframeMPScriptNode"

#     CACHED_TEMP_DIR_OPTION_VAR = "MayaToKeyframeMPCachedTempDir"
#     COLLAPSE_STATE_OPTION_VAR = "MayaToKeyframeMPCollapseState"
#     SYNC_OFFSET_OPTION_VAR = "MayaToKeyframeMPSyncOffset"
#     FROM_RANGE_START_OPTION_VAR = "MayaToKeyframeMPFromRangeStart"
#     SYNC_MULTIPLIER_OPTION_VAR = "MayaToKeyframeMPSyncMultiplier"

#     WAIT_FOR_OPEN_DURATION = 1  # Seconds to sleep after trying to open the application

#     BUTTON_COLOR_01 = (0.5, 0.5, 0.5)
#     BUTTON_COLOR_02 = (0.361, 0.361, 0.361)

#     SYNC_ACTIVE_COLOR = (0.0, 0.5, 0.0)

#     kmp_client = None

#     main_window = None
#     sync_layout = None
#     viewer_layout = None
#     playblast_layout = None

#     sync_from_range_start_cb = None
#     sync_offset_ifg = None
#     playblast_viewer_rbg = None

#     @classmethod
#     def open_keyframe_mp(cls, application_path=""):
#         """
#         Open the Keyframe MP application.

#         :param application_path: Application path override.
#         """
#         if not application_path:
#             application_path = cls.KEYFRAME_MP_PATH

#         if not application_path:
#             om.MGlobal.displayError("Keyframe MP application path not set.")
#         elif not os.path.exists(application_path):
#             om.MGlobal.displayError("Keyframe MP application path does not exist: {0}".format(application_path))
#         else:
#             try:
#                 subprocess.Popen(cls.KEYFRAME_MP_PATH, shell=False, stdin=None, stdout=None, stderr=None)
#             except:
#                 traceback.print_exc()
#                 om.MGlobal.displayError("Failed to open Keyframe MP. See script editor for details.")

#     @classmethod
#     def is_initialized(cls, display_errors=True):
#         """
#         Check to see if Keyframe MP is initialized.

#         :param display_errors: Show/hide error messages.
#         :return: True if initialized. False otherwise.
#         """
#         if not cls.kmp_client:
#             cls.kmp_client = KeyframeMPClient()

#         if cls.kmp_client.connect(port=cls.PORT, display_errors=display_errors):
#             if cls.kmp_client.initialize():
#                 return True
#         else:
#             if display_errors:
#                 om.MGlobal.displayError("Connection failed. Application may be closed or the port may be in use ({0}).".format(cls.PORT))

#         if display_errors:
#             om.MGlobal.displayError("Failed to connect to Keyframe MP. See script editor for details.")

#         return False

#     @classmethod
#     def toggle_sync(cls):
#         """
#         Toggle timeline sync with Keyframe MP.
#         """
#         if not cls.sync_script_node_exists() and cls.is_initialized():
#             cls.create_sync_script_node()
#             if cls.sync_script_node_exists():
#                 cls.update_sync_time()
#         else:
#             cls.delete_sync_script_node()
#             cls.kmp_client.disconnect()

#         cls.update_sync_state()

#     @classmethod
#     def update_sync_time(cls):
#         """
#         Set the Keyframe MP frame to the current Maya frame.
#         """
#         if cls.sync_script_node_exists():
#             frame = cmds.currentTime(q=True) + cls.get_sync_offset()
#             frame = int((frame - 1) * cls.get_sync_multiplier()) + 1

#             from_range_start = bool(cls.get_from_range_start())
#             if cls.kmp_client.set_frame(frame, False, from_range_start) <= 0:
#                 cls.toggle_sync()

#     @classmethod
#     def playblast(cls):
#         """
#         Create a playblast in the Keyframe MP temp dir using the existing playblast settings
#         and open it in Keyframe MP.
#         """
#         format = cls.get_option_var("playblastFormat", "avi")
#         ext = ""
#         if format == "avi":
#             ext = "avi"
#         elif format == "qt" or format == "avfoundation":
#             ext = "mov"
#         else:
#             om.MGlobal.displayError("Unsupported playblast format: {0}".format(format))
#             return

#         temp_dir = cls.get_temp_dir()
#         if not temp_dir:
#             om.MGlobal.displayError("Failed to get temp directory from Keyframe MP. See script editor for details.")
#             return

#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)

#         name = "blast"
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         if format == "image":
#             file_path = "{0}/{1}_{2}".format(temp_dir, name, timestamp)
#         else:
#             file_path = "{0}/{1}_{2}.{3}".format(temp_dir, name, timestamp, ext)

#         clear_cache = cls.get_option_var("playblastClearCache", True)
#         show_ornaments = cls.get_option_var("playblastShowOrnaments", False)
#         compression = cls.get_option_var("playblastCompression", "none")
#         quality = cls.get_option_var("playblastQuality", 70)
#         percent = cls.get_option_var("playblastScale", 0.5) * 100
#         padding = cls.get_option_var("playblastPadding", 4)
#         display_source_size = cls.get_option_var("playblastDisplaySizeSource", 1)
#         playblast_width = cls.get_option_var("playblastWidth", 720)
#         playblast_height = cls.get_option_var("playblastHeight", 480)

#         args = {"format": format,
#                 "clearCache": clear_cache,
#                 "viewer": False,
#                 "showOrnaments": show_ornaments,
#                 "fp": padding,
#                 "percent": percent,
#                 "compression": compression,
#                 "quality": quality,
#                 "filename": file_path
#                 }

#         if display_source_size == 2:
#             args["widthHeight"] = [cmds.getAttr("defaultResolution.w"), cmds.getAttr("defaultResolution.h")]
#         elif display_source_size == 3:
#             args["widthHeight"] = [playblast_width, playblast_height]

#         playback_slider = mel.eval("$tempVar = $gPlayBackSlider")
#         if(cmds.timeControl(playback_slider, q=True, rv=True)):
#             range = cmds.timeControl(playback_slider, q=True, ra=True)
#             args["startTime"] = range[0]
#             args["endTime"] = range[1]

#         sound = cmds.timeControl(playback_slider, q=True, sound=True)
#         if sound:
#             args["sound"] = sound

#         temp_path = cmds.playblast(**args)
#         if temp_path:
#             file_path = temp_path

#         if not os.path.exists(file_path):
#             om.MGlobal.displayError("Playblast file does not exist. See script editor for details.")
#             return

#         # Open in viewer
#         if not cls.is_initialized(False):
#             cls.open_keyframe_mp()
#             time.sleep(cls.WAIT_FOR_OPEN_DURATION)

#             if not cls.is_initialized():
#                 om.MGlobal.displayError("Failed to open in viewer. See script editor for details.")
#                 return

#         source = cls.kmp_client.import_file(file_path)
#         if not source:
#             om.MGlobal.displayError("Failed to import file. See script editor for details.")
#             return

#         autoplay = cls.kmp_client.is_autoplay()
#         if(autoplay):
#             cls.kmp_client.set_playing(autoplay)

#     @classmethod
#     def get_option_var(cls, name, default):
#         """
#         Get to value of an option variable.

#         :param name: Name of the option variable.
#         :param default: Default value if the option variable does not exist.
#         :return: The value of the option variable.
#         """
#         if cmds.optionVar(exists=name):
#             return cmds.optionVar(q=name)
#         else:
#             return default

#     @classmethod
#     def open_temp_dir(cls):
#         """
#         Open the temporary directory in Explorer.
#         """
#         temp_dir = cls.get_temp_dir()
#         if temp_dir:
#             if sys.platform == "win32":
#                 os.startfile(temp_dir, 'explore')
#             elif sys.platform == "darwin":
#                 subprocess.Popen(["open", temp_dir])
#             else:
#                 om.MGlobal.displayError("Open temp dir is not supported on the current platform ({0})".format(sys.platform))
#         else:
#             om.MGlobal.displayError("Failed to get temp directory from Keyframe MP. See script editor for details.")

#     @classmethod
#     def clear_temp_dir(cls):
#         """
#         Delete all files in the temporary directory.
#         """
#         result = cmds.confirmDialog(title='Confirm',
#                                     message='Clear temporary directory?',
#                                     button=['Yes', 'No'],
#                                     defaultButton='Yes',
#                                     cancelButton='No',
#                                     dismissString='No')
#         if result == "Yes":
#             temp_dir = cls.get_temp_dir()
#             if temp_dir:
#                 errors_occurred = False

#                 for the_file in os.listdir(temp_dir):
#                     file_path = os.path.join(temp_dir, the_file)
#                     try:
#                         if os.path.isfile(file_path):
#                             os.unlink(file_path)
#                         elif os.path.isdir(file_path):
#                             shutil.rmtree(file_path)
#                     except:
#                         om.MGlobal.displayWarning("Failed to remove file: {0}".format(file_path))
#                         om.MGlobal.displayWarning("File may be open in an application")
#                         errors_occurred = True

#                 if errors_occurred:
#                     om.MGlobal.displayWarning("Unable to remove all files. See script editor for details.")
#                 else:
#                     om.MGlobal.displayInfo("Temporary directory cleared: {0}".format(temp_dir))
#             else:
#                 om.MGlobal.displayError("Failed to get temp directory from Keyframe MP. See script editor for details.")

#     @classmethod
#     def get_temp_dir(cls):
#         """
#         Get the temporary directory path.

#         :return: The path of the temporary directory.
#         """
#         if cls.is_initialized(display_errors=False):
#             config = cls.kmp_client.get_config()
#             if config:
#                 cmds.optionVar(sv=[cls.CACHED_TEMP_DIR_OPTION_VAR, config["temp_dir"]])
#                 return config["temp_dir"]

#         temp_dir = cls.get_option_var(cls.CACHED_TEMP_DIR_OPTION_VAR, "")
#         if not temp_dir:
#             cls.open_keyframe_mp()
#             time.sleep(cls.WAIT_FOR_OPEN_DURATION)

#             if cls.is_initialized(display_errors=False):
#                 config = cls.kmp_client.get_config()
#                 if config:
#                     cmds.optionVar(sv=[cls.CACHED_TEMP_DIR_OPTION_VAR, config["temp_dir"]])
#                     return config["temp_dir"]

#         return temp_dir

#     @classmethod
#     def sync_script_node_exists(cls):
#         """
#         Check if a sync script node exists in the Maya scene.

#         :return: True if the script node exists. False otherwise.
#         """
#         return cmds.objExists(cls.SYNC_SCRIPT_NODE_NAME)

#     @classmethod
#     def create_sync_script_node(cls):
#         """
#         Create a sync script node if one does not already exist.
#         """
#         if not cls.sync_script_node_exists():
#             cmds.scriptNode(scriptType=7,
#                             beforeScript="try: MayaToKeyframeMP.update_sync_time()\nexcept: pass",
#                             name=cls.SYNC_SCRIPT_NODE_NAME,
#                             sourceType="python")

#     @classmethod
#     def delete_sync_script_node(cls):
#         """
#         Delete the sync script node if it exists.
#         """
#         if cls.sync_script_node_exists():
#             cmds.delete(cls.SYNC_SCRIPT_NODE_NAME)

#     @classmethod
#     def get_sync_offset(cls):
#         """
#         Get the current sync offset value.

#         :return: The sync offset value in frames.
#         """
#         if cmds.optionVar(exists=cls.SYNC_OFFSET_OPTION_VAR):
#             return cmds.optionVar(q=cls.SYNC_OFFSET_OPTION_VAR)
#         else:
#             return 0

#     @classmethod
#     def set_sync_offset(cls, value):
#         """
#         Set the current sync offset value.

#         :param value: New sync offset value in frames.
#         """
#         cmds.intFieldGrp(cls.sync_offset_ifg, e=True, value1=value)
#         cmds.optionVar(iv=[cls.SYNC_OFFSET_OPTION_VAR, value])
#         if (cls.sync_script_node_exists()):
#             cls.update_sync_time()

#     @classmethod
#     def get_sync_multiplier(cls):
#         if cmds.optionVar(exists=cls.SYNC_MULTIPLIER_OPTION_VAR):
#             return cmds.optionVar(q=cls.SYNC_MULTIPLIER_OPTION_VAR)
#         else:
#             return 1.0

#     @classmethod
#     def set_sync_multiplier(cls, value):
#         cmds.floatFieldGrp(cls.sync_multiplier_ffg, e=True, value1=value)
#         cmds.optionVar(fv=[cls.SYNC_MULTIPLIER_OPTION_VAR, value])
#         if (cls.sync_script_node_exists()):
#             cls.update_sync_time()

#     @classmethod
#     def sync_offset_to_current(cls):
#         """
#         Set the sync offset based on the current Maya time (frame)
#         """
#         cls.set_sync_offset(-cmds.currentTime(q=True) + 1)

#     @classmethod
#     def sync_offset_changed(cls):
#         """
#         Callback when value in the sync offset UI value changes.
#         """
#         cls.set_sync_offset(cmds.intFieldGrp(cls.sync_offset_ifg, q=True, value1=True))

#     @classmethod
#     def sync_multiplier_changed(cls):
#         cls.set_sync_multiplier(cmds.floatFieldGrp(cls.sync_multiplier_ffg, q=True, value1=True))

#     @classmethod
#     def get_from_range_start(cls):
#         """
#         Check if sync should occur from the current range start in Keyframe MP.

#         :return: True if range shart should be used. False otherwise.
#         """
#         if cmds.optionVar(exists=cls.FROM_RANGE_START_OPTION_VAR):
#             return cmds.optionVar(q=cls.FROM_RANGE_START_OPTION_VAR)
#         else:
#             return 1

#     @classmethod
#     def update_from_range_start(cls):
#         """
#         Callback when the range start checkbox (in the UI) changes.
#         """
#         value = cmds.checkBox(cls.sync_from_range_start_cb, q=True, value=True)
#         cmds.optionVar(iv=[cls.FROM_RANGE_START_OPTION_VAR, value])

#         if cls.sync_script_node_exists():
#             cls.update_sync_time()

#     @classmethod
#     def get_collapse_state(cls):
#         """
#         Get the UI collapse state.

#         :return: The UI collapse state.
#         """
#         if cmds.optionVar(exists=cls.COLLAPSE_STATE_OPTION_VAR):
#             collapse_state = cmds.optionVar(q=cls.COLLAPSE_STATE_OPTION_VAR)
#             if len(collapse_state) == 2:
#                 for value in collapse_state:
#                     if value < 0 or value > 1:
#                         return [0, 1]

#                 return collapse_state

#         return [0, 1]

#     @classmethod
#     def update_collapse_state(cls):
#         """
#         Update the collapse state option variable.
#         """
#         cmds.optionVar(clearArray=cls.COLLAPSE_STATE_OPTION_VAR)
#         layouts = [cls.sync_layout, cls.playblast_layout]
#         for layout in layouts:
#             collapse = cmds.frameLayout(layout, q=True, cl=True)
#             cmds.optionVar(iva=[cls.COLLAPSE_STATE_OPTION_VAR, collapse])

#     @classmethod
#     def display(cls):
#         """
#         Create and display the User Interface.
#         """
#         if cmds.window(cls.WINDOW_NAME, exists=True):
#             cmds.deleteUI(cls.WINDOW_NAME, window=True)

#         collapse_state = cls.get_collapse_state()

#         # ---------------------------------------------------------------------
#         # Main layout
#         # ---------------------------------------------------------------------
#         cls.main_window = cmds.window(cls.WINDOW_NAME, title=cls.WINDOW_TITLE, s=True, tlb=False, rtf=True, mnb=False, mxb=False)
#         main_layout = cmds.formLayout(parent=cls.main_window)

#         cls.sync_layout = cmds.frameLayout(parent=main_layout,
#                                            label="Sync", collapsable=True,
#                                            cl=collapse_state[0],
#                                            cc='cmds.evalDeferred("MayaToKeyframeMP.on_collapse_changed()")',
#                                            ec='cmds.evalDeferred("MayaToKeyframeMP.on_collapse_changed()")')
#         sync_form_layout = cmds.formLayout(parent=cls.sync_layout)

#         cls.playblast_layout = cmds.frameLayout(parent=main_layout,
#                                                 label="Playblast",
#                                                 collapsable=True,
#                                                 cl=collapse_state[1],
#                                                 cc='cmds.evalDeferred("MayaToKeyframeMP.on_collapse_changed()")',
#                                                 ec='cmds.evalDeferred("MayaToKeyframeMP.on_collapse_changed()")')
#         playblast_form_layout = cmds.formLayout(parent=cls.playblast_layout)

#         cmds.formLayout(main_layout, e=True, af=(cls.sync_layout, "top", 0))
#         cmds.formLayout(main_layout, e=True, af=(cls.sync_layout, "left", 0))
#         cmds.formLayout(main_layout, e=True, af=(cls.sync_layout, "right", 0))

#         cmds.formLayout(main_layout, e=True, ac=(cls.playblast_layout, "top", 0, cls.sync_layout))
#         cmds.formLayout(main_layout, e=True, af=(cls.playblast_layout, "left", 0))
#         cmds.formLayout(main_layout, e=True, af=(cls.playblast_layout, "right", 0))

#         # ---------------------------------------------------------------------
#         # Sync layout
#         # ---------------------------------------------------------------------
#         cls.sync_offset_ifg = cmds.intFieldGrp(label="Offset: ",
#                                                value1=MayaToKeyframeMP.get_sync_offset(),
#                                                columnWidth2=(56, 48),
#                                                cl2=("right", "right"),
#                                                cc="MayaToKeyframeMP.sync_offset_changed()",
#                                                parent=sync_form_layout)

#         cls.sync_from_range_start_cb = cmds.checkBox(label="From Range Start",
#                                                      value=MayaToKeyframeMP.get_from_range_start(),
#                                                      cc="MayaToKeyframeMP.update_from_range_start()",
#                                                      parent=sync_form_layout)

#         sync_offset_to_current_btn = cmds.button(label="Current",
#                                                  bgc=cls.BUTTON_COLOR_01,
#                                                  c="MayaToKeyframeMP.sync_offset_to_current()",
#                                                  parent=sync_form_layout)

#         reset_sync_offset_btn = cmds.button(label="  Reset  ",
#                                             bgc=cls.BUTTON_COLOR_01,
#                                             c="MayaToKeyframeMP.set_sync_offset(0)",
#                                             parent=sync_form_layout)

#         cls.sync_multiplier_ffg = cmds.floatFieldGrp(label="Multiplier: ",
#                                                      value1=MayaToKeyframeMP.get_sync_multiplier(),
#                                                      precision=2,
#                                                      columnWidth2=(56, 48),
#                                                      cl2=("right", "right"),
#                                                      cc="MayaToKeyframeMP.sync_multiplier_changed()",
#                                                      parent=sync_form_layout)

#         reset_sync_multiplier_btn = cmds.button(label="  Reset  ",
#                                                 bgc=cls.BUTTON_COLOR_01,
#                                                 c="MayaToKeyframeMP.set_sync_multiplier(1.0)",
#                                                 parent=sync_form_layout)

#         cls.sync_btn = cmds.button(label="SYNC", c="MayaToKeyframeMP.toggle_sync()", parent=sync_form_layout)

#         top_offset = 1
#         bottom_offset = 4
#         left_position = 1
#         right_position = 99
#         spacing = 2
#         cmds.formLayout(sync_form_layout, e=True, af=(cls.sync_offset_ifg, "top", top_offset))
#         cmds.formLayout(sync_form_layout, e=True, ap=(cls.sync_offset_ifg, "left", 0, left_position))

#         cmds.formLayout(sync_form_layout, e=True, af=(sync_offset_to_current_btn, "top", top_offset))
#         cmds.formLayout(sync_form_layout, e=True, ac=(sync_offset_to_current_btn, "left", 0, cls.sync_offset_ifg))

#         cmds.formLayout(sync_form_layout, e=True, af=(reset_sync_offset_btn, "top", top_offset))
#         cmds.formLayout(sync_form_layout, e=True, ac=(reset_sync_offset_btn, "left", spacing, sync_offset_to_current_btn))

#         cmds.formLayout(sync_form_layout, e=True, ac=(cls.sync_from_range_start_cb, "top", top_offset, sync_offset_to_current_btn))
#         cmds.formLayout(sync_form_layout, e=True, ap=(cls.sync_from_range_start_cb, "left", 60, left_position))

#         cmds.formLayout(sync_form_layout, e=True, ac=(cls.sync_multiplier_ffg, "top", 6, cls.sync_from_range_start_cb))
#         cmds.formLayout(sync_form_layout, e=True, ap=(cls.sync_multiplier_ffg, "left", 0, left_position))

#         cmds.formLayout(sync_form_layout, e=True, ac=(reset_sync_multiplier_btn, "top", 6, cls.sync_from_range_start_cb))
#         cmds.formLayout(sync_form_layout, e=True, ac=(reset_sync_multiplier_btn, "left", 0, cls.sync_multiplier_ffg))

#         cmds.formLayout(sync_form_layout, e=True, ac=(cls.sync_btn, "top", 4 * spacing, cls.sync_multiplier_ffg))
#         cmds.formLayout(sync_form_layout, e=True, af=(cls.sync_btn, "bottom", bottom_offset))
#         cmds.formLayout(sync_form_layout, e=True, ap=(cls.sync_btn, "left", 0, left_position))
#         cmds.formLayout(sync_form_layout, e=True, ap=(cls.sync_btn, "right", 0, right_position))

#         # ---------------------------------------------------------------------
#         # Playblast layout
#         # ---------------------------------------------------------------------
#         playblast_btn = cmds.button(label="PLAYBLAST",
#                                     bgc=cls.BUTTON_COLOR_01,
#                                     c="MayaToKeyframeMP.playblast()",
#                                     parent=playblast_form_layout)

#         open_temp_dir_btn = cmds.button(label="Open Temp Folder",
#                                         bgc=cls.BUTTON_COLOR_01,
#                                         c="MayaToKeyframeMP.open_temp_dir()",
#                                         parent=playblast_form_layout)

#         clear_temp_dir_btn = cmds.button(label="Clear Temp Folder",
#                                          bgc=cls.BUTTON_COLOR_01,
#                                          c="MayaToKeyframeMP.clear_temp_dir()",
#                                          parent=playblast_form_layout)

#         version_label = cmds.text(label="v{0}".format(cls.VERSION), align="right")

#         cmds.formLayout(playblast_form_layout, e=True, af=(playblast_btn, "top", top_offset))
#         cmds.formLayout(playblast_form_layout, e=True, ap=(playblast_btn, "left", 0, left_position))
#         cmds.formLayout(playblast_form_layout, e=True, ap=(playblast_btn, "right", 0, right_position))

#         cmds.formLayout(playblast_form_layout, e=True, ac=(open_temp_dir_btn, "top", spacing, playblast_btn))
#         cmds.formLayout(playblast_form_layout, e=True, ap=(open_temp_dir_btn, "left", 0, left_position))
#         cmds.formLayout(playblast_form_layout, e=True, ap=(open_temp_dir_btn, "right", 1, 50))

#         cmds.formLayout(playblast_form_layout, e=True, ac=(clear_temp_dir_btn, "top", spacing, playblast_btn))
#         cmds.formLayout(playblast_form_layout, e=True, ap=(clear_temp_dir_btn, "left", 1, 50))
#         cmds.formLayout(playblast_form_layout, e=True, ap=(clear_temp_dir_btn, "right", 0, right_position))

#         cmds.formLayout(playblast_form_layout, e=True, ac=(version_label, "top", spacing, open_temp_dir_btn))
#         cmds.formLayout(playblast_form_layout, e=True, ap=(version_label, "right", 0, right_position))

#         # ---------------------------------------------------------------------
#         # Update and show
#         # ---------------------------------------------------------------------
#         cls.update_sync_state()
#         cls.on_collapse_changed()
#         cmds.setFocus(cls.sync_btn)

#         cmds.showWindow(cls.main_window)

#     @classmethod
#     def on_collapse_changed(cls):
#         """
#         Callback when the UI collapse state changes.
#         """
#         total_height = 0
#         layouts = [cls.sync_layout, cls.playblast_layout]
#         for layout in layouts:
#             total_height += cmds.frameLayout(layout, q=True, h=True)

#         cmds.window(MayaToKeyframeMP.main_window, e=True, h=total_height)
#         cls.update_collapse_state()

#     @classmethod
#     def update_sync_state(cls):
#         """
#         Update the UI based on the current sync state.
#         """
#         if cls.sync_script_node_exists():
#             cmds.button(cls.sync_btn, e=True, bgc=cls.SYNC_ACTIVE_COLOR, label="SYNCED")
#         else:
#             cmds.button(cls.sync_btn, e=True, bgc=cls.BUTTON_COLOR_01, label="SYNC")


class KeyframeMPClient(object):
    """
    Client API for Keyframe MP
    """

    API_VERSION = "2.0.1"

    PORT = 17174

    HEADER_SIZE = 10

    kmp_socket = None
    kmp_initialized = False

    def __init__(self, timeout=2):
        """
        """
        self.timeout = timeout
        self.show_timeout_errors = True

    def connect(self, port=-1, display_errors=True):
        """
        Create a connection with the application.

        :param port: The port Keyframe MP is listening on.
        :return: True if connection was successful (or already exists). False otherwise.
        """
        if self.is_connected():
            return True

        if port < 0:
            port = self.__class__.PORT

        try:
            self.__class__.kmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__class__.kmp_socket.connect(("localhost", port))
            self.__class__.kmp_socket.setblocking(0)

            self.__class__.kmp_initialized = False

        except:
            self.__class__.kmp_socket = None
            if display_errors:
                traceback.print_exc()
            return False

        return True

    def disconnect(self):
        """
        Disconnect from the application.

        :return: True if the existing connection was disconnect successfully. False otherwise.
        """
        result = False
        if self.__class__.kmp_socket:
            try:
                self.__class__.kmp_socket.close()
                result = True
            except:
                traceback.print_exc()

        self.__class__.kmp_socket = None
        self.__class__.kmp_initialized = False

        return result

    def is_connected(self):
        """
        Test if a connection exists.

        :return: True if a connection exists. False otherwise.
        """
        self.show_timeout_errors = False
        connected = self.__class__.kmp_socket and self.echo("conn")
        self.show_timeout_errors = True

        if connected:
            return True
        else:
            self.disconnect()
            return False

    def send(self, cmd):
        """
        Send a command to the application and wait for a processed reply.

        :param cmd: Dictionary containing the cmd and args
        :return: Variable depending on cmd.
        """
        json_cmd = json.dumps(cmd)

        message = []
        message.append("{0:10d}".format(len(json_cmd)))  # header
        message.append(json_cmd)

        try:
            msg_str = "".join(message)
            if sys.version_info[0] == 3:
                self.__class__.kmp_socket.sendall(msg_str.encode())
            else:
                self.__class__.kmp_socket.sendall("".join(message))
        except:
            traceback.print_exc()
            return None

        return self.recv(cmd)

    def recv(self, cmd):
        """
        Wait for the application to reply to a previously sent cmd.

        :param cmd: Dictionary containing the cmd and args
        :return: Variable depending on cmd.
        """
        total_data = []
        data = ""
        reply_length = 0
        bytes_remaining = self.__class__.HEADER_SIZE

        begin = time.time()
        while time.time() - begin < self.timeout:

            try:
                data = self.__class__.kmp_socket.recv(bytes_remaining)
            except:
                time.sleep(0.01)
                continue

            if data:
                total_data.append(data)

                bytes_remaining -= len(data)
                if(bytes_remaining <= 0):

                    if sys.version_info[0] == 3:
                        for i in range(len(total_data)):
                            total_data[i] = total_data[i].decode()

                    if reply_length == 0:
                        header = "".join(total_data)
                        reply_length = int(header)
                        bytes_remaining = reply_length
                        total_data = []
                    else:
                        reply_json = "".join(total_data)
                        return json.loads(reply_json)

        if self.show_timeout_errors:
            if "cmd" in cmd.keys():
                cmd_name = cmd["cmd"]
                print('[KeyframeMP][ERROR] "{0}" timed out.'.format(cmd_name))
            else:
                print('[KeyframeMP][ERROR] Unknown cmd timed out.')

        return None

    def is_valid_reply(self, reply):
        """
        Test if a reply from the application is valid. Output any messages.

        :param reply: Dictionary containing the response to a cmd
        :return: True if valid. False otherwise.
        """
        if not reply:
            return False

        if not reply["success"]:
            print('[KeyframeMP][ERROR] "{0}" failed: {1}'.format(reply["cmd"], reply["msg"]))
            return False

        return True

    def initialize(self):
        """
        One time initialization required by the application.

        :return: True if successfully initalized. False otherwise.
        """
        if self.__class__.kmp_initialized:
            return True

        cmd = {
            "cmd": "initialize",
            "api_version": self.__class__.API_VERSION
        }

        reply = self.send(cmd)
        if reply and reply["success"] and reply["result"] == 0:
            self.__class__.kmp_initialized = True
            return True
        else:
            print('[KeyframeMP][ERROR] Initialization failed: {0}'.format(reply["msg"]))
            self.disconnect()
            return False

    # ------------------------------------------------------------------
    # COMMANDS
    # ------------------------------------------------------------------
    def echo(self, text):
        """
        Get an echo response from the application.

        :param text: The string to be sent to the application.
        :return: A string containing the text on success. None otherwise.
        """
        cmd = {
            "cmd": "echo",
            "text": text
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["result"]
        else:
            return None

    def get_config(self):
        """
        Get the configuration settings for the application.

        :return: Dictionary containing the config values.
        """
        cmd = {
            "cmd": "get_config"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply
        else:
            return None

    def set_playing(self, playing, play_forwards=True):
        """
        Set the play state to playing or paused. Option to control play direction.

        :param playing: Enable playing state
        :param play_forwards: Play direction (ignored if playing is False)
        :return: True on success. False otherwise.
        """
        cmd = {
            "cmd": "set_playing",
            "playing": playing,
            "play_forwards": play_forwards
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return True
        else:
            return False

    def is_autoplay(self):
        """
        Get the autoplay state of the player.

        :return: Autoplay state (True/False). None on error.
        """
        cmd = {
            "cmd": "is_autoplay"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["autoplay"]
        else:
            return None

    def import_file(self, file_path, name="", range_start=-1, range_end=-1):
        """
        Import a source file into the project.

        :param file_path: Path to the source
        :param name: Name of the source
        :param range_start: Range start frame
        :param range_end: Range end frame
        :param parent_id: Parent folder of the source
        :return: Dictionary representing the source object. None on error.
        """
        cmd = {
            "cmd": "import_file",
            "file_path": file_path,
            "name": name,
            "range_start": range_start,
            "range_end": range_end,
            "parent_id": ""
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["source"]
        else:
            return None

    def get_frame(self):
        """
        Get the current frame.

        :return: The current frame. Zero on error.
        """
        cmd = {
            "cmd": "get_frame"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["frame"]
        else:
            return 0

    def set_frame(self, frame, audio=False, from_range_start=False):
        """
        Set the current frame.

        :param frame: Requested frame number
        :param audio: Play audio for the frame after setting it.
        :param from_range_start: Frame number is relative to the range start.
        :return: The current frame. Zero on error.
        """
        cmd = {
            "cmd": "set_frame",
            "frame": frame,
            "audio": audio,
            "from_range_start": from_range_start
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["frame"]
        else:
            return 0

    def get_range(self):
        """
        Get the current range.

        :return: Tuple containing the range. None on error.
        """
        cmd = {
            "cmd": "get_range"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return (reply["start_frame"], reply["end_frame"])
        else:
            return None

    def set_range(self, start_frame, end_frame):
        """
        Set the current range.

        :param start_frame: Requested range start frame number.
        :param end_frame: Requested range end frame number.
        :return: Tuple containing the range. None on error.
        """
        cmd = {
            "cmd": "set_range",
            "start_frame": start_frame,
            "end_frame": end_frame
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return (reply["start_frame"], reply["end_frame"])
        else:
            return None

# if __name__ == "__main__":
#     MayaToKeyframeMP.display()
