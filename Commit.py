import subprocess
import sys
import os
from mistralai import Mistral
import time
from dotenv import load_dotenv

def MistralMaind(contentBox):
    #time.sleep(1)

    load_dotenv()

    api_key = os.getenv("MISTRAL_API_KEY")
    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)
    
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": contentBox,
            },
        ]
    )

    #print('\nMISTRAl',chat_response.choices[0].message.content)
    return chat_response.choices[0].message.content

def get_modified_files():
    # Pobierz listę zmodyfikowanych plików
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    modified_files = []
    for line in result.stdout.splitlines():
        if line.startswith( (' M', '??', ' A') ):
            file_path = line.split()[1]
            relative_path = file_path.split('/', 1)[1] if '/' in file_path else file_path
            modified_files.append(relative_path)
    return modified_files



def get_diff_for_file(file_path):
    # Pobierz zmiany dla konkretnego pliku ------
    result = subprocess.run(['git', 'diff', '--', file_path], capture_output=True, text=True, encoding='utf-8')
    return result.stdout

modified_files = get_modified_files()
if not modified_files:
    print("Brak zmodyfikowanych plików - nie dodano commitu.")
    sys.exit()

modifited = ''
for file in modified_files:
    modifited += f"Plik: {file} \n"
    change = get_diff_for_file(file)
    if change == '':
        subprocess.run(['git', 'add', '-N', file], capture_output=True, text=True, encoding='utf-8')
        change = get_diff_for_file(file)
    modifited += "Zmiany w pliku:\n"+change+"\n"

#print(modifited)

contentBox = "Na podstawie nazw plików i zmian w plikach utwórz mi commit dla gita. Commit ma być w języku polskim. Oto lista zmian:"
contentBox += "<changes>"
contentBox += modifited
contentBox += "<changes>"
contentBox += "Wypisz tylko sam commit bez dodawania żadnych fragmentów z plików które zostały zmodyfikowane."
contentBox += "Napisz ten commit bez znaków specjalnych abym mógł go użyć w komendzie git commit -m \"<commit>\". Jeszcze raz nic nie komentuj tylko samą treść commita mi wypisz."
print("MISTRAL ZACZYNA PRACE")
commit = MistralMaind(contentBox)

subprocess.run(['git', 'add', '--all' ], capture_output=True, text=True)
subprocess.run(['git', 'commit', '-m', commit], capture_output=True, text=True)

print("MISTRAL: ",commit)