<p align="center">
  <strong>Windows</strong><br><br>
  <a href="https://www.youtube.com/watch?v=_9cLWZtqm7k" target="_blank">
    <img src="https://img.youtube.com/vi/_9cLWZtqm7k/0.jpg" alt="WINDOWS">
  </a>
</p>
> To open the video in a new tab, right-click the thumbnail and select "Open link in new tab."
---
### 🔧 Important Configuration Changes

For proper functioning, update **lines 79 to 81** in your script with the correct paths:

```python
conda_activate = r'C:/Users/%USERNAME%/miniconda3/Scripts/activate.bat'  # Your Conda directory
conda_env = "DAM4SAM"  # Your Conda environment name
script_dir = r'C:/Users/WORKSTATION/.nuke/DAM4SAM'  # Directory where the run_bbox_example.py script is located
