import bpy

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

class GridProperties(bpy.types.PropertyGroup):
    set_grid_size: bpy.props.FloatProperty(name="Set Grid Size", default=1.0, min=0.0)
    add_subtruct_step: bpy.props.FloatProperty(name = "Add/Subtruct Step", default = 1.0, min = 0.0)
    multiply_divide_step: bpy.props.FloatProperty(name = "Multiply/Divide Step", default = 2.0, min = 1.0)

class SetGridScale(bpy.types.Operator):
    bl_idname = "view3d.set_grid_size"
    bl_label = "Set Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale = bpy.data.objects[0].grid_property_group.set_grid_size
        return {'FINISHED'}

class IncreaseGridScale(bpy.types.Operator):
    bl_idname = "view3d.increase_grid_size"
    bl_label = "Increase Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale += bpy.data.objects[0].grid_property_group.add_subtruct_step
        return {'FINISHED'}

class DecreaseGridScale(bpy.types.Operator):
    bl_idname = "view3d.decrease_grid_size"
    bl_label = "Decrease Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale -= bpy.data.objects[0].grid_property_group.add_subtruct_step
        return {'FINISHED'}

class MultiplyGridScale(bpy.types.Operator):
    bl_idname = "view3d.multiply_grid_size"
    bl_label = "Multiply Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale *= bpy.data.objects[0].grid_property_group.multiply_divide_step
        return {'FINISHED'}

class DivideGridScale(bpy.types.Operator):
    bl_idname = "view3d.divide_grid_size"
    bl_label = "Divide Grid Size"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.space_data.overlay.grid_scale /= bpy.data.objects[0].grid_property_group.multiply_divide_step
        return {'FINISHED'}

class GridPanel(bpy.types.Panel):
    bl_idname = "EASYGRIDSIZER_PT_grid_size"
    bl_label = "Easy Grid Resizer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text = "Current Grid Size")
        row = box.row()
        box = row.box()
        current_grid_label = box.label(text = str(bpy.context.space_data.overlay.grid_scale))

        layout.row()
        box = layout.box()
        box.label(text = "Set Grid Size")
        box.row()
        prop_group = bpy.data.objects[0].grid_property_group
        box.prop(prop_group, "set_grid_size")
        box.operator("view3d.set_grid_size")
        row = box.row()

        layout.row()
        box = layout.box()
        box.label(text="Add/Subtruct Grid Size")
        box.row()
        box.prop(prop_group, "add_subtruct_step")
        row = box.row()
        row.operator("view3d.decrease_grid_size")
        row.operator("view3d.increase_grid_size")

        layout.row()
        box = layout.box()
        box.label(text="Multiply/Divide Grid Size")
        box.row()
        box.prop(prop_group, "multiply_divide_step")
        row = box.row()
        row.operator("view3d.divide_grid_size")
        row.operator("view3d.multiply_grid_size")
    
def register():
    bpy.utils.register_class(GridProperties)
    bpy.types.Object.grid_property_group = bpy.props.PointerProperty(type = GridProperties)
    bpy.utils.register_class(SetGridScale)
    bpy.utils.register_class(IncreaseGridScale)
    bpy.utils.register_class(DecreaseGridScale)
    bpy.utils.register_class(MultiplyGridScale)
    bpy.utils.register_class(DivideGridScale)
    bpy.utils.register_class(GridPanel)

def unregister():
    bpy.utils.unregister_class()(GridProperties)
    del bpy.types.Object.grid_property_group
    bpy.utils.unregister_class()(SetGridScale)
    bpy.utils.unregister_class()(IncreaseGridScale)
    bpy.utils.unregister_class()(DecreaseGridScale)
    bpy.utils.unregister_class()(MultiplyGridScale)
    bpy.utils.unregister_class()(DivideGridScale)
    bpy.utils.unregister_class(GridPanel)

if __name__ == "__main__":
    register()