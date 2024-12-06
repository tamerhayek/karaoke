import sounddevice as sd
import signal
import sys

# Configurazione
RATE = 48000  # Frequenza di campionamento
CHANNELS = 1  # Numero di canali audio
BLOCKSIZE = 128  # Dimensione del blocco per bassa latenza

def list_input_devices():
    """Elenca solo i dispositivi di input disponibili."""
    print("\nDispositivi di INPUT disponibili:")
    devices = sd.query_devices()
    input_devices = [
        (i, device['name']) for i, device in enumerate(devices) if device['max_input_channels'] > 0
    ]
    for i, name in input_devices:
        print(f"{i}: {name}")
    return input_devices

def list_output_devices():
    """Elenca solo i dispositivi di output disponibili."""
    print("\nDispositivi di OUTPUT disponibili:")
    devices = sd.query_devices()
    output_devices = [
        (i, device['name']) for i, device in enumerate(devices) if device['max_output_channels'] > 0
    ]
    for i, name in output_devices:
        print(f"{i}: {name}")
    return output_devices

def choose_device(prompt, available_devices):
    """Permette all'utente di selezionare un dispositivo audio dalla lista."""
    while True:
        try:
            device_index = int(input(f"\n{prompt} (inserisci l'indice): "))
            if any(device_index == device[0] for device in available_devices):
                return device_index
            else:
                print("Indice non valido. Riprova.")
        except ValueError:
            print("Inserisci un numero valido. Riprova.")

def audio_callback(indata, outdata, frames, time, status):
    """Callback per il routing dell'audio."""
    if status:
        print(status)
    try:
        outdata[:] = indata  # Copia i dati catturati dall'input all'output
    except Exception as e:
        print(f"Errore nel callback audio: {e}")

def signal_handler(sig, frame):
    """Gestisce CTRL+C per terminare il programma."""
    print("\nInterruzione rilevata. Arresto del programma...")
    sys.exit(0)

# Imposta il gestore del segnale per CTRL+C
signal.signal(signal.SIGINT, signal_handler)

# Elenca i dispositivi disponibili separatamente
try:
    input_devices = list_input_devices()
    output_devices = list_output_devices()

    # Permetti all'utente di scegliere i dispositivi
    input_device = choose_device("Seleziona il dispositivo di INPUT", input_devices)
    output_device = choose_device("Seleziona il dispositivo di OUTPUT", output_devices)

    # Mostra i dispositivi selezionati
    devices = sd.query_devices()
    print(f"\nDispositivo di input selezionato: {devices[input_device]['name']}")
    print(f"Dispositivo di output selezionato: {devices[output_device]['name']}")
    print("\nInizio del monitoraggio audio... Premi CTRL+C per terminare.")

    try:
        # Avvia lo stream audio
        with sd.Stream(
            samplerate=RATE,
            channels=CHANNELS,
            blocksize=BLOCKSIZE,
            device=(input_device, output_device),  # Seleziona i dispositivi
            callback=audio_callback
        ):
            sd.sleep(-1)  # Mantiene il programma in esecuzione
    except sd.PortAudioError as e:
        print(f"Errore di dispositivo: {e}")
        print("Assicurati che i dispositivi selezionati siano collegati e riprova.")
    except Exception as e:
        print(f"Errore sconosciuto: {e}")

except KeyboardInterrupt:
    print("\nProgramma interrotto manualmente.")
    sys.exit(0)
except Exception as e:
    print(f"Errore durante la selezione dei dispositivi: {e}")
    sys.exit(1)
