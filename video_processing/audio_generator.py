import torch
import torchaudio
import os
import typing as T
import streamlit as st
from einops import rearrange
from stable_audio_tools import get_pretrained_model
from stable_audio_tools.inference.generation import generate_diffusion_cond

def sanitize_filename(prompt: str) -> str:
    return "".join(c for c in prompt if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')[:50]

@st.cache_data(persist=True)
def generate_audio(
        prompt:str,
        lenght:int,
        steps:int,
        cfg_scale:int,
        sigma_min:float,
        sigma_max:int,
        ) -> T.List[str]:
    """
    Generate audio file with text prompt, 
    file lenght in seconds, up to 47s
    steps 10-1000
    cfg_scale 1-20
    sigma_min 0.0-1.0
    sigma_max 1-1000

    """
    device = "cuda" if torch.cuda.is_available() else "cpu"

 
    # Download model
    model, model_config = get_pretrained_model("stabilityai/stable-audio-open-1.0")
    sample_rate = model_config["sample_rate"]
    sample_size = model_config["sample_size"]

    model = model.to(device)

    # Set up text and timing conditioning
    conditioning = [{
        "prompt": prompt,
        "seconds_start": 0, 
        "seconds_total": lenght
    }]

    # Generate stereo audio
    output = generate_diffusion_cond(
        model,
        steps=steps,
        cfg_scale=cfg_scale,
        conditioning=conditioning,
        sample_size=sample_size,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        sampler_type="dpmpp-3m-sde",
        device=device
    )

    # Rearrange audio batch to a single sequence
    output = rearrange(output, "b d n -> d (b n)")

    # Peak normalize, clip, convert to int16, and save to file
    output = output.to(torch.float32).div(torch.max(torch.abs(output))).clamp(-1, 1).mul(32767).to(torch.int16).cpu()

    # Create the output directory if it does not exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Generate the file path
    sanitized_prompt = sanitize_filename(prompt)
    filename = f"{sanitized_prompt}.wav"
    file_path = os.path.join(output_dir, filename)

    torchaudio.save(file_path, output, sample_rate)

    os.system('afplay /System/Library/Sounds/Glass.aiff')
    os.system('afplay /System/Library/Sounds/Glass.aiff')
    

    return file_path
