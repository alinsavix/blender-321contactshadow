import os
import sys
from typing import *

import bpy

bl_info = {
    "name": "3-2-1 Contact(Shadow)",
    "author": "TDV Alinsa",
    "description": "",
    "blender": (2, 91, 0),
    "version": (0, 0, 0),   # autoreplace
    "location": "keybinds > ttocs.set_contact_shadows or ttocs.force_set_contact_shadows",
    "warning": "",
    "category": "Mesh"
}


class TTOContactShadowInfo(bpy.types.PropertyGroup):
    shadowed: bpy.props.BoolProperty(  # type: ignore
        name="Contacct Shadowed",
        description="Object processed by TTOContactShadow",
        default=False,
        options={'HIDDEN'},
    )


class TTOCS_OT_SetContactShadows(bpy.types.Operator):
    bl_idname = "ttocs.set_contact_shadows"
    bl_label = "Set contact shadows on all untouched lights"
    bl_options = {'UNDO'}

    def execute(self, context):
        for light in bpy.data.lights:
            if not light.use_contact_shadow and not light.TTOCS.shadowed:
                print(f"Setting contact shadow for light {light.name} ({light.type})")
                light.use_contact_shadow = True
                light.TTOCS.shadowed = True

        return {'FINISHED'}


class TTOCS_OT_ForceSetContactShadows(bpy.types.Operator):
    bl_idname = "ttocs.force_set_contact_shadows"
    bl_label = "Force set contact shadows on all untouched lights"
    bl_options = {'UNDO'}

    def execute(self, context):
        for light in bpy.data.lights:
            if not light.use_contact_shadow:
                print(f"Force-setting contact shadow for light {light.name} ({light.type})")
                light.use_contact_shadow = True
                light.TTOCS.shadowed = True

        return {'FINISHED'}


def register():
    bpy.utils.register_class(TTOCS_OT_SetContactShadows)
    bpy.utils.register_class(TTOCS_OT_ForceSetContactShadows)
    bpy.utils.register_class(TTOContactShadowInfo)
    bpy.types.Light.TTOCS = bpy.props.PointerProperty(type=TTOContactShadowInfo)

    print("registered")


def unregister():
    del bpy.types.Light.TTOCS
    bpy.utils.unregister_class(TTOContactShadowInfo)
    bpy.utils.unregister_class(TTOCS_OT_ForceSetContactShadows)
    bpy.utils.unregister_class(TTOCS_OT_SetContactShadows)

    print("unregistered")



# contact shadow paths:
# bpy.data.lights["Sun"].use_shadow
# bpy.data.lights["Point"].use_contact_shadow
# bpy.data.lights["Sun"].use_contact_shadow
# bpy.data.lights["Spot"].use_contact_shadow
# bpy.data.lights["Area"].use_contact_shadow
#
# types:
# bpy.types.PointLight
# bpy.types.SpotLight
# bpy.types.SpotLight
# bpy.types.AreaLight
