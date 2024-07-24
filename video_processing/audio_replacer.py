from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip

def replace_audio(clip_path, audio_path):
    """
    Replace audio to a selected clip
    """
    # Load the video and get its duration
    video = VideoFileClip(clip_path)
    video_duration = video.duration

    # Load the audio and get its duration
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration

    # Stitch the audio together if its duration is less than the video duration
    if audio_duration < video_duration:
        num_repeats = int(video_duration // audio_duration) + 1
        audio = concatenate_audioclips([audio] * num_repeats)
    
    # Truncate the audio to match the video duration
    audio = audio.subclip(0, video_duration)

    # Replace the video's audio
    video.audio = CompositeAudioClip([audio])
    
    # Define output path
    output_path = f"clip_with_audio_{clip_path}"
    
    # Write the result to a new video file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    return output_path