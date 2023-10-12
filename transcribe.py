import os
from pydub import AudioSegment
import whisper
from pydub.silence import split_on_silence
import re

# Function to remove audio chunk files
def remove_audio_chunk_files(folder_name):
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

if os.path.exists("Transcription and Summarization") == False:
    os.mkdir("Transcription and Summarization")

# Check if the "audio-chunk" directory exists, and if it does, remove its contents
if os.path.exists("audio-chunks"):
    remove_audio_chunk_files("audio-chunks")
else:
    os.mkdir("audio-chunks")

def convert_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

# Function to transcribe audio chunk by chunk
def transcribe_audio_chunk(audio_chunk, language, model_name="large-v2"):
    # Load the Whisper model
    model = whisper.load_model(model_name)

    # Transcribe the audio chunk using Whisper with the specified language
    result = model.transcribe(audio_chunk, language=language)
    text = result["text"]

    # Capitalize the first letter and add a period
    text = f"{text.capitalize()}."

    return text

def count_words(text):
    words = text.split()
    return len(words)

def Transcribe_main(input_path, language):
    folder_name = "audio-chunks"
    output_path = "output.wav"  # Replace with the desired output file path

    # Get the last successfully transcribed chunk number
    last_chunk_number = 0
    if os.path.exists("./Transcription and Summarization/Transcription_with_timestamps.txt"):
        with open("./Transcription and Summarization/Transcription_with_timestamps.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                last_chunk_number = int(last_line.split(":")[0][1:])

    # Remove existing audio chunk files if they exist
    remove_audio_chunk_files(folder_name)
    # Convert the audio file to .wav
    convert_to_wav(input_path, output_path)

    # Load the entire audio as one segment
    sound = AudioSegment.from_wav(output_path)

    # Split audio into chunks based on silence
    chunks = split_on_silence(
        sound,
        min_silence_len=500,
        silence_thresh=sound.dBFS - 14,
        keep_silence=500
    )

    transcription = ""
    combined_chunk = ""
    
    # Check if there's an existing transcription and load it
    existing_transcription = ""
    if os.path.exists("./Transcription and Summarization/Transcription_with_timestamps.txt"):
        with open("./Transcription and Summarization/Transcription_with_timestamps.txt", "r") as file:
            existing_transcription = file.read()

    # Iterate through the audio chunks, starting from the last successfully transcribed chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        if i <= last_chunk_number:
            continue  # Skip already transcribed chunks

        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        # Transcribe the current chunk
        text = transcribe_audio_chunk(chunk_filename, language=f"{language}")

        with open('./Transcription and Summarization/Transcription_with_timestamps.txt', 'a', encoding='utf-8') as file:
            file.write(f"[{i}:00] {text}\n")

        # Combine short chunks with the previous one
        if len(text.split()) <= 16:  # Adjust the word count threshold as needed
            combined_chunk += text + ' '
        else:
            transcription += combined_chunk
            combined_chunk = text + ' '

    # Add the remaining combined chunk
    transcription += combined_chunk
    # Remove consecutive periods
    text_without_double_periods = re.sub(r'\.{2,}', '.', transcription)

    # Capitalize the first letter at the start of sentences
    text_with_capitalized_start = re.sub(r'(?<=[.!?])\s*([a-z])', lambda x: x.group(1).upper(), text_without_double_periods)

    # Append the new transcription to the existing one
    final_transcription = existing_transcription + text_with_capitalized_start
    os.remove("output.wav")
    return final_transcription

transcription = Transcribe_main(input_path=r"D:\Coding\CPU_AI_Telegram\yt_download_audio\Imperialism Crash Course World History 35.mp4", language="en")
