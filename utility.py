# Vado a verificare se la cartella chat e se il file history_chat esistono già
# Se non esistono li creo
def initial_checks():
    import os
    if not os.path.exists("chat"):
        os.makedirs("chat")
    if not os.path.isfile('./chat/history_chat.txt'):
        with open('./chat/history_chat.txt', 'w') as file:
            file.write("$$$question: My history-chat\n$$$answer: by @merendamattia")

# ------------------------------------------------------------------------------------------

# Carico la vecchia history-chat
def upload_old_chat(chat):
    with open('./chat/history_chat.txt', 'r') as file:
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
def main(chat, Fore, you):
    # Mi serve per aggiornare poi la history-chat
    output = "" 

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
        
        # Mi copio la risposta
        answer = response.text

        # Stampo la risposta
        print(Fore.BLUE + "Bot:" + Fore.RESET, answer)

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
def update_chat_log(output):
    # Leggo il vecchio contenuto della history-chat
    old = ""
    with open('./chat/history_chat.txt', 'r') as file:
        old = file.read()

    # Scrivo la nuova history-chat aggiornata
    with open('./chat/history_chat.txt', 'w') as file:
        file.write(old + output)
