import speech_recognition as sr
import serial
import time

# Funzione per inviare i comandi ad Arduino tramite Bluetooth
def invia_comando(modalita, stato):
    try:
        # Crea la connessione Bluetooth (assicurati di sostituire il tuo Bluetooth port)
        arduino = serial.Serial('/dev/rfcomm0', 9600, timeout=1)  # Puoi trovare il tuo dispositivo Bluetooth con `ls /dev/rfcomm*`
        time.sleep(2)  # Attendi che la connessione sia stabilita
        
        # Invia la modalità e lo stato come byte
        arduino.write(bytes([modalita, stato]))  # Modalità e stato devono essere valori numerici (1, 2, 3 per modalità; 0, 1 per stato)
        
        # Leggi la risposta di Arduino (opzionale)
        response = arduino.readline().decode().strip()
        print("Risposta Arduino:", response)`1111
        
        # Chiudi la connessione
        arduino.close()
    except Exception as e:
        print("Errore nella comunicazione Bluetooth:", e)

# Dizionario comandi vocali
comandi = {
    "accendi luci": lambda: invia_comando(1, 1),  # Modalità 1, Stato 1 (accendi LED)
    "spegni luci": lambda: invia_comando(1, 0),   # Modalità 1, Stato 0 (spegni LED)
    "accendi allarme": lambda: invia_comando(2, 1),  # Modalità 2, Stato 1 (accendi buzzer)
    "spegni allarme": lambda: invia_comando(2, 0),   # Modalità 2, Stato 0 (spegni buzzer)
    "imposta timer": lambda: invia_comando(3, 1),  # Modalità 3, Stato 1 (avvia cronometro)
    "spegni timer": lambda: invia_comando(3, 0),   # Modalità 3, Stato 0 (ferma cronometro)
    "fine": exit
}

# Inizializzazione del riconoscitore vocale
r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        print("Parla ora:")
        audio = r.listen(source)
        try:
            testo = r.recognize_google(audio, language='it-IT')
            testo = testo.lower().strip()  # normalizza il testo
            print("Hai detto:", testo)
            if testo in comandi:
                comandi[testo]()  # Esegui la funzione associata al comando
            elif testo == "comandi":
                print(comandi)
            else:
                print("Comando non riconosciuto.")
        except sr.UnknownValueError:
            print("Non ho capito")
