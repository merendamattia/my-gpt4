#!/usr/bin/env python3

# Importo GPT-4
from gpt4free import you

# Importo le funzioni per l'esecuzione dell'algoritmo
from utility import *

# Serve per far terminare il programma
import sys

# Verifico se le precondizioni sono rispettate
initial_checks()

# Inizializzo la chat
chat = []

print(Fore.LIGHTBLUE_EX + "**** Welcome to GPT-4 ****" + Fore.RESET)

while True:
    # Decido cosa fare
    res = menu()

    if res == 0:
        print(Fore.LIGHTBLUE_EX + "\n**** Addios! ****" + Fore.RESET)
        # Faccio terminare il programma
        sys.exit()

    elif res == 1:
        # Scelgo su quale chat lavorare
        chat_name = choose_chat()

        # Elimino il carattere "dell'andare a capo"
        chat_name = chat_name.replace('\n', '')

        # Carico la vecchia history-chat
        upload_old_chat(chat_name, chat)

        # Esecuzione iterazione GPT-4
        output = main(chat_name, chat, you)

        # Aggiorno la history-chat
        update_chat_log(chat_name, output)

    elif res == 2:
        # Aggiungo una nuova chat
        add_chat_name()
    
    elif res == 3:
        # Elimino una chat
        delete_chat()
