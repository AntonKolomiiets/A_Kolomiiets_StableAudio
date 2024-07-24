# Hi Reface!

Here is a Streamlit application for processing video files. This project allows users to upload videos, generate audio from text prompts, and replace the audio in the video clips.

## Features

- Upload video files in mp4 or avi format.
- Split videos into multiple parts with custom duration.
- Generate audio from text prompts.
- Replace audio in video clips with generated audio.
- Download processed video clips.

## Exra

With the model provided by the task (Riffusion), I was not able to get decent sounding results. An application that uses Riffusion can be found here: ["Link here"](https://github.com/AntonKolomiiets/A_Kolomiiets_RiffusionModel), if it is absolutely necessary to complete the task using Riffusion.

The model used in this app can be found here: https://huggingface.co/stabilityai/stable-audio-open-1.0.

The model was trained on Freesound and Free Music Archive, so prompts should contain exact music types, instruments, etc., like "128 BPM tech house drum loop", instead of "Eminem-like hip-hop mixed with LinkinPark."

## Installation

To run the application locally, clone the repo from GitHub with `git clone`, install dependencies with `pip install -r requirements.txt` and run with `streamlit run app.py`

## Sugesstions

With Streamlit i could not find reliable library to make use of browser's local storage to store Prompt and model values, to prevent acident delition or settings lost. And as I'm also familiar with JavaScrypt, If we used somethin like React for interface, we could open mode features to prompt engeneers and also help them manage their work better.