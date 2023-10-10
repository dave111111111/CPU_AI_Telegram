from pytube import YouTube
from transcribe import Transcribe_main
from summarizer import summarize_main
import os  # Import the os module
from pytube import YouTube

def yt_download_Transcribe(video_url, user_language):

    yt = YouTube(video_url)

    # Set the output path for the downloaded audio file
    output_path = './yt_download_audio'

    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

    # Path to the downloaded audio file (with the correct file extension)
    audio_file_path = f"{output_path}/{audio_stream.default_filename}"

    # Check if the audio file already exists
    if not os.path.exists(audio_file_path):
        # Create a YouTube object
        yt = YouTube(video_url)

        # Select the stream with the desired audio quality (e.g., highest quality)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        # Download the audio
        audio_stream.download(output_path)

        print("Audio download complete.")
    else:
        print("Audio file already exists. Skipping download.")

    # Perform transcription
    transcription = Transcribe_main(input_path=audio_file_path, language=f"{user_language}")
    print(transcription)

    # Error handling for Transcribe_main and summarize_main functions
    if not transcription:
        print("Error: Transcription failed.")
    else:
        return transcription
    
def yt_download_main(transcription, min_percentage, max_percentage):

    summary_audio = summarize_main(text=transcription, min_summary_percentage=min_percentage, max_summary_percentage=max_percentage)

    if not summary_audio:
        print("Error: Summarization failed.")

    # Create a variable to store the cleaned summaries
    summary_text = ""
    # Iterate through the cleaned summaries and append them to the variable
    for cleaned_chunk in summary_audio:
        summary_text += f"{cleaned_chunk}\n\n"

    print(f"Transcription: {transcription}")
    print(f"Audio summary: {summary_text}")

    with open("./Transcription and Summarization/Summary.txt", "a") as file:
        file.write(f"{summary_text}")  # Add a newline to separate chunks

    return summary_text

#transcription = yt_download_Transcribe(video_url="""https://www.youtube.com/watch?v=Mi1x5bjpiJ0""", user_language="en")
# summary = yt_download_main(transcription=transcription, min_percentage=30, max_percentage70)
