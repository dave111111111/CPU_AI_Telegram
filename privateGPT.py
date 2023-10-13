#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
import os
import argparse
import subprocess

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

from constants import CHROMA_SETTINGS

def ask_question_and_get_answer(question, model_path, model_type, model_n_ctx, model_n_batch, target_source_chunks, embeddings_model_name, persist_directory, args):
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    
    # Activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    
    # Prepare the LLM
    if model_type == "LlamaCpp":
        llm = LlamaCpp(model_path=model_path, max_tokens=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False)
    elif model_type == "GPT4All":
        llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gptj', n_batch=model_n_batch, callbacks=callbacks, verbose=False)
    else:
        raise Exception(f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not args.hide_source)

    # Get the answer for the provided question
    res = qa(question)
    answer = res['result']
    documents = res['source_documents'] if not args.hide_source else []

    if not args.hide_source:
        relevant_sources = []
        for document in documents:
            source_text = f"Source: {document.metadata['source']}\n{document.page_content}"
            if source_text not in relevant_sources:
                relevant_sources.append(source_text)

    return answer, relevant_sources

def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()

args = parse_arguments()

def subprocess_running():

    # Path to the Python script
    script_path = r"ingest.py"

    # Run the script in the user's terminal
    process = subprocess.Popen(['python', script_path], shell=True)

    # Wait for the script to finish
    process.wait()

def main_embeddings_question(question):

    subprocess_running()
    answer, sources = ask_question_and_get_answer(question, model_path, model_type, model_n_ctx, model_n_batch, target_source_chunks, embeddings_model_name, persist_directory, args)

    combined_result = f"\n> Question:\n{question}\n\n> Answer:\n{answer}"

    if not args.hide_source:
        combined_result += "\n\n> Relevant Sources:\n" + "\n".join(sources)

    print(combined_result)
    return combined_result



#question = "How long is a football pitch?"  # Provide your question

#main_embeddings_question(question)