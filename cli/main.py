import sounddevice as sd
import signal
import sys

# Configurazione
RATE = 48000  # Frequenza di campionamento
CHANNELS = 1  # Numero di canali audio
BLOCKSIZE = 128  # Dimensione del blocco per bassa latenza

def list_devices():
    """Elenca i dispositivi disponibili."""
    devices = sd.query_devices()
    print("\nDispositivi audio disponibili:")
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']} ({'Input' if device['max_input_channels'] > 0 else 'Output'})")
    return devices

def choose_device(prompt, mode):
    """Permette all'utente di selezionare un dispositivo audio."""
    while True:
        try:
            device_index = int(input(f"\n{prompt} (inserisci l'indice): "))
            device = sd.query_devices(device_index)
            if mode == 'input' and device['max_input_channels'] > 0:
                return device_index
            elif mode == 'output' and device['max_output_channels'] > 0:
                return device_index
            else:
                print(f"Il dispositivo selezionato non supporta {mode}. Riprova.")
        except (ValueError, IndexError):
            print("Indice non valido. Riprova.")

def audio_callback(indata, outdata, frames, time, status):
    """Callback per il routing dell'audio."""
    if status:
        print(status)
    outdata[:] = indata  # Copia i dati catturati dall'input all'output

def signal_handler(sig, frame):
    """Gestisce CTRL+C per terminare il programma."""
    print("\nInterruzione rilevata. Arresto del programma...")
    sys.exit(0)

# Imposta il gestore del segnale per CTRL+C
signal.signal(signal.SIGINT, signal_handler)

# Elenca i dispositivi disponibili e permetti all'utente di scegliere
devices = list_devices()
input_device = choose_device("Seleziona il dispositivo di INPUT", "input")
output_device = choose_device("Seleziona il dispositivo di OUTPUT", "output")

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
except Exception as e:
    print(f"Errore: {e}")
    sys.exit(1)
