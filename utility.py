# Serve per stampare le scritte colorate
from colorama import init, Fore, Back, Style
init()

import os
# Vado a verificare se la cartella chat e se il file history_chat esistono già
# Se non esistono li creo
def initial_checks():
    if not os.path.exists("chat"):
        os.makedirs("chat")
    
    path = './chat/chats_name.txt'

    if not os.path.isfile(path):
        with open(path, 'w') as file:
            file.write("landing_chat")

# ------------------------------------------------------------------------------------------

# Carico la vecchia history-chat
def upload_old_chat(chat_name, chat):
    path = "./chat/" + chat_name + ".txt"
    
    if not os.path.isfile(path):
        with open(path, 'w') as file:
            file.write("$$$init: My history-chat " + chat_name + " by @merendamattia\n")
    
    with open(path, 'r') as file:
        question = ""
        answer = ""
        for line in file:
            if line.startswith("$$$question:"):
                # Se la riga inizia con "$$$question:" allora memorizziamo la domanda
                question = line[len("$$$question:"):].strip()
            elif line.startswith("$$$answer:"):
                # Se la riga inizia con "$$$answer:" allora memorizziamo la risposta
                answer += line[len("$$$answer:"):].strip()
            if question and answer:
                # Se abbiamo sia la domanda che la risposta, allora aggiungiamo la coppia alla lista e resettiamo le variabili
                answer = answer.replace("${$endl}", '\n')
                answer = answer.replace("${$tab}", '\t')
                chat.append({"question": question, "answer": answer})
                question = ""
                answer = ""
        # Se è presente un'ultima coppia domanda-risposta, l'aggiungiamo all'array
        if question and answer:
            chat.append({"question": question, "answer": answer})

# ------------------------------------------------------------------------------------------

# Esecuzione iterazione GPT-4
def main(chat_name, chat, you):
    # Messaggio iniziale
    print(Fore.RED + "#chatbot model GPT-4 (`q`: to quit)" + Fore.MAGENTA + " - Chat: " + chat_name + Fore.RESET)
    # print(Fore.MAGENTA + "Chat: " + chat_name + Fore.RESET)
    
    # Mi serve per aggiornare poi la history-chat
    output = "" 

    while True:
        # Leggo la domanda in input
        prompt = input(Fore.GREEN + "You - " + chat_name + ": " + Fore.RESET)
        
        # Serve per uscire dalla chat
        if prompt == 'q':
            break

        # Calcolo la risposta
        response = you.Completion.create(
            prompt=prompt,
            chat=chat,
            detailed=True)
        
        # Mi copio la risposta
        answer = response.text

        # Stampo la risposta
        print(Fore.BLUE + "Bot - " + chat_name + ": " + Fore.RESET, answer)

        # Inserisco domanda e risposta nella history-chat
        chat.append({"question": prompt, "answer": response.text})

        # Preparo la risposta per essere scritta su file
        answer_log = answer.replace('\n', "${$endl}")
        answer_log = answer_log.replace('\t', "${$tab}")

        # Inserisco domanda e risposta nella history-chat da scrivere poi sul file
        output += "$$$question: " + prompt + "\n"
        output += "$$$answer: " + answer_log + "\n"
    return output

# ------------------------------------------------------------------------------------------

# Aggiorno la history-chat
def update_chat_log(chat_name, output):
    path = "./chat/" + chat_name + ".txt"
    # Leggo il vecchio contenuto della history-chat
    old = ""
    with open(path, 'r') as file:
        old = file.read()

    # Scrivo la nuova history-chat aggiornata
    with open(path, 'w') as file:
        file.write(old + output)

# ------------------------------------------------------------------------------------------

# Permette di scegliere quale chat utilizzare
def choose_chat():
    path = './chat/chats_name.txt'

    if not os.path.isfile(path):
        with open(path, 'w') as file:
            file.write("landing_chat")
        return 'landing_chat'
    
    while True:
        with open(path, 'r') as file:
            c = 0 # conta le righe

            output = ""
            
            for line in file:
                line = line.replace('\n', '')
                c = c + 1
                output += str(c) + '. ' + line
            
            if c > 1:
                print(Fore.MAGENTA + "Scegli la chat:")
                print(output)
                res = int(input(Fore.RESET + "Scelta: "))
            else:
                res = 1

        with open(path, 'r') as file:
            c = 0 # conta le righe
            for line in file:
                c = c + 1
                if c == res:
                    return str(line)
    
# ------------------------------------------------------------------------------------------

# Menu
def menu():
    res = -1
    while res < 0 or res > 3:
        print(Fore.YELLOW + "Menù GPT-4")
        print("1. Avvia chatbot")
        print("2. Crea nuova chat")
        print("3. Elimina chat")
        print("0. Terminazione programma" + Fore.RESET)
        res = int(input("Scelta: "))
    return res

# ------------------------------------------------------------------------------------------

# Aggiungo una nuova chat
def add_chat_name():
    new_name = input("Inserisci il nome della nuova chat: ")

    path = "./chat/chats_name.txt"

    # Se non esiste l'elenco delle chat lo creo vuoto
    if not os.path.isfile(path):
        with open(path, 'w') as file:
            file.write(new_name)
    else:
        # Leggo il vecchio contenuto della chats_name
        old = ""
        with open(path, 'r') as file:
            old = file.read()

        new = old + "\n" + new_name

        # Scrivo la nuova chats_name aggiornata
        with open(path, 'w') as file:
            file.write(new)

# ------------------------------------------------------------------------------------------

# Elimino una chat
def delete_chat():
    path = './chat/chats_name.txt'

    while True:
        print(Fore.RED + "Scegli la chat da eliminare:")
        
        with open(path, 'r') as file:
            c = 0 # conta le righe
            
            for line in file:
                line = line.replace('\n', '')
                c = c + 1
                print(str(c) + '. ' + line)

            # print(Fore.RESET)
            res = int(input(Fore.RESET + "Scelta: "))

        new_chats = ""
        old_chat = ""

        with open(path, 'r') as file:
            c = 0 # conta le righe
            for line in file:
                c = c + 1
                if c != res:
                    new_chats += line
                else:
                    old_chat = line
        
        # Scrivo il nuovo elenco delle chat
        with open(path, 'w') as file:
            file.write(new_chats)