import os
import torch
from pydub import AudioSegment

def audio(language, text, speaker, set_number=5):
    device = torch.device('cpu')
    torch.set_num_threads(4)

    local_file = f'./models_TTS/model_{language}.pt'

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    example_text = text
    sample_rate = 48000
    speaker = speaker

    # Split the text into chunks based on the number of phrases (set_number)
    text_chunks = example_text.split('\n\n')
    
    # Initialize a list to store the audio segments
    audio_segments = []

    # Generate audio for each text chunk
    for i, chunk in enumerate(text_chunks):
        audio_path = model.save_wav(text=chunk, speaker=speaker, sample_rate=sample_rate)
        audio = AudioSegment.from_file(audio_path)
        audio_segments.append(audio)

    # Combine the audio segments into one audio file
    combined_audio = sum(audio_segments)
    
    combined_audio_path = f'TTS.wav'
    combined_audio.export(combined_audio_path, format="wav")
    
    return combined_audio_path


#audio(language="en", text="""The FIFA World Cup, the pinnacle of international football, unites nations in a celebration of sport. It's a quadrennial spectacle that transcends borders and cultures. Teams from around the globe compete for the coveted trophy, showcasing their skills and national pride. Established in 1930, the tournament has a rich history of memorable moments, from Pele's dazzling displays to Maradona's "Hand of God." The World Cup is not just about football; it's about passion, unity, and the human spirit. It brings the world together, with billions of fans cheering for their teams. The FIFA World Cup is more than a competition; it's a global phenomenon.""", speaker="en_5", set_number=5)
#os.remove("test.wav")