import bpy
import bgl
import blf

bl_info = {
    "name": "Easy Grid Resizer",
    "author": "MehmetHY",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "3D View -> N Panel -> View -> Easy Grid Resizer",
    "description": "Set, add, subtruct, multiply or divide the grid size with a single click.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/MehmetHY/BlenderEasyGridResizer",
    "category": "3D View"
}


font_info = {"handler": None}


class GridProperties(bpy.types.PropertyGroup):
    set_grid_size: bpy.props.FloatProperty(name="Set Grid Size", default=1.0, min=0.0, description="Set Grid Size")
    add_subtruct_step: bpy.props.FloatProperty(name="Add/Subtruct Step", default=1.0, min=0.0, description="Add/Subtract Value")
    multiply_divide_step: bpy.props.FloatProperty(
        name="Multiply/Divide Step", default=2.0, min=1.0, description="Multply/Divide Value")
    overlay_active: bpy.props.BoolProperty(
        "Grid Size Overlay", default=False, description="Draw Overlay")
    overlay_font_size: bpy.props.IntProperty(
        "Overlay Size", default=24, description="Overlay Size", min=18, max=64)
    overlay_color: bpy.props.FloatVectorProperty("Overlay Color", subtype="COLOR", size=4, default=(
        1.0, 1.0, 1.0, 1.0), min=0.0, max=1.0, description="Overlay Color")
    overlay_direction: bpy.props.EnumProperty(
        items=[("Right", "Right", ""), ("Left", "Left", "")], name="overlay_direction", default="Left", description="Overlay Location")


class DrawGridSizeOverlay(bpy.types.Operator):
    bl_idname = "view3d.draw_grid_size_overlay"
    bl_label = "Draw Grid Size Overlay"
    bl_description = "Shows Grid Size Text"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.grid_property_group.overlay_active = not bpy.context.scene.grid_property_group.overlay_active
        if bpy.context.area .type == "VIEW_3D":
            if bpy.context.scene.grid_property_group.overlay_active:
                font_info["handler"] = bpy.types.SpaceView3D.draw_handler_add(draw_callback, (self, context), 'WINDOW', 'POST_PIXEL')
            else:
                bpy.types.SpaceView3D.draw_handler_remove(font_info["handler"], 'WINDOW')
        return {'FINISHED'}


def draw_callback(self, context):
    grid_size_text = f"Grid Size: {bpy.context.space_data.overlay.grid_scale}"
    overlay_width = len(grid_size_text) * bpy.context.scene.grid_property_group.overlay_font_size * 0.3
    overlay_offset = bpy.context.area.width - int(overlay_width) - 60
    if bpy.context.scene.grid_property_group.overlay_direction == "Right":
        blf.position(0, overlay_offset, 20, 0)
    else:
        blf.position(0, 20, 20, 0)
    blf.color(0, bpy.context.scene.grid_property_group.overlay_color[0],
              bpy.context.scene.grid_property_group.overlay_color[1], bpy.context.scene.grid_property_group.overlay_color[2], bpy.context.scene.grid_property_group.overlay_color[3])
    blf.size(0, bpy.context.scene.grid_property_group.overlay_font_size, bpy.context.preferences.system.dpi)
    blf.draw(0, f"Grid Size: {bpy.context.space_data.overlay.grid_scale}")


class SetGridScale(bpy.types.Operator):
    bl_idname = "view3d.set_grid_size"
    bl_label = "Set Grid Size"
    bl_description = "Set Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale = bpy.context.scene.grid_property_group.set_grid_size
        return {'FINISHED'}


class IncreaseGridScale(bpy.types.Operator):
    bl_idname = "view3d.increase_grid_size"
    bl_label = "Increase Grid Size"
    bl_description = "Increase Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale += bpy.context.scene.grid_property_group.add_subtruct_step
        return {'FINISHED'}


class DecreaseGridScale(bpy.types.Operator):
    bl_idname = "view3d.decrease_grid_size"
    bl_label = "Decrease Grid Size"
    bl_description = "Decrease Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale -= bpy.context.scene.grid_property_group.add_subtruct_step
        return {'FINISHED'}


class MultiplyGridScale(bpy.types.Operator):
    bl_idname = "view3d.multiply_grid_size"
    bl_label = "Multiply Grid Size"
    bl_description = "Multiply Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale *= bpy.context.scene.grid_property_group.multiply_divide_step
        return {'FINISHED'}


class DivideGridScale(bpy.types.Operator):
    bl_idname = "view3d.divide_grid_size"
    bl_label = "Divide Grid Size"
    bl_description = "Divide Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale /= bpy.context.scene.grid_property_group.multiply_divide_step
        return {'FINISHED'}


class GridPanel(bpy.types.Panel):
    bl_idname = "EASYGRIDSIZER_PT_grid_size"
    bl_label = "Easy Grid Resizer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"

    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def draw(self, context):
        prop_group = bpy.context.scene.grid_property_group
        layout = self.layout

        box = layout.box()
        box.label(text="Current Grid Size")
        row = box.row()
        box = row.box()
        box.label(text=str(bpy.context.space_data.overlay.grid_scale))
        box.operator("view3d.draw_grid_size_overlay", text="Show Text")
        box.prop(prop_group, "overlay_font_size", text="Text Size")
        box.prop(prop_group, "overlay_direction", text="Text Location")
        box.prop(prop_group, "overlay_color", text="Text Color")

        layout.row()
        box = layout.box()
        box.label(text="Set Grid Size")
        box.row()
        box.prop(prop_group, "set_grid_size")
        box.operator("view3d.set_grid_size")
        row = box.row()

        layout.row()
        box = layout.box()
        box.label(text="Add/Subtruct Grid Size")
        box.row()
        box.prop(prop_group, "add_subtruct_step")
        row = box.row()
        row.operator("view3d.decrease_grid_size", text="Subtract")
        row.operator("view3d.increase_grid_size", text="Add")

        layout.row()
        box = layout.box()
        box.label(text="Multiply/Divide Grid Size")
        box.row()
        box.prop(prop_group, "multiply_divide_step")
        row = box.row()
        row.operator("view3d.divide_grid_size", text="Divide")
        row.operator("view3d.multiply_grid_size", text="Multiply")


classes_to_register = (GridProperties, SetGridScale, IncreaseGridScale, DecreaseGridScale,
                       MultiplyGridScale, DivideGridScale, GridPanel, DrawGridSizeOverlay)

def register():
    for cls in classes_to_register:
        bpy.utils.register_class(cls)
    bpy.types.Scene.grid_property_group = bpy.props.PointerProperty(type=GridProperties)

def unregister():
    for cls in classes_to_register:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.grid_property_group


if __name__ == "__main__":
    register()
    
