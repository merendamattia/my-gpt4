# Importo GPT-4
from gpt4free import you

# Importo le funzioni per l'esecuzione dell'algoritmo
from utility import *

# Serve per stampare le scritte colorate
from colorama import init, Fore, Back, Style
init()

# Verifico se le precondizioni sono rispettate
initial_checks()

# Messaggio iniziale
print(Fore.RED + "#chatbot model GPT-4 (`q`: to quit)" + Fore.RESET)

# Inizializzo la chat
chat = []

# Carico la vecchia history-chat
upload_old_chat(chat)

# Esecuzione iterazione GPT-4
output = main(chat, Fore, you)

# Aggiorno la history-chat
update_chat_log(output)