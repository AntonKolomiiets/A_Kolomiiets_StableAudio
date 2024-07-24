import zipfile

def create_zip(clips):
    """
    Create zip file with clips for dowload
    """
    zip_path = "clips.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for clip in clips:
            zipf.write(clip)
    return zip_path
