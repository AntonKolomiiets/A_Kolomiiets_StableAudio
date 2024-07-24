import streamlit as st
import math
import os
from video_processing.file_handler import handle_file_upload
from video_processing.video_splitter import split_video
from video_processing.audio_generator import generate_audio
from video_processing.audio_replacer import replace_audio
from video_processing.zip_creator import create_zip
from video_processing.get_duration import get_duration
from moviepy.editor import VideoFileClip

def main():
    st.set_page_config(layout="wide")
    st.title("Hi Reface!")

    
    with st.sidebar:
        st.header("Upload and Settings")
        video_file = st.file_uploader("Upload a video file", type=["mp4", "avi"])
        prompt = st.text_input("Audio generation prompt", value="")
   
        # Model settings
        with st.expander("Model Settings"):
            steps = st.slider("steps", min_value=10, max_value=1000, value=100, step=10)
            cfg_scale = st.slider("cfg_scale", min_value=1, max_value=20, value=7, step=1)
            sigma_min = st.slider("sigma_min", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
            sigma_max = st.slider("sigma_max", min_value=1, max_value=1000, value=500, step=1)
        
            
        clip_with_audio = st.number_input("Clip number to add audio to", min_value=1)
        num_columns = st.number_input("Number of columns", min_value=3)

        # Upload videdo file
        if video_file:
            video_path = handle_file_upload(video_file)
            video = VideoFileClip(video_path)

            # Define number of parts
            num_parts = st.number_input("Number of video parts", min_value=1, max_value=10, value=1)
            
            # Session state for part duration
            if "part_durations" not in st.session_state:
                st.session_state.part_durations = [0] * num_parts

            # Dynamic slider creation
            total_duration = video.duration
            part_durations = []
            accumulated_duration = 0.0

            st.write("### Select durations for each part (in seconds)")

            for i in range(num_parts - 1):
                min_value = accumulated_duration
                max_value = total_duration - (num_parts - i - 1)
                part_duration = st.slider(f"Part {i+1} duration", min_value=min_value, max_value=max_value, value=st.session_state.part_durations[i] + min_value, step=0.1)
                part_durations.append(part_duration - accumulated_duration)
                accumulated_duration = part_duration

            # The last "slider" to display last part duration
            remaining_duration = total_duration - accumulated_duration
            st.write(f"Part {num_parts} duration: {remaining_duration:.1f} seconds")
            part_durations.append(remaining_duration)

            st.session_state.part_durations = part_durations

            st.write(f"Selected durations: {part_durations}")

    
    

    if st.button("Process"):
        if video_file and prompt:
            try:
                # Split video to clips
                with st.spinner("Splitting clips..."):
                    clips = split_video(video, st.session_state.part_durations)

                # Get duration of selectet clip for audio replacement
                audio_duration = get_duration(clips[clip_with_audio - 1])

                # Generate audio
                with st.spinner("Generating image..."):
                    audio_path = generate_audio(
                        prompt=prompt,
                        lenght=math.ceil(audio_duration),
                        steps=steps,
                        cfg_scale=cfg_scale,
                        sigma_min=sigma_min,
                        sigma_max=sigma_max)
                

                if not os.path.exists(audio_path):
                    st.error(f"Audio file not found at path: {audio_path}")
                    return

                # Replace audio
                clips[clip_with_audio - 1] = replace_audio(clips[clip_with_audio - 1], audio_path)

                # Create zip file
                zip_path = create_zip(clips)
                st.success("Processing complete! Download the clips below.")

                # Download clips
                with open(zip_path, "rb") as f:
                    st.download_button("Download Clips", data=f, file_name="clips.zip")
                
                # Results in columns
                st.write("### Generated Clips:")
                columns = st.columns(num_columns)
                for i, clip in enumerate(clips):
                    col = columns[i % num_columns]
                    col.video(clip)

            
            except Exception as e:
                st.error(f"An error occurred: {e}")
            

        else:
            st.error("Please upload a video file and provide an audio prompt.")


        
if __name__ == "__main__":
    main()