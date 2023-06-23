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

while True:
    # Decido cosa fare
    res = menu()

    if res == 0:
        # Faccio terminare il programma
        sys.exit()

    elif res == 1:
        # Scelgo su quale chat lavorare
        chat_name = str(choose_chat())
        # print("chat_name: " + chat_name)

        # Carico la vecchia history-chat
        upload_old_chat(chat_name, chat)

        # Esecuzione iterazione GPT-4
        output = main(chat_name, chat, you)

        # Aggiorno la history-chat
        update_chat_log(chat_name, output)

    elif res == 2:
        # Aggiungo una nuova chat
        add_chat_name()
