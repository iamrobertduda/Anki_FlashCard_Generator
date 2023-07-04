# import required packages
import PyPDF2
import openai
import os
import requests

# Initialize OpenAI API with your key


openai.api_key = 'YOUR-API-KEY'

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


url = "https://edge-config.vercel.com/ecfg_qb7ymmxm41illxzlso3texjkhtkm/item/openai_api"  # Ersetze "example.com" durch die gewünschte Adresse

response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
if response.status_code == 200:
    openai.api_key = response.raw
    print(response.raw)

# Read PDF
def read_pdf(file_path):

    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])

    return text

# dividing text into smaller chunks:
def divide_text(text, section_size):
    sections = []
    start = 0
    end = section_size
    while start < len(text):
        section = text[start:end]
        sections.append(section)
        start = end
        end += section_size
    return sections

# Create Anki cards
def create_anki_cards(pdf_text,):
    # Limit the number of prompts to avoid excessive API usage

    SECTION_SIZE = 1000
    divided_sections = divide_text(pdf_text, SECTION_SIZE)
    # text = divided_sections[0]
    generated_flashcards = ' '
    for i, text in enumerate(divided_sections):
    
        ## You might need to change the Prompt to get consistent format.
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Create anki flashcards with the provided text using a format: question;answer next line question;answer etc. Keep question and the corresponding answer on the same line {text}"}
            ]

        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages, 
                temperature =0.3,
                max_tokens=2048
            )

        response_from_api = response['choices'][0]['message']['content']#.strip()
        generated_flashcards += response_from_api

        if i==0:
            break

    # # Save the cards to a text file
    with open(f'{ROOT_DIRECTORY}/output/flashcards.txt', "w") as f:
        f.write(generated_flashcards)






