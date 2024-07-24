from moviepy.editor import VideoFileClip

def get_duration(video_path:str) -> float:
    """
    Utility function to get duration of clip with it's path
    """
    video = VideoFileClip(video_path)
    duration = video.duration
    return duration