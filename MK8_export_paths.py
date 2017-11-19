import bpy
import mathutils
import math
import addon_add_object
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       AddonPreferences,
                       PropertyGroup,
                       )
 

class MySettings(PropertyGroup):

    my_bool = BoolProperty(
        name="Enable or Disable",
        description="A simple bool property",
        default = False) 


		
		
class CustomPanel(bpy.types.Panel):
    """A Custom Panel in the Viewport Toolbar"""
    bl_label = "LapPath"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

	
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
		

        layout.prop(mytool, "my_bool", text="Bool Property")


        if (mytool.my_bool == True):
            print ("Property Enabled")
        else:
            print ("Property Disabled")







def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
 
    f.write('  <EnemyPath type="array">')
 
    # Add Extra Code here for Multiple Paths. Lap path IDs will reset for these.
 
    # So now we will search for layers in the scene and group them!
 
    objects = sorted(bpy.context.scene.objects, key=lambda ob: ob.name)
 
    layerIndecies = []
 
    for layerIndex in range(20):  # loop from layer 0 to layer 19
        selectedObjects = [ob for ob in objects if ob.layers[layerIndex] and ob.select]
 
        if selectedObjects:
            layerIndecies.append(layerIndex)
 
    for groupIndex, layerIndex in enumerate(layerIndecies):  # loop from first group to last group
        selectedObjects = [ob for ob in objects if ob.layers[layerIndex] and ob.select]
 
        # Write the start of lap path group
        if layerIndex != layerIndecies[0]:
            f.write('    </value>')
        f.write('\n    <value UnitIdNum="38">')
        f.write('\n      <PathPt type="array">\n')
 
        for objID, obj in enumerate(selectedObjects):
            f.write('        <value BattleFlag="0" PathDir="0" Priority="1">\n')

 
            f.write('          <NextPt type="array">\n')
 
 
            # Write next lap path group ID
            f.write('            <value PathId="')  # write the next group ID
 
            if obj == selectedObjects[-1]:
                if layerIndex == layerIndecies[-1]:
                    f.write('0')
                else:
                    f.write('%d' % (groupIndex + 1))
            else:
                f.write('%d' % groupIndex)
 
            # Write next lap path ID
            f.write('" PtId="')
 
            if obj == selectedObjects[-1]:
                f.write('0" />')
            else:
                f.write('%d" />' % (objID + 1))
 
            f.write('\n          </NextPt>\n')
 
            # Write previous lap path group ID
            f.write('          <PrevPt type="array">\n')
            f.write('            <value PathId="')  # write the next group ID
 
            if obj == selectedObjects[0]:
                if layerIndex == layerIndecies[0]:
                    f.write('%d' %  (len(layerIndecies) - 1))
                else:
                    f.write('%d' % (groupIndex - 1))
            else:
                f.write('%d' % groupIndex)
 
            # Write previous lap path ID
            f.write('" PtId="')
 
            if obj == selectedObjects[0]:
                f.write('%d" />' %  (len(selectedObjects) - 1))
            else:
                f.write('%d" />' % (objID - 1))
 
            f.write('\n          </PrevPt>')
 

            XRot = round(obj.rotation_euler.x, 3)
            ZRot = round(obj.rotation_euler.z, 3)
            YRot = round(-obj.rotation_euler.y,
                         3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            xloc = round(obj.location.x, 3)
            yloc = round(-obj.location.y, 3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            zloc = round(obj.location.z, 3)
 
            # Write Coordinates from lap paths selected
            f.write('\n          <Rotate X="')
            f.write(str(XRot) + 'f" Y="' + str(ZRot) + 'f" Z="' + str(YRot) + 'f" />')
            f.write('\n          <Translate X="')
            f.write(str(xloc) + 'f" Y="' + str(zloc) + 'f" Z="' + str(yloc) + 'f" />')
            f.write('\n        </value>\n')
 
        f.write('      </PathPt>\n')
 

 
 
    f.write('    </value>\n')
    f.write('  </EnemyPath>\n')
 
    f.write('  <FirstCurve type="string">right</FirstCurve>\n')
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    f.write('  <LapPath type="array">')
 
    # Add Extra Code here for Multiple Paths. Lap path IDs will reset for these.
 
    # So now we will search for layers in the scene and group them!
 
    objects = sorted(bpy.context.scene.objects, key=lambda ob: ob.name)
 
    layerIndecies = []
 
    for layerIndex in range(20):  # loop from layer 0 to layer 19
        selectedObjects = [ob for ob in objects if ob.layers[layerIndex] and ob.select]
 
        if selectedObjects:
            layerIndecies.append(layerIndex)
 
    for groupIndex, layerIndex in enumerate(layerIndecies):  # loop from first group to last group
        selectedObjects = [ob for ob in objects if ob.layers[layerIndex] and ob.select]
 
        # Write the start of lap path group
        if layerIndex != layerIndecies[0]:
            f.write('    </value>')
			
			
        if "gravity" in obj.name.lower():
            f.write('\n    <value LapPathGroup="-1" ReturnPointsError="false" UnitIdNum="62">')
            f.write('\n      <LapPath_GravityPath type="array">')
            f.write('\n        <value>0</value>')
            f.write('\n        <value>2</value>')
            f.write('\n      </LapPath_GravityPath>')
            f.write('\n      <PathPt type="array">\n')

        else:
            f.write('\n    <value LapPathGroup="-1" ReturnPointsError="false" UnitIdNum="1">')
            f.write('\n      <PathPt type="array">\n')
 
 
        headlights = "false"
 
        for objID, obj in enumerate(selectedObjects):
            if obj == selectedObjects[0]:
                if layerIndex == layerIndecies[0]:
                  f.write('        <value CheckPoint="-1" ClipIdx="-1" HeadLightSW="' + str(headlights) + '" LapCheck="0" MapCameraFovy="65" MapCameraY="320" ReturnPosition="-1" SoundSW="-1">')
                else:
                  f.write('        <value CheckPoint="-1" ClipIdx="-1" HeadLightSW="' + str(headlights) + '" LapCheck="-1" MapCameraFovy="65" MapCameraY="320" ReturnPosition="-1" SoundSW="-1">')
            else:
                  f.write('        <value CheckPoint="-1" ClipIdx="-1" HeadLightSW="' + str(headlights) + '" LapCheck="-1" MapCameraFovy="65" MapCameraY="320" ReturnPosition="-1" SoundSW="-1">')
 
            f.write('\n          <NextPt type="array">\n')
 
 
            # Write next lap path group ID
            f.write('            <value PathId="')  # write the next group ID
 
            if obj == selectedObjects[-1]:
                if layerIndex == layerIndecies[-1]:
                    f.write('0')
                else:
                    f.write('%d' % (groupIndex + 1))
            else:
                f.write('%d' % groupIndex)
 
            # Write next lap path ID
            f.write('" PtId="')
 
            if obj == selectedObjects[-1]:
                f.write('0" />')
            else:
                f.write('%d" />' % (objID + 1))
 
            f.write('\n          </NextPt>\n')
 
            # Write previous lap path group ID
            f.write('          <PrevPt type="array">\n')
            f.write('            <value PathId="')  # write the next group ID
 
            if obj == selectedObjects[0]:
                if layerIndex == layerIndecies[0]:
                    f.write('%d' %  (len(layerIndecies) - 1))
                else:
                    f.write('%d' % (groupIndex - 1))
            else:
                f.write('%d' % groupIndex)
 
            # Write previous lap path ID
            f.write('" PtId="')
 
            if obj == selectedObjects[0]:
                f.write('%d" />' %  (len(selectedObjects) - 1))
            else:
                f.write('%d" />' % (objID - 1))
 
            f.write('\n          </PrevPt>')
            #Scale paths as they are smaller for some reason
            if obj.type != 'EMPTY': 
                 ScaleX = obj.scale.x * 2
                 ScaleY = obj.scale.y * 2
                 ScaleZ = obj.scale.z * 2
            else:
                ScaleX = obj.scale.x
                ScaleY = obj.scale.y
                ScaleZ = obj.scale.z
				
			
            zscale = round(ScaleZ, 3)
            yscale = round(ScaleY, 3)
            xscale = round(ScaleX, 3)
            XRot = round(obj.rotation_euler.x, 3)
            ZRot = round(obj.rotation_euler.z, 3)
            YRot = round(-obj.rotation_euler.y,
                             3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            xloc = round(obj.location.x, 3)
            yloc = round(-obj.location.y, 3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            zloc = round(obj.location.z, 3)
 
 
            # Write Coordinates from lap paths selected
            f.write('\n          <Rotate X="')
            f.write(str(XRot) + 'f" Y="' + str(ZRot) + 'f" Z="' + str(YRot) + 'f" />')
            f.write('\n          <Scale X="')
            f.write(str(xscale) + 'f" Y="' + str(zscale) + 'f" Z="0.0f" />')		
            f.write('\n          <Translate X="')
            f.write(str(xloc) + 'f" Y="' + str(zloc) + 'f" Z="' + str(yloc) + 'f" />')
            f.write('\n        </value>\n')

        f.write('      </PathPt>\n')
        f.write('      <ReturnPoints type="array">\n')
 
        for obj in selectedObjects:
		
		
            mat_rot = obj.rotation_euler.to_matrix() #matricies will write based on euler rotation!

            mat = mat_rot.to_4x4() #Lets turn this into a grid!
            
			#These are for tangents
            matXR = mat[1][0] #Write second row, first column
            matYR = mat[1][1] #Write second row, second column
            matZR = mat[1][2] #Write second row, third column
		
            matX = round(matXR, 3)
            matY = round(matYR, 3)
            matZ = round(matZR, 3)

            #These are for normals
			
            matXRN = mat[2][0] #Write second row, first column
            matYRN = mat[2][1] #Write second row, second column
            matZRN = mat[2][2] #Write second row, third column
		
            matXN = round(matXRN, 3)
            matYN = round(matYRN, 3)
            matZN = round(matZRN, 3)
            f.write('        <value JugemIndex="-1" JugemPath="-1" ReturnType="-1" hasError="0">')
 
            xloc = round(obj.location.x, 3)
            yloc = round(-obj.location.y, 3)
            zloc = round(obj.location.z, 3)
 
            # Write Coordinates from lap paths selected
            f.write('\n          <Normal X="' + str(matXN) + 'f" Y="' + str(matZN) + 'f" Z="' + str(matYN) + 'f" />')
            f.write('\n          <Position X="')
            f.write(str(xloc) + 'f" Y="' + str(zloc) + 'f" Z="' + str(yloc) + 'f" />')
            f.write('\n          <Tangent X="' + str(matX) + 'f" Y="' + str(matZ) + 'f" Z="' + str(matY) + 'f" />')
            f.write('\n        </value>\n')
 
        f.write('      </ReturnPoints>\n')
 
    f.write('    </value>\n')
    f.write('  </LapPath>')
	
	
	
    objects = sorted(bpy.context.scene.objects, key=lambda ob: ob.name)

	
    objactive = context.scene.objects.active
	
	
	
    


    
 
    # Add Extra Code here for Multiple Paths. Lap path IDs will reset for these.
 
    # So now we will search for layers in the scene and group them!
 
    objects = sorted(bpy.context.scene.objects, key=lambda ob: ob.name)
 
    layerIndecies = []
 
    for layerIndex in range(20):  # loop from layer 0 to layer 19
        selectedObjectsGravity  = [ob for ob in objects if ob.layers[layerIndex] and  "gravity" in ob.name.lower() and ob.select]
 
        if selectedObjectsGravity:
            layerIndecies.append(layerIndex)
        

 
 
    for groupIndex, layerIndex in enumerate(layerIndecies):  # loop from first group to last group
        selectedObjectsGravity  = [ob for ob in objects if ob.layers[layerIndex] and  "gravity" in ob.name.lower() and ob.select]
 
        # Write the start of lap path group
		
        if layerIndex == layerIndecies[0]:
            f.write('\n  <GravityPath type="array">')


        if layerIndex != layerIndecies[0]:
            f.write('    </value>')
                    
			
			
			
        f.write('\n    <value UnitIdNum="70">')
        f.write('\n      <PathPt type="array">\n')
 
        for objID, obj in enumerate(selectedObjectsGravity ):
            f.write('        <value CameraHeight="1" GlideOnly="false" Transform="true">\n')

            if obj == selectedObjectsGravity [-1]:
                    f.write('          <NextPt type="array" />\n')
            else:
                    f.write('          <NextPt type="array">\n')

 
            # Write next lap path group ID
            if obj == selectedObjectsGravity [-1]:
                    f.write('')  # Last Object does not loop so has no ID after
            else:
                    f.write('            <value PathId="')  # write the next group ID
				
            if obj == selectedObjectsGravity [-1]:
                if layerIndex == layerIndecies[-1]:
                    f.write('')
                else:
                    f.write('%d' % (groupIndex + 1))
            else:
                f.write('%d' % groupIndex)
 
            if obj == selectedObjectsGravity [-1]:
                    f.write('')
					
            # Write next lap path ID
            if obj == selectedObjectsGravity [-1]:
                f.write('')  # Last Object does not loop so has no ID after
            else:
                f.write('" PtId="')
 
            if obj == selectedObjectsGravity [-1]:
                f.write('')
            else:
                f.write('%d" />' % (objID + 1))
 
            if obj == selectedObjectsGravity [-1]:
                f.write('')  # Last Object does not loop so has no ID after
            else:
                f.write('\n          </NextPt>\n')
 
            # Write previous lap path group ID
            if obj == selectedObjectsGravity [0]:
                    f.write('          <PrevPt type="array" />')
            else:
                    f.write('          <PrevPt type="array">')
			
            if obj == selectedObjectsGravity [0]:
                f.write('')  # Last Object does not loop so has no ID before
            else:
                f.write('\n            <value PathId="')  # write the next group ID
 
            if obj == selectedObjectsGravity [0]:
                    f.write('')
            else:
                f.write('%d' % groupIndex)
 
            # Write previous lap path ID
            if obj == selectedObjectsGravity [0]:
                f.write('')  # Last Object does not loop so has no ID before
            else:
                f.write('" PtId="')
 
            if obj == selectedObjectsGravity [0]:
                f.write('')
            else:
                f.write('%d" />' % (objID - 1))
				
				
            if obj == selectedObjectsGravity [0]:
                f.write('')  # Last Object does not loop so has no ID before
            else:
                 f.write('\n          </PrevPt>')
 
            zscale = round(obj.scale.z, 3)
            yscale = round(obj.scale.y, 3)
            xscale = round(obj.scale.x, 3)
            XRot = round(obj.rotation_euler.x, 3)
            ZRot = round(obj.rotation_euler.z, 3)
            YRot = round(-obj.rotation_euler.y,
                         3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            xloc = round(obj.location.x, 3)
            yloc = round(-obj.location.y, 3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            zloc = round(obj.location.z, 3)
 
            # Write Coordinates from lap paths selected
            f.write('\n          <Rotate X="')
            f.write(str(XRot) + 'f" Y="' + str(ZRot) + 'f" Z="' + str(YRot) + 'f" />')
            f.write('\n          <Scale X="')
            f.write(str(xscale) + 'f" Y="' + str(zscale) + 'f" Z="0.0f" />')
            f.write('\n          <Translate X="')
            f.write(str(xloc) + 'f" Y="' + str(zloc) + 'f" Z="' + str(yloc) + 'f" />')
            f.write('\n        </value>\n')
 
        f.write('      </PathPt>\n')
 
        if layerIndex != layerIndecies[0]:
            f.write('')
        else:
            f.write('    </value>\n')
            f.write('  </GravityPath>')
	
	
	
	
	
	
	
	
	
	
	
	
    
	
	
	
	
	
	
	
	
	
 
    # Add Extra Code here for Multiple Paths. Lap path IDs will reset for these.
 
    # So now we will search for layers in the scene and group them!
 
    objects = sorted(bpy.context.scene.objects, key=lambda ob: ob.name)
 
    layerIndecies = []
 
    for layerIndex in range(20):  # loop from layer 0 to layer 19
        selectedObjectsGlider  = [ob for ob in objects if ob.layers[layerIndex] and  "glide" in ob.name.lower() and ob.select]
 
        if selectedObjectsGlider:
            layerIndecies.append(layerIndex)
 
    for groupIndex, layerIndex in enumerate(layerIndecies):  # loop from first group to last group
        selectedObjectsGlider  = [ob for ob in objects if ob.layers[layerIndex] and  "glide" in ob.name.lower() and ob.select]
 
        # Write the start of lap path group
        if layerIndex == layerIndecies[0]:
            f.write('\n  <GlidePath type="array">')
		
        if layerIndex != layerIndecies[0]:
            f.write('    </value>')
			
			
        f.write('\n    <value GlideType="1" IsUp="true" UnitIdNum="0">')
        f.write('\n      <PathPt type="array">\n')
 
        for objID, obj in enumerate(selectedObjectsGlider ):
            f.write('        <value Cannon="true">\n')

            if obj == selectedObjectsGlider [-1]:
                    f.write('          <NextPt type="array" />\n')
            else:
                    f.write('          <NextPt type="array">\n')

 
            # Write next lap path group ID
            if obj == selectedObjectsGlider [-1]:
                    f.write('')  # Last Object does not loop so has no ID after
            else:
                    f.write('            <value PathId="')  # write the next group ID
				
            if obj == selectedObjectsGlider [-1]:
                if layerIndex == layerIndecies[-1]:
                    f.write('')
                else:
                    f.write('%d' % (groupIndex + 1))
            else:
                f.write('%d' % groupIndex)
 
            if obj == selectedObjectsGlider [-1]:
                    f.write('')
					
            # Write next lap path ID
            if obj == selectedObjectsGlider [-1]:
                f.write('')  # Last Object does not loop so has no ID after
            else:
                f.write('" PtId="')
 
            if obj == selectedObjectsGlider [-1]:
                f.write('')
            else:
                f.write('%d" />' % (objID + 1))
 
            if obj == selectedObjectsGlider [-1]:
                f.write('')  # Last Object does not loop so has no ID after
            else:
                f.write('\n          </NextPt>\n')
 
            # Write previous lap path group ID
            if obj == selectedObjectsGlider [0]:
                    f.write('          <PrevPt type="array" />')
            else:
                    f.write('          <PrevPt type="array">')
			
            if obj == selectedObjectsGlider [0]:
                f.write('')  # Last Object does not loop so has no ID before
            else:
                f.write('\n            <value PathId="')  # write the next group ID
 
            if obj == selectedObjectsGlider [0]:
                    f.write('')
            else:
                f.write('%d' % groupIndex)
 
            # Write previous lap path ID
            if obj == selectedObjectsGlider [0]:
                f.write('')  # Last Object does not loop so has no ID before
            else:
                f.write('" PtId="')
 
            if obj == selectedObjectsGlider [0]:
                f.write('')
            else:
                f.write('%d" />' % (objID - 1))
				
				
            if obj == selectedObjectsGlider [0]:
                f.write('')  # Last Object does not loop so has no ID before
            else:
                 f.write('\n          </PrevPt>')
 
            zscale = round(obj.scale.z, 3)
            yscale = round(obj.scale.y, 3)
            xscale = round(obj.scale.x, 3)
            XRot = round(obj.rotation_euler.x, 3)
            ZRot = round(obj.rotation_euler.z, 3)
            YRot = round(-obj.rotation_euler.y,
                         3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            xloc = round(obj.location.x, 3)
            yloc = round(-obj.location.y, 3)  # Invert the dumb Y coords so positive is negitive, negitive is positive
            zloc = round(obj.location.z, 3)
 
            # Write Coordinates from lap paths selected
            f.write('\n          <Rotate X="')
            f.write(str(XRot) + 'f" Y="' + str(ZRot) + 'f" Z="' + str(YRot) + 'f" />')
            f.write('\n          <Scale X="')
            f.write(str(xscale) + 'f" Y="' + str(zscale) + 'f" Z="0.0f" />')
            f.write('\n          <Translate X="')
            f.write(str(xloc) + 'f" Y="' + str(zloc) + 'f" Z="' + str(yloc) + 'f" />')
            f.write('\n        </value>\n')
 
        f.write('      </PathPt>\n')
 
 
        if layerIndex != layerIndecies[0]:
            f.write('')
        else:
            f.write('    </value>\n')
            f.write('  </GlidePath>')
	
	
	
    f.close()
 
    return {'FINISHED'}
 
 
# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
 
 
class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"
 
    # ExportHelper mixin class uses this
    filename_ext = "course_muunt_PATHS.xml"
 
    filter_glob = StringProperty(
        default=".xml",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
 
    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )
 
    type = EnumProperty(
        name="Mario Kart 8 XML Path Exporter",
        description="Choose between two items",
        items=(('OPT_A', "First Option", "Description one"),
               ('OPT_B', "Second Option", "Description two")),
        default='OPT_A',
    )
 
    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)
 
 
# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="Mario Kart 8 XML Path Exporter")
 
 
def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.append(menu_func_export)
 
 
def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
 
 
if __name__ == "__main__":
    register()
 
    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')