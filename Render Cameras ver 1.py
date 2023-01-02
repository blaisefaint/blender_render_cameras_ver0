bl_info = {
    "name": "Render Cameras ver 1",
    "blender": (3, 4, 1),
    "category": "Render",
}

import bpy

class RenderCamerasOperator(bpy.types.Operator):
    """Renders the animation for each camera in the scene"""
    bl_idname = "render.render_cameras"
    bl_label = "Render Cameras"

    def execute(self, context):
        # Get the current settings
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end
        file_format = bpy.context.scene.render.image_settings.file_format
        encoding_container = bpy.context.scene.render.ffmpeg.format
        video_codec = bpy.context.scene.render.ffmpeg.codec
        color_depth = bpy.context.scene.render.image_settings.color_mode
        output_dir = bpy.context.scene.render.filepath

        # Get the file name
        file_name = bpy.path.basename(bpy.context.blend_data.filepath)
               
        # Find the first object with an action
        first_object = None
        for obj in bpy.data.objects:
            if obj.animation_data is not None and obj.animation_data.action is not None:
                first_object = obj
                break  # No need to keep searching, so we can exit the loop

        # Get the action name
        action_name = first_object.animation_data.action.name if first_object else ""
  
        # Save the first camera to use later
        first_camera = None

        # Render each camera in the scene
        for camera_obj in bpy.data.objects:
            if camera_obj.type == 'CAMERA':
                # Save the first camera
                if first_camera is None:
                    first_camera = camera_obj
                # Set the active camera
                bpy.context.scene.camera = camera_obj
                # Set the output file name
                bpy.context.scene.render.filepath = f"{output_dir}{action_name} {file_name} {camera_obj.name} "
                # Set the frame range
                bpy.context.scene.frame_start = frame_start
                bpy.context.scene.frame_end = frame_end
                # Set the other rendering options
                bpy.context.scene.render.image_settings.file_format = file_format
                bpy.context.scene.render.ffmpeg.format = encoding_container
                bpy.context.scene.render.ffmpeg.codec = video_codec
                bpy.context.scene.render.image_settings.color_mode = color_depth
                # Render the scene and save the output
                bpy.ops.render.render(animation=True, write_still=True)

        # Set the active camera to the first camera
        bpy.context.scene.camera = first_camera
        
        # Reset the output file path
        bpy.context.scene.render.filepath = output_dir

        return {'FINISHED'}

class RenderCamerasPanel(bpy.types.Panel):
    """Creates a panel with a button to render the animation for each camera in the scene"""
    bl_label = "Render Cameras"
    bl_idname = "RENDER_PT_render_cameras"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        layout.operator(RenderCamerasOperator.bl_idname)

def register():
    bpy.utils.register_class(RenderCamerasOperator)
    bpy.utils.register_class(RenderCamerasPanel)
    bpy.types.RENDER_PT_output.append(RenderCamerasPanel)

def unregister():
    bpy.types.RENDER_PT_render.remove(RenderCamerasPanel)
    bpy.utils.unregister_class(RenderCamerasPanel)
    bpy.utils.unregister_class(RenderCamerasOperator)

if __name__ == "__main__":
    register()