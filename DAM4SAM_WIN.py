import subprocess
import threading
import nuke
import os
import re

# Get the current Nuke node
ref_node = nuke.thisNode()

# Get the input and output paths from the node parameters
image_dir = ref_node['input'].getValue()
output_path = ref_node['output'].getValue()
output_path_new = output_path + "/%04d.png"


def extract_frame_number(filename):
    """Extracts frame number from a filename. Modify based on your naming convention."""
    import re
    match = re.search(r'(\d+)(?=\.\w+$)', filename)
    return int(match.group(0)) if match else None

def create_read(output_path_new):
    output_dir = os.path.dirname(output_path_new)
    file_extension = os.path.splitext(output_path_new)[-1]

    frames = [f for f in sorted(os.listdir(output_dir)) if f.endswith(file_extension)]
    if not frames:
        nuke.message(f"No frames with extension {file_extension} found in the output directory.")
        return False

    first_frame_number = extract_frame_number(frames[0])
    last_frame_number = extract_frame_number(frames[-1])

    if first_frame_number is None or last_frame_number is None:
        nuke.message("Could not extract frame numbers from filenames.")
        return False

    read_node = nuke.createNode("Read")
    read_node["file"].setValue(output_path_new)
    read_node["first"].setValue(first_frame_number)
    read_node["last"].setValue(last_frame_number)
    read_node["reload"].execute()

    # Position the Read node 50px below ref_node
    x_pos = ref_node.xpos()
    y_pos = ref_node.ypos() + 150
    read_node.setXYpos(x_pos, y_pos)

    # Create a Shuffle node connected to the Read node
    shuffle_node = nuke.createNode("Shuffle")

    # Connect the Shuffle node to the Read node
    shuffle_node.setInput(0, read_node)

    # Set the Shuffle node to copy Red to all RGBA channels
    shuffle_node["in"].setValue("red")  # Set input to red
    shuffle_node["red"].setValue("red")
    shuffle_node["green"].setValue("red")
    shuffle_node["blue"].setValue("red")
    shuffle_node["alpha"].setValue("red")

    # Position the Shuffle node 50px below the Read node
    shuffle_node.setXYpos(x_pos, y_pos + 150)

    # Find the existing Viewer node
    viewer_nodes = [n for n in nuke.allNodes("Viewer")]
    
    if viewer_nodes:
        viewer_node = viewer_nodes[0]  # Use the first found Viewer node
        viewer_node.setInput(0, shuffle_node)  # Connect the Viewer to the Shuffle node
    else:
        nuke.message("No existing Viewer node found in the script.")

    return True


# Define paths
batch_script = r'C:/Users/WORKSTATION/temp_script.bat'
conda_activate = r'C:/Users/%USERNAME%/miniconda3/Scripts/activate.bat'
conda_env = "DAM4SAM"  # Your Conda environment name
script_dir = r'C:/Users/WORKSTATION/.nuke/DAM4SAM'
test_dir = image_dir
output_dir = output_path
imformat = r'png'

# Create the batch script
with open(batch_script, 'w') as f:
    f.write(f'@echo off\n')
    f.write(f'call "{conda_activate}"\n')  # Activate Conda
    f.write(f'call conda activate {conda_env}\n')  # Activate DAM4SAM environment
    f.write(f'cd "{script_dir}"\n')
    f.write(f'python run_bbox_example.py --dir "{test_dir}" --ext "{imformat}" --output_dir "{output_dir}"\n')
    f.write(f'exit\n')  # Automatically closes the process when done

# Function to run the script
def run_script():
    process = subprocess.Popen(batch_script, creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()  # Wait for script to finish

# Run the script in a thread
script_thread = threading.Thread(target=run_script)
script_thread.start()
script_thread.join()  # Wait for thread to finish

# Now that the thread is finished, create the Read node on the main thread
create_read(output_path_new)
