import logging
import time
import os
import shutil
from download import download_models
from text_to_speech import audio
from transcribe import Transcribe_main
from integration import subprocess_running, questions
from file_summarizer import read_text_or_pdf_file
from summarizer import summarize_main
from yt_download_transcription_summarization import yt_download_Transcribe, yt_download_main
from speech_enhancement import enhance_speech
from gptfunctioning import chat_with_model
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    Application
)
WAITING_FOR_INPUT = 1
WAITING_FOR_CHAT = 1
WAITING_FOR_TTS = 2

download_models()

# Define language and speaker options
language_keyboards = [
    [
        InlineKeyboardButton("Deutsch", callback_data="de"),
        InlineKeyboardButton("English", callback_data="en"),
        InlineKeyboardButton("Español", callback_data="es"),
        InlineKeyboardButton("Français", callback_data="fr")
    ],
    [
        InlineKeyboardButton("o'zbek", callback_data="uz"),
        InlineKeyboardButton("हिंदी", callback_data="indic"),
        InlineKeyboardButton("українська", callback_data="ua"),
        InlineKeyboardButton("Русский", callback_data="ru"),
    ],
]

# Define speaker options for each language
speaker_options = {
    "de": [
        InlineKeyboardButton("eva_k", callback_data="eva_k"),
        InlineKeyboardButton("friedrich", callback_data="friedrich"),
        InlineKeyboardButton("hokuspokus", callback_data="hokuspokus"),
        InlineKeyboardButton("karlsson", callback_data="karlsson"),
    ],
    "en": [
        
            InlineKeyboardButton("en_0", callback_data="en_0"),
            InlineKeyboardButton("en_1", callback_data="en_1"),
            InlineKeyboardButton("en_2", callback_data="en_2"),
            InlineKeyboardButton("en_3", callback_data="en_3"),
        
            InlineKeyboardButton("en_4", callback_data="en_4"),
            InlineKeyboardButton("en_5", callback_data="en_5"),
            InlineKeyboardButton("en_6", callback_data="en_6"),
            InlineKeyboardButton("en_7", callback_data="en_7"),
        
            InlineKeyboardButton("en_8", callback_data="en_8"),
            InlineKeyboardButton("en_9", callback_data="en_9"),
            InlineKeyboardButton("en_10", callback_data="en_10"),
            InlineKeyboardButton("en_11", callback_data="en_11"),
        
            InlineKeyboardButton("en_12", callback_data="en_12"),
            InlineKeyboardButton("en_13", callback_data="en_13"),
            InlineKeyboardButton("en_14", callback_data="en_14"),
            InlineKeyboardButton("en_15", callback_data="en_15"),
        
            InlineKeyboardButton("en_16", callback_data="en_16"),
            InlineKeyboardButton("en_17", callback_data="en_17"),
            InlineKeyboardButton("en_18", callback_data="en_18"),
            InlineKeyboardButton("en_19", callback_data="en_19"),
        

        
            InlineKeyboardButton("en_20", callback_data="en_20"),
            InlineKeyboardButton("en_21", callback_data="en_21"),
            InlineKeyboardButton("en_22", callback_data="en_22"),
            InlineKeyboardButton("en_23", callback_data="en_23"),
        

        
            InlineKeyboardButton("en_24", callback_data="en_24"),
            InlineKeyboardButton("en_25", callback_data="en_25"),
            InlineKeyboardButton("en_26", callback_data="en_26"),
            InlineKeyboardButton("en_27", callback_data="en_27"),
        

        
            InlineKeyboardButton("en_28", callback_data="en_28"),
            InlineKeyboardButton("en_29", callback_data="en_29"),
            InlineKeyboardButton("en_30", callback_data="en_30"),
            InlineKeyboardButton("en_31", callback_data="en_31"),

        

        
            InlineKeyboardButton("en_32", callback_data="en_32"),
            InlineKeyboardButton("en_33", callback_data="en_33"),
            InlineKeyboardButton("en_34", callback_data="en_34"),
            InlineKeyboardButton("en_35", callback_data="en_35"),

        

        
            InlineKeyboardButton("en_36", callback_data="en_36"),
            InlineKeyboardButton("en_37", callback_data="en_37"),
            InlineKeyboardButton("en_38", callback_data="en_38"),
            InlineKeyboardButton("en_39", callback_data="en_39"),

        

        
            InlineKeyboardButton("en_40", callback_data="en_40"),
            InlineKeyboardButton("en_41", callback_data="en_41"),
            InlineKeyboardButton("en_42", callback_data="en_42"),
            InlineKeyboardButton("en_43", callback_data="en_43"),

        

        
            InlineKeyboardButton("en_44", callback_data="en_44"),
            InlineKeyboardButton("en_45", callback_data="en_45"),
            InlineKeyboardButton("en_46", callback_data="en_46"),
            InlineKeyboardButton("en_47", callback_data="en_47"),

        

        
            InlineKeyboardButton("en_48", callback_data="en_48"),
            InlineKeyboardButton("en_49", callback_data="en_49"),
            InlineKeyboardButton("en_50", callback_data="en_50"),
            InlineKeyboardButton("en_51", callback_data="en_51"),

        

        
            InlineKeyboardButton("en_52", callback_data="en_52"),
            InlineKeyboardButton("en_53", callback_data="en_53"),
            InlineKeyboardButton("en_54", callback_data="en_54"),
            InlineKeyboardButton("en_55", callback_data="en_55"),

        

        
            InlineKeyboardButton("en_56", callback_data="en_56"),
            InlineKeyboardButton("en_57", callback_data="en_57"),
            InlineKeyboardButton("en_58", callback_data="en_58"),
            InlineKeyboardButton("en_59", callback_data="en_59"),

        

        
            InlineKeyboardButton("en_60", callback_data="en_60"),
            InlineKeyboardButton("en_61", callback_data="en_61"),
            InlineKeyboardButton("en_62", callback_data="en_62"),
            InlineKeyboardButton("en_63", callback_data="en_63"),

        

    
            InlineKeyboardButton("en_64", callback_data="en_64"),
            InlineKeyboardButton("en_65", callback_data="en_65"),
            InlineKeyboardButton("en_66", callback_data="en_66"),
            InlineKeyboardButton("en_67", callback_data="en_67"),


            InlineKeyboardButton("en_68", callback_data="en_68"),
            InlineKeyboardButton("en_69", callback_data="en_69"),
            InlineKeyboardButton("en_70", callback_data="en_70"),
            InlineKeyboardButton("en_71", callback_data="en_71"),


            InlineKeyboardButton("en_72", callback_data="en_72"),
            InlineKeyboardButton("en_73", callback_data="en_73"),
            InlineKeyboardButton("en_74", callback_data="en_74"),
            InlineKeyboardButton("en_75", callback_data="en_75"),


            InlineKeyboardButton("en_76", callback_data="en_76"),
            InlineKeyboardButton("en_77", callback_data="en_77"),
            InlineKeyboardButton("en_78", callback_data="en_78"),
            InlineKeyboardButton("en_79", callback_data="en_79"),


            InlineKeyboardButton("en_80", callback_data="en_80"),
            InlineKeyboardButton("en_81", callback_data="en_81"),
            InlineKeyboardButton("en_82", callback_data="en_82"),
            InlineKeyboardButton("en_83", callback_data="en_83"),


            InlineKeyboardButton("en_84", callback_data="en_84"),
            InlineKeyboardButton("en_85", callback_data="en_85"),
            InlineKeyboardButton("en_86", callback_data="en_86"),
            InlineKeyboardButton("en_87", callback_data="en_87"),


            InlineKeyboardButton("en_88", callback_data="en_88"),
            InlineKeyboardButton("en_89", callback_data="en_89"),
            InlineKeyboardButton("en_90", callback_data="baya"),
            InlineKeyboardButton("en_91", callback_data="en_91"),


            InlineKeyboardButton("en_93", callback_data="en_93"),
            InlineKeyboardButton("en_94", callback_data="en_94"),
            InlineKeyboardButton("en_95", callback_data="en_95"),
            InlineKeyboardButton("en_96", callback_data="en_96"),

 
            InlineKeyboardButton("en_97", callback_data="en_97"),
            InlineKeyboardButton("en_98", callback_data="en_98"),
            InlineKeyboardButton("en_99", callback_data="en_99"),
            InlineKeyboardButton("en_100", callback_data="en_100"),

            InlineKeyboardButton("en_101", callback_data="en_101"),
            InlineKeyboardButton("en_102", callback_data="en_102"),
            InlineKeyboardButton("en_103", callback_data="en_103"),
            InlineKeyboardButton("en_104", callback_data="en_104"),


            InlineKeyboardButton("en_105", callback_data="en_105"),
            InlineKeyboardButton("en_106", callback_data="en_106"),
            InlineKeyboardButton("en_107", callback_data="en_107"),
            InlineKeyboardButton("en_108", callback_data="en_108"),


            InlineKeyboardButton("en_109", callback_data="en_109"),
            InlineKeyboardButton("en_110", callback_data="en_110"),
            InlineKeyboardButton("en_111", callback_data="en_111"),
            InlineKeyboardButton("en_112", callback_data="en_112"),


            InlineKeyboardButton("en_113", callback_data="en_113"),
            InlineKeyboardButton("en_114", callback_data="en_114"),
            InlineKeyboardButton("en_115", callback_data="en_115"),
            InlineKeyboardButton("en_116", callback_data="en_116"),
            InlineKeyboardButton("en_117", callback_data="en_117"),


        
    ],
    "es": [
        InlineKeyboardButton("es_0", callback_data="es_0"),
        InlineKeyboardButton("es_1", callback_data="es_1"),
        InlineKeyboardButton("es_2", callback_data="es_2"),
    ],
    "fr": [
        
            InlineKeyboardButton("fr_0", callback_data="fr_0"),
            InlineKeyboardButton("fr_1", callback_data="fr_1"),
            InlineKeyboardButton("fr_2", callback_data="fr_2"),

            InlineKeyboardButton("fr_3", callback_data="fr_3"),
            InlineKeyboardButton("fr_4", callback_data="fr_4"),
            InlineKeyboardButton("fr_5", callback_data="fr_5")
        
    ],
    "uz": [
                InlineKeyboardButton("dilnavoz", callback_data="dilnavoz")

        ],
    "indic": [
        [
            InlineKeyboardButton("bengali_female", callback_data="bengali_female"),
            InlineKeyboardButton("bengali_male", callback_data="bengali_male"),
            InlineKeyboardButton("gujarati_female", callback_data="gujarati_female"),
            InlineKeyboardButton("gujarati_male", callback_data="gujarati_male"),
        ],
        [
            InlineKeyboardButton("hindi_female", callback_data="hindi_female"),
            InlineKeyboardButton("hindi_male", callback_data="hindi_male"),
            InlineKeyboardButton("kannada_female", callback_data="kannada_female"),
            InlineKeyboardButton("kannada_male", callback_data="kannada_male"),
        ],
        [
            InlineKeyboardButton("malayalam_female", callback_data="malayalam_female"),
            InlineKeyboardButton("malayalam_male", callback_data="malayalam_male"),
            InlineKeyboardButton("manipuri_female", callback_data="manipuri_female"),
            InlineKeyboardButton("rajasthani_female", callback_data="rajasthani_female"),
        ],
        [
            InlineKeyboardButton("rajasthani_male", callback_data="rajasthani_male"),
            InlineKeyboardButton("tamil_female", callback_data="tamil_female"),
            InlineKeyboardButton("tamil_male", callback_data="tamil_male"),
            InlineKeyboardButton("telugu_female", callback_data="telugu_female"),
        ],
        [
            InlineKeyboardButton("telugu_male", callback_data="telugu_male"),
            # Add more buttons here as needed
        ],
    ],
    "ua": [
            InlineKeyboardButton("mykyta", callback_data="mykyta")
    ],
    "ru": [
            InlineKeyboardButton("aidar", callback_data="aidar"),
            InlineKeyboardButton("baya", callback_data="baya"),
            InlineKeyboardButton("kseniya", callback_data="kseniya"),
            InlineKeyboardButton("xenia", callback_data="xenia"),
            InlineKeyboardButton("eugene", callback_data="eugene")
    ],
}

reply_markup_language = InlineKeyboardMarkup(language_keyboards)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

def remove_start_end_quotes_and_brackets(text):
    # Remove starting and ending quotes (both single and double)
    text = text[1:-1]

    # Remove starting and ending square brackets
    text = text[1:-1]

    return text

async def start(update: Update, context: CallbackContext) -> None:

    introduction_message = (
"""
📊 Polls Command:
With the "/polls" command, you can initiate the text-to-speech (TTS) process and engage in a chat with the bot. For example, you can send "/polls" to start the process.

💬 Chat Command:
To chat with the bot, use the "/chat" command followed by your message. For instance, you can send "/chat what is Wikipedia?" to start a chat with the bot. You can also send PDF or TXT documents to the bot for discussion; it will process them and respond to your questions. To chat with files, use the "/chat_with_files" command followed by a question related to the files.

📃 Summarize Files Command:
Use the "/file_summarize" command followed by the name of a file previously sent to the bot, along with the minimum and maximum percentage of the summary. For example, you can use "/file_summarize "Research_paper.pdf" 30 70" to summarize a document.

📃 Summarize Text Command:
To summarize text, use the "/summarize_text" command, specifying the minimum and maximum percentage of the summary, along with the text you want to summarize. For instance, you can send "/summarize_text 20 50" followed by your text.

🎙️ Summarize Audio Command:
For audio summarization, use the "summarize_audio" command. Provide the name of the audio file you've uploaded, the language, and the desired range for the summary percentage. For example, send "/summarize_audio "audio_file.mp3" en 20 70".

📺 Summarize YouTube Video Command:
To summarize a YouTube video, use the "summarize_yt_video" command. Include the link to the video, the language, and the minimum and maximum percentages for the summary. For example, send "/summarize_yt_video "https://youtube.com/your_video" en 10 40".

🎙️ Speech Enhancement Command:
You can enhance audio quality by uploading your audio file and using the "/speech_enhancement" command, followed by the name of the uploaded audio file. For example, send "/speech_enhancement "enhance_audio.wav".

🗑️ Clean Files Command:
To remove files you've sent to the bot, use the "/clean_files" command. For example, you can send "/clean_files" to clear your workspace.

🔊 Text-to-Speech (TTS) Command:
If you'd like to convert text into speech, start with the "/polls" command, select TTS, and follow the prompts to choose a language and speaker. Once configured, use the "/tts" command followed by your text. For example, send "/tts "Hello, how are you?" to initiate the TTS process.

Enjoy using these commands! 👍"""
    )

    await update.message.reply_text(introduction_message)

async def polls(update: Update, context: CallbackContext) -> None:
    """Start the bot and display the main menu."""
    reply_markup_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("Chat", callback_data="chat"),
         InlineKeyboardButton("Text_to_speech", callback_data="TTS")]
    ])
    await update.message.reply_text(text=""""Here Are Your Interactive Options 🤖🗣️💬

Explore the exciting capabilities of this AI-powered bot with the following choices:

1. Text-to-Speech (TTS) 🗣️:
Convert your text into lifelike speech! Use the "/tts" command to transform any text message into spoken words. Select your preferred language and speaker to customize the voice.

2. Chatting 💬:
Engage in natural conversations with the bot! Initiate a chat by sending "/chat" followed by your message. The bot will respond with meaningful interactions.

Select the option that suits your needs, and let's get started on a journey of voice and conversation! 👇""", reply_markup=reply_markup_menu)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == 'chat':
        await query.edit_message_text("Ok, chat with me.🤖")
        context.user_data.clear()
        # Set the state to indicate chat input
        context.user_data['state'] = WAITING_FOR_CHAT
    elif query.data == 'TTS':
        context.user_data.clear()
        await query.edit_message_text("Please choose the language🗣️:", reply_markup=reply_markup_language)
        # Set the state to indicate TTS input
        context.user_data['state'] = WAITING_FOR_TTS
    elif query.data in [lang.callback_data for row in language_keyboards for lang in row]:
        context.user_data.clear()
        selected_language = query.data
        keyboard_speaker = speaker_options.get(selected_language, [])
        reply_markup_speaker = InlineKeyboardMarkup([keyboard_speaker])
        await query.edit_message_text("Please choose the speaker:", reply_markup=reply_markup_speaker)
        context.user_data['selected_language'] = selected_language
    elif query.data in [spk.callback_data for spk in speaker_options.get(context.user_data.get('selected_language', ''), [])]:
        global selected_speaker
        selected_speaker = query.data
        selected_language = context.user_data.get('selected_language')
        
        # Set the state to indicate the bot is waiting for input
        context.user_data['state'] = WAITING_FOR_INPUT
        
        await query.edit_message_text("Please enter the text you want to convert to audio with this command: /tts <text you want to tts>")
    else:
        context.user_data.clear()

# Handle user text input
async def TTS(update: Update, context: CallbackContext):
    user_input = update.message.text
    # Extract the text after "/TTS " and assign it to user_input
    user_input = user_input[len("/tts "):].strip()

    # Rest of the code remains the same
    selected_language = context.user_data.get('selected_language')
    print("Language:", selected_language)
    print("Speaker:", selected_speaker)
    print("User Input:", user_input)
    # Clear the state
    context.user_data.pop('state', None)
    if user_input is not None:
        await update.message.reply_text("Creating your Audio file...🗣️")
    # Example usage
    combined_audio_path = audio(language=selected_language, text=user_input, speaker=selected_speaker, set_number=5)
    print(f"Combined audio file saved at: {combined_audio_path}")
    os.remove("test.wav")
    await update.message.reply_audio(audio=open(f"TTS.wav", 'rb'))
    os.remove("TTS.wav")

async def speech_enhancer(update: Update, context: CallbackContext):
    user_input = update.message.text
    # Split the input by whitespace to separate the command and the filename
    parts = user_input.split()
    if len(parts) == 2 and parts[0] == "/speech_enhancement":
        filename = parts[1]
        print("Filename:", filename)
        path = f"source_everything_else/{filename}"
        await update.message.reply_text("Enhancing your audio_file...🗣️")
        enhance_speech(mp3_file=path)
        await update.message.reply_audio(audio=open("enhanced.wav", 'rb'))
        os.remove("enhanced.wav")

    else:
        await update.message.reply_text("Invalid command. Please use '/speech_enhancement filename' format.")

async def summarize_text(update: Update, context: CallbackContext):
    # Handle user text input
    user_input = update.message.text

    # Split the input to get the command parts
    command_parts = user_input.split()
    try:
        if len(command_parts) >= 4:  # Check if there are at least four parts
            min_percentage = int(command_parts[1])
            max_percentage = int(command_parts[2])
            user_text = " ".join(command_parts[3:])  # Join the remaining elements as user_text
            print("max percentage:", max_percentage, "min_percentage:", min_percentage, "text:", user_text)
            await update.message.reply_text("Summarizing your text...📖")   
            # Call the summarize_main function
            summary = summarize_main(text=user_text, min_summary_percentage=min_percentage, max_summary_percentage=max_percentage)

            # Create a variable to store the cleaned summaries
            summary_text = ""

            # Iterate through the cleaned summaries and append them to the variable
            for cleaned_chunk in summary:
                summary_text += f"{cleaned_chunk}\n\n"

            await update.message.reply_text(f"{summary_text}")
    except ValueError:
        await update.message.reply_text("Invalid max_percentage or min_percentage values. Please provide valid integers.")

async def summarize_audio(update: Update, context: CallbackContext):
    user_input = update.message.text
    # Split the command into individual parts
    command_parts = user_input.split()

    # Extract the file name, language, min percentage, and max percentage
    file_name = command_parts[1].strip('"')
    user_language = command_parts[2]
    min_percentage = int(command_parts[3])
    max_percentage = int(command_parts[4])
    
    # Validate percentage values
    if min_percentage < 0 or min_percentage > 100 or max_percentage < 0 or max_percentage > 100:
        await update.message.reply_text("Error: Min and Max Percentages should be between 0 and 100.")
        return  # Exit the function

    await update.message.reply_text("Transcribing and summarizing...")
    transcription_audio = Transcribe_main(input_path=f"source_everything_else/{file_name}", language=user_language)
    
    # Error handling for Transcribe_main and summarize_main functions
    if not transcription_audio:
        await update.message.reply_text("Error: Transcription failed.")
        return  # Exit the function
    
    summary_audio = summarize_main(text=transcription_audio, min_summary_percentage=min_percentage, max_summary_percentage=max_percentage)

    if not summary_audio:
        await update.message.reply_text("Error: Summarization failed.")
        return  # Exit the function

    # Create a variable to store the cleaned summaries
    summary_text = ""

    # Iterate through the cleaned summaries and append them to the variable
    for cleaned_chunk in summary_audio:
        summary_text += f"{cleaned_chunk}\n\n"

    await update.message.reply_text(f"Transcription: {transcription_audio}")
    await update.message.reply_text(f"Audio summary: {summary_text}")
    
    with open("./Transcription and Summarization/Summary.txt", "a") as file:
        file.write(f"{summary_text}")  # Add a newline to separate chunks

async def summarize_yt_video(update: Update, context: CallbackContext):
    user_input = update.message.text
    # Split the command into individual parts
    command_parts = user_input.split()

    # Extract the file name, language, min percentage, and max percentage
    url_video = command_parts[1].strip('"')
    user_language = command_parts[2]
    min_percentage = int(command_parts[3])
    max_percentage = int(command_parts[4])
    
    transcription = yt_download_Transcribe(video_url=url_video, user_language=user_language)
    await update.message.reply_text(f"Transcription: {transcription}")
    summary = yt_download_main(transcription=transcription, min_percentage=min_percentage, max_percentage=max_percentage)
    await update.message.reply_text(f"Summary: {summary}")

async def file_summarize(update: Update, context: CallbackContext):

    # Get the text of the command message
    command_text = update.message.text

    # Split the command into individual parts
    command_parts = command_text.split()

    # Extract the file name, min words, and max words
    file_name = " ".join(command_parts[1:-2]).strip('"')
    min_percentage = int(command_parts[-2])
    max_percentage = int(command_parts[-1])

    print("File:", file_name, "min_percentage:", min_percentage, "max_percentage:", min_percentage)
    await update.message.reply_text("Summarizing your file...📖")   

    # Check if the file name has a valid extension (e.g., .pdf)
    if not file_name.lower().endswith(('.pdf', '.txt')):
        await update.message.reply_text("Unsupported file format. Only PDF and TXT files are supported.")
        return

    # Construct the full file path
    file_path = f"./source_documents/{file_name}"

    # Check if the file exists
    if not os.path.exists(file_path):
        await update.message.reply_text("File not found. Please check the file name.")
        return

    # Check if the desired word counts are valid integers
    if not (isinstance(max_percentage, int) and isinstance(min_percentage, int)):
        await update.message.reply_text("Invalid word count. Please provide valid integer word counts.")
        return

    file_content = read_text_or_pdf_file(file_path=file_path)
    file_summary_unclean = summarize_main(text=file_content, min_summary_percentage=min_percentage, max_summary_percentage=max_percentage)
    # Create a variable to store the cleaned summaries
    summary_text = ""

    # Iterate through the cleaned summaries and append them to the variable
    for cleaned_chunk in file_summary_unclean:
        summary_text += f"{cleaned_chunk}\n\n"

    await update.message.reply_text(f"{summary_text}")

async def downloader(update: Update, context: CallbackContext):
    if os.path.exists("source_documents") == False:
        os.mkdir("source_documents")
    
    if os.path.exists("source_everything_else") == False:
        os.mkdir("source_everything_else")
    
    # Download file
    document = update.message.document
    file_name = document.file_name
    new_file = await document.get_file()

    if document is not None:
        file_name = document.file_name
        # Proceed with your file handling code here
    else:
        # Handle the case where the document is None
        update.message.reply_text("No document found in the message.")

    # Specify the destination directory path based on the file extension
    file_extension = os.path.splitext(file_name)[1].lower()
    if file_extension in {'.pdf', '.txt'}:
        destination_directory = "source_documents"
    else:
        destination_directory = "source_everything_else"

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    # Set the full path for the destination file
    destination_path = os.path.join(destination_directory, file_name)

    # Download the file and save it to the destination path
    file_data = await new_file.download_as_bytearray()
    with open(destination_path, "wb") as f:
        f.write(file_data)

    # Acknowledge file received
    await update.message.reply_text(f"{file_name} saved to {destination_directory} successfully")

async def clean_files(update: Update, context: CallbackContext) -> None:
    try:
        # Replace 'source_documents' with the path to your directory
        directory_path = 'source_documents'

        # List all files in the directory
        files = os.listdir(directory_path)

        # Iterate through the files and remove them
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Send a success message to the user
        await update.message.reply_text("All files in 'source_documents' directory have been successfully removed.")

    except Exception as e:
        # Handle any exceptions that may occur during file removal
        error_message = f"An error occurred while cleaning files: {str(e)}"
        await update.message.reply_text(error_message)

    try:
        # Replace 'source_documents' with the path to your directory
        directory_path = 'source_everything_else'

        # List all files in the directory
        files = os.listdir(directory_path)

        # Iterate through the files and remove them
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Send a success message to the user
        await update.message.reply_text("All files in 'source_everything_else' directory have been successfully removed.")

    except Exception as e:
        # Handle any exceptions that may occur during file removal
        error_message = f"An error occurred while cleaning files: {str(e)}"
        await update.message.reply_text(error_message)

    def delete_contents_in_directory(directory):
        # Check if the directory exists
        if os.path.exists(directory):
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    # If it's a directory, delete its contents recursively
                    shutil.rmtree(item_path)
                else:
                    # If it's a file, delete the file
                    os.remove(item_path)
        else:
            print(f"Directory '{directory}' does not exist.")

    def delete_directory(directory):
        try:
            delete_contents_in_directory(directory)  # Delete contents within 'db'
            os.rmdir(directory)  # Delete the 'db' directory
            print(f"Directory '{directory}' has been deleted.")
        except FileNotFoundError:
            print(f"Directory '{directory}' does not exist.")
        except PermissionError:
            print(f"Permission denied to delete '{directory}'.")

    # Specify the directory you want to delete and its path
    directory_to_delete = "db"  # Change this to your desired directory path

    # Call the function to delete the 'db' directory and its contents
    delete_directory(directory_to_delete)

async def Chat_with_embeddings(update: Update, context: CallbackContext) -> None:  
    user_message = update.message.text
    start_time = time.time()  # Record the start time

    subprocess_running()
    await update.message.reply_text("Processing chat...")
    # Extract the text after "/chat " and assign it to user_message
    user_message = user_message[len("/chat_with_files "):].strip()
    # Process chat input
    model_reply = questions(query=user_message)
    await update.message.reply_text(model_reply)

    end_time = time.time()  # Record the end time
    processing_time = end_time - start_time  # Calculate processing time
    time_response = f"Response Time: {processing_time:.2f} seconds⏱️"
    await update.message.reply_text(time_response)

async def Chat(update: Update, context: CallbackContext) -> None:
    user_message = ""
    user_message = update.message.text
    start_time = time.time()  # Record the start time

    # Check if the user's message starts with "/chat "
    if user_message.startswith("/chat "):
        await update.message.reply_text("Processing chat...")

        # Extract the text after "/chat " and assign it to user_message
        user_message = user_message[len("/chat "):].strip()

        # Process chat input
        model_reply = chat_with_model(user_input=user_message)
        await update.message.reply_text(model_reply)

    end_time = time.time()  # Record the end time
    processing_time = end_time - start_time  # Calculate processing time
    time_response = f"Response Time: {processing_time:.2f} seconds⏱️"
    await update.message.reply_text(time_response)

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Use /start to test this bot.")

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("polls", polls))
    application.add_handler(CommandHandler("file_summarize", file_summarize))
    application.add_handler(CommandHandler("summarize_text", summarize_text))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("summarize_audio", summarize_audio))
    application.add_handler(CommandHandler("summarize_yt_video", summarize_yt_video))
    application.add_handler(CommandHandler("speech_enhancement", speech_enhancer))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tts", TTS))
    application.add_handler(CommandHandler("chat", Chat))
    application.add_handler(CommandHandler("chat_with_files", Chat_with_embeddings))
    application.add_handler(CommandHandler("clean_files", clean_files))
    application.add_handler(MessageHandler(filters.ALL, downloader))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
