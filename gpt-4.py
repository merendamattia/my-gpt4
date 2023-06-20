# Importo GPT-4
from gpt4free import you

# Serve per stampare le scritte colorate
from colorama import init, Fore, Back, Style
init()

# Vado a verificare se la cartella chat e se il file history_chat esistono già
# Se non esistono li creo
import os
if not os.path.exists("chat"):
    os.makedirs("chat")
if not os.path.isfile('./chat/history_chat.txt'):
    with open('./chat/history_chat.txt', 'w') as file:
        file.write("My history-chat$$$by @merendamattia")

# Messaggio iniziale
print(Fore.RED + "#chatbot model GPT-4 (`q`: to quit)" + Fore.RESET)

chat = []

# Mi serve per aggiornare poi la history-chat
output = "" 

# Leggo la history-chat e 're-insegno' le cose a gpt
with open('./chat/history_chat.txt', 'r') as file:
    for riga in file:
        contenuto_riga = riga.split("$$$")
        question = contenuto_riga[0].strip()
        answer = contenuto_riga[1].strip()

        chat.append({"question": question, "answer": answer})

# Esecuzione iterazione GPT-4
while True:
    # Leggo la domanda in input
    prompt = input(Fore.GREEN + "You: " + Fore.RESET)
    
    # Serve per uscire dalla chat
    if prompt == 'q':
        break

    # Calcolo la risposta
    response = you.Completion.create(
        prompt=prompt,
        chat=chat,
        detailed=True)

    # Stampo la risposta
    print(Fore.BLUE + "Bot:" + Fore.RESET, response.text)

    # Inserisco domanda e risposta nella history-chat
    chat.append({"question": prompt, "answer": response.text})
    # Inserisco domanda e risposta nella history-chat da scrivere poi sul file
    output += prompt + "$$$" + response.text + "\n"


# Leggo il vecchio contenuto della history-chat
old = ""
with open('./chat/history_chat.txt', 'r') as file:
    old = file.read()

# Scrivo la nuova history-chat aggiornata
with open('./chat/history_chat.txt', 'w') as file:
    file.write(old + output)
