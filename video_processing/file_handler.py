import os
import shutil
import tempfile

def handle_file_upload(uploaded_file):
    """
    Save the uploaded video file to a temporary directory.
    
    Args:
    uploaded_file: Uploaded file object from Streamlit.
    
    Returns:
    str: Path to the saved video file.
    """
    temp_dir = tempfile.mkdtemp() # create a temporary directory where the uploaded file will be saved
    video_path = os.path.join(temp_dir, uploaded_file.name) # constructs the file path using the temporary directory and the uploaded file's name
    
    with open(video_path, "wb") as f: # copy file
        shutil.copyfileobj(uploaded_file, f)
    
    return video_path