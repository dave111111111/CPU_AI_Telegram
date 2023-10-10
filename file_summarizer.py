import PyPDF2
from summarizer import summarizing_text

def read_text_or_pdf_file(file_path):
    try:
        if file_path.endswith('.pdf'):
            # Open and read a PDF file
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page].extract_text()
        elif file_path.endswith('.txt'):
            # Open and read a text file
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
        else:
            raise ValueError("Unsupported file format. Only .txt and .pdf files are supported.")

        return text
    except Exception as e:
        return str(e)

# Example usage:
#file_path = r"D:\Coding\Coding\AI_bot\source_documents\Football Reveiw.pdf"  # Replace with the path to your file
#file_contents = read_text_or_pdf_file(file_path)
#print(file_contents)

# Assuming you have a 'summarizing_text' function
#summarized_text = summarizing_text(file_contents)
