import bpy
import csv
import random
import math

# Constants
SCALE_FACTOR = 33.3  # Scale factor for node positions
ARC_HEIGHT = 15.0    # Height of the arc for "over" paths
OFFSET = 2.0         # Offset for 90 degree turns
BORDER_OFFSET = 4.0     # Offset for 90 degree turns on border
SEGMENT_SIZE = 10000   # Number of edges per segment
MAX_NODE_DIM = 23 # max width & height index of graph

def delete_existing_paths():
    # Delete existing path segments
    for obj in bpy.context.scene.objects:
        if obj.name.startswith("PathCurveSegment"):
            bpy.data.objects.remove(obj, do_unlink=True)

def import_path_data(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        path_data = list(reader)
    return path_data

def create_nurbs_curve_segment(curve_data, segment_data):
    # Create a new spline in the curve
    spline = curve_data.splines.new('NURBS')
    
    # Initialize node_state dictionary
    node_state = {}

    for i, (start_node, end_node) in enumerate(segment_data):
        node_start_x, node_start_y = map(int, start_node.split(','))
        node_end_x, node_end_y = map(int, end_node.split(','))

        next_end_node = segment_data[i + 1][1] if i + 1 < len(segment_data) else None
        if next_end_node:
            next_node_end_x, next_node_end_y = map(int, next_end_node.split(','))
        else:
            next_node_end_x, next_node_end_y = -1, -1

        # Scale coordinates
        start_x, start_y = node_start_x * SCALE_FACTOR, node_start_y * SCALE_FACTOR
        end_x, end_y = node_end_x * SCALE_FACTOR, node_end_y * SCALE_FACTOR
        next_end_x, next_end_y = next_node_end_x * SCALE_FACTOR, next_node_end_y * SCALE_FACTOR

        if i == 0:
            spline.points.add(1)
            spline.points[0].co = (start_x, start_y, 0, 1)
            spline.points[0].tilt = 0
            node_key = (start_x, start_y)
            node_state[node_key] = {'horizontal': 'over', 'vertical': 'under'}

        midpoint = ((start_x + end_x) / 2, (start_y + end_y) / 2, 0)
        spline.points.add(1)
        spline.points[-1].co = (*midpoint, 1)
        spline.points[-1].tilt = 0

        if start_x == next_end_x or start_y == next_end_y:  # Straight path
            node_key = (end_x, end_y)
            
            if node_key not in node_state:
                node_state[node_key] = {'horizontal': None, 'vertical': None}
            
            if start_x == next_end_x:  # Vertical path
                if node_state[node_key]['vertical'] is None:
                    node_state[node_key]['vertical'] = random.choice(['over', 'under'])
                path_type = node_state[node_key]['vertical']
            else:  # Horizontal path
                if node_state[node_key]['horizontal'] is None:
                    node_state[node_key]['horizontal'] = random.choice(['over', 'under'])
                path_type = node_state[node_key]['horizontal']
            
            # Ensure one over and one under path at each node
            if path_type == 'over':
                node_state[node_key]['horizontal'] = 'under'
                node_state[node_key]['vertical'] = 'under'
            else:
                node_state[node_key]['horizontal'] = 'over'
                node_state[node_key]['vertical'] = 'over'
            
            # Add points to the spline based on path type
            if path_type == 'over':
                spline.points.add(1)
                spline.points[-1].co = (end_x, end_y, ARC_HEIGHT, 1)
                spline.points[-1].tilt = 0
            else:  # Under path (straight line)
                spline.points.add(1)
                spline.points[-1].co = (end_x, end_y, 0, 1)
                spline.points[-1].tilt = 0
        else:  # 90 degree turn
            # Calculate offset direction for the arc
            if node_end_x == 0 or node_end_x == MAX_NODE_DIM or node_end_y == 0 or node_end_y == MAX_NODE_DIM:
                turn_offset = BORDER_OFFSET
            else:
                turn_offset = OFFSET
            direction = (math.copysign(turn_offset, (start_x - end_x)+(next_end_x - end_x)), math.copysign(turn_offset, (start_y - end_y)+(next_end_y - end_y)), 0)
            offset_x, offset_y = (end_x + direction[0], end_y + direction[1])
            spline.points.add(1)
            spline.points[-1].co = (offset_x, offset_y, 0, 1)
            #spline.points[-1].co = (end_x, end_y, 0, 1)
            spline.points[-1].tilt = 0

    spline.use_endpoint_u = True
    spline.use_cyclic_u = True
    spline.order_u = 4
    
def create_nurbs_curve(path_data):
    num_segments = (len(path_data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
    
    for segment_index in range(num_segments):
        segment_start = segment_index * SEGMENT_SIZE
        segment_end = min(segment_start + SEGMENT_SIZE, len(path_data))
        segment_data = path_data[segment_start:segment_end]
        
        # Create a new curve object for each segment
        curve_data = bpy.data.curves.new(name=f'PathCurveSegment{segment_index}', type='CURVE')
        curve_data.dimensions = '3D'
        
        create_nurbs_curve_segment(curve_data, segment_data)
        
        # Create a new object with the curve data
        curve_obj = bpy.data.objects.new(f'PathCurveSegment{segment_index}', curve_data)
        bpy.context.collection.objects.link(curve_obj)

# Delete existing paths
delete_existing_paths()

# Path to the CSV file (use raw string notation to handle backslashes)
filepath = r'C:\Users\micha\OneDrive\Repos\SnakeEulerianPath\path_data.csv'

# Import path data and create NURBS curve
path_data = import_path_data(filepath)
create_nurbs_curve(path_data)