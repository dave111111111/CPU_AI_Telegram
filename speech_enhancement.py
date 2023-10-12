import torch
import torchaudio
from speechbrain.pretrained import SpectralMaskEnhancement
from pydub import AudioSegment
import os
# Convert MP3 to WAV
def mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

def enhance_speech(mp3_file):
    # Convert MP3 to WAV
    wav_file = "input.wav"  # Output WAV file path
    mp3_to_wav(mp3_file, wav_file)

    # Initialize the enhancement model
    enhance_model = SpectralMaskEnhancement.from_hparams(
        source="speechbrain/metricgan-plus-voicebank",
        savedir="speech_enhancement_models",
    )

    # Load and add a fake batch dimension
    noisy = enhance_model.load_audio(wav_file).unsqueeze(0)

    # Add a relative length tensor
    enhanced = enhance_model.enhance_batch(noisy, lengths=torch.tensor([1.]))

    # Saving the enhanced signal to disk
    torchaudio.save('enhanced.wav', enhanced.cpu(), 16000)
    os.remove("input.wav")

filename = "dave.wav"
enhance_speech(mp3_file=f"{filename}")
