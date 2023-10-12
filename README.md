# 💬 CPU_AI_Telegram-Messange

**AI Chatbot with Multifunctionalities**

This is a versatile AI chatbot with various functionalities, including text-to-speech, chat capabilities, summarization of text, audio, and YouTube videos, speech enhancement, and more. You can use this bot to interact with AI models and perform various tasks.

## 🚀 Getting Started

These instructions will help you set up and run the AI chatbot on your system.

### Download Git

Before you start, make sure you have Git installed on your system. If you don't have it, you can download Git from the official website: [Download Git](https://git-scm.com/downloads)🔧.

### Prerequisites

Before you begin, make sure you have Python 3.x (suggested 3.10) installed on your system. You will also need to install the required Python packages. To install them, run the following command: `pip install -r requirements.txt`.


# How to Create a Telegram Bot and Obtain the Token

Follow these steps to create a Telegram bot and obtain the token necessary for your bot development:

## Step 1: Set Up a Telegram Account

If you don't already have one, create a Telegram account.

## Step 2: Open Telegram and Search for BotFather

- Open the Telegram app.
- In the search bar at the top, type "BotFather."
- You will see a user with the name "BotFather" and a blue checkmark. This is the official Telegram bot for creating other bots.

## Step 3: Start a Chat with BotFather

- Click on the "BotFather" user to start a chat.
- Click the "Start" button or send the command "/start" to initiate a chat with BotFather.

## Step 4: Create a New Bot

- To create a new bot, send the command "/newbot" to BotFather.

## Step 5: Choose a Name and Username

- BotFather will ask you to choose a name for your bot. This name can be anything you like.
- Next, you will need to choose a username for your bot. The username must be unique and end with "bot" (e.g., "mytestbot" or "awesome_bot_bot"). BotFather will let you know if the username is available.

## Step 6: Obtain Your Token

- After successfully creating your bot, BotFather will provide you with a unique API token. This token is essential for your bot to communicate with the Telegram API.

## Step 7: Save Your Token

- It's crucial to save your API token in a secure place. You'll need this token to configure your bot.

## Step 8: Configure Your Bot

- Use the API token you obtained from BotFather to configure your bot in your code. Insert the token in the designated place in your code.

And that's it! You've created a Telegram bot and obtained the token to use in your bot code. Now you can integrate your bot with the Telegram platform and start building its functionalities.

Feel free to use this guide in your GitHub README to help others create their Telegram bots and obtain API tokens.


### Download LLM

To download the model the code will automatically start to download them from the gpt4all and TTS github, they OCCUPY MUCH SPACE, so # out some links of site, infact the most heavy files are the llms models and all of them are 69gb while the tts model only 357mb This is the python file `download.py`.

Here is the code to download only the most important model:
`
    gpt4all_urls  = [
        #"https://gpt4all.io/models/wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin",
        #"https://huggingface.co/nomic-ai/gpt4all-falcon-ggml/resolve/main/ggml-model-gpt4all-falcon-q4_0.bin",
        #"https://huggingface.co/TheBloke/Nous-Hermes-13B-GGML/resolve/main/nous-hermes-13b.ggmlv3.q4_0.bin",
        "https://huggingface.co/TheBloke/GPT4All-13B-snoozy-GGML/resolve/main/GPT4All-13B-snoozy.ggmlv3.q4_0.bin",
        #"https://huggingface.co/TheBloke/orca_mini_7B-GGML/resolve/main/orca-mini-7b.ggmlv3.q4_0.bin",
        #"https://huggingface.co/TheBloke/orca_mini_3B-GGML/resolve/main/orca-mini-3b.ggmlv3.q4_0.bin",
        #"https://huggingface.co/TheBloke/orca_mini_13B-GGML/resolve/main/orca-mini-13b.ggmlv3.q4_0.bin",
        #"https://huggingface.co/TheBloke/WizardLM-13B-Uncensored-GGML/resolve/main/wizardLM-13B-Uncensored.ggmlv3.q4_0.bin",
        #"https://huggingface.co/nomic-ai/ggml-replit-code-v1-3b/resolve/main/ggml-replit-code-v1-3b.bin",
        #"https://gpt4all.io/models/ggml-all-MiniLM-L6-v2-f16.bin",
        #"https://gpt4all.io/models/starcoderbase-3b-ggml.bin",
        #"https://gpt4all.io/models/starcoderbase-7b-ggml.bin",
        #"https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin"
    ]
`
### Running the Chatbot

To start the chatbot, use the following command `python chatbot.py`.


## 💡 Functionalities

### Text-to-Speech (TTS)

You can convert text into lifelike speech using the `/tts` command. Customize the voice by choosing the language and speaker.

💬 Chat Command:
To chat with the bot, use the "/chat" command followed by your message. For instance, you can send "/chat what is Wikipedia?" to start a chat with the bot. You can also send PDF or TXT documents to the bot for discussion; it will process them and respond to your questions. To chat with files, use the "/chat_with_files" command followed by a question related to the files.

📃 Summarize Text Command:
Use the "/summarize_text" command to summarize text. Specify the minimum and maximum percentage of the summary along with the text you want to summarize.

🎙️ Summarize Audio Command:
The "/summarize_audio" command allows you to transcribe and summarize audio files. Provide the file name, language, and desired summary percentage.

📺 Summarize YouTube Video Command:
Summarize YouTube videos with the "/summarize_yt_video" command. Provide the video link, language, and summary percentages.

🎙️ Speech Enhancement Command:
Improve audio quality by uploading your audio file and using the "/speech_enhancement" command.

🗑️ Clean Files Command:
Use the "/clean_files" command to remove files you've sent to the bot.

🤖 Chat with Models:
Chat with AI models by using the "/chat" command followed by your message.

💬 Chat with Embeddings:
For more advanced chat capabilities, use the "/chat_with_files" command followed by your message.

📁 File Management:

The chatbot can handle various file types, such as PDF and TXT documents, for summarization and conversation.

🆘 Support:
If you encounter any issues or have questions, feel free to [create an issue](https://github.com/CPU_AI_Telegram-Messange/issues) or [contact us](mailto:bonnie.dido@gmail.com).

📄 License:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
