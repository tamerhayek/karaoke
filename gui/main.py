import sys
import sounddevice as sd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

# Configurazione
RATE = 48000  # Frequenza di campionamento
CHANNELS = 1  # Numero di canali audio
BLOCKSIZE = 128  # Dimensione del blocco per bassa latenza


class AudioStreamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Karaoke by Tamer")
        self.setGeometry(100, 100, 400, 300)

        # Variabili per il flusso audio
        self.stream = None
        self.input_device_index = None
        self.output_device_index = None

        # Costruzione dell'interfaccia
        self.init_ui()

    def init_ui(self):
        """Inizializza la GUI."""
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Etichetta di benvenuto
        self.label = QLabel("Benvenuto in Karaoke by Tamer")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Menu a tendina per i dispositivi di input
        self.input_label = QLabel("Seleziona il dispositivo di INPUT:")
        layout.addWidget(self.input_label)
        self.input_combo = QComboBox()
        self.input_devices = self.list_input_devices()
        self.input_combo.addItems([name for _, name in self.input_devices])
        layout.addWidget(self.input_combo)

        # Menu a tendina per i dispositivi di output
        self.output_label = QLabel("Seleziona il dispositivo di OUTPUT:")
        layout.addWidget(self.output_label)
        self.output_combo = QComboBox()
        self.output_devices = self.list_output_devices()
        self.output_combo.addItems([name for _, name in self.output_devices])
        layout.addWidget(self.output_combo)

        # Pulsante per avviare lo streaming
        self.start_button = QPushButton("Avvia Streaming")
        self.start_button.clicked.connect(self.start_streaming)
        layout.addWidget(self.start_button)

        # Pulsante per fermare lo streaming
        self.stop_button = QPushButton("Ferma Streaming")
        self.stop_button.clicked.connect(self.stop_streaming)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        # Configura il layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def list_input_devices(self):
        """Elenca i dispositivi di input."""
        devices = sd.query_devices()
        return [(i, device['name']) for i, device in enumerate(devices) if device['max_input_channels'] > 0]

    def list_output_devices(self):
        """Elenca i dispositivi di output."""
        devices = sd.query_devices()
        return [(i, device['name']) for i, device in enumerate(devices) if device['max_output_channels'] > 0]

    def start_streaming(self):
        """Avvia lo streaming audio."""
        try:
            # Ottieni l'indice dei dispositivi selezionati
            self.input_device_index = self.input_devices[self.input_combo.currentIndex()][0]
            self.output_device_index = self.output_devices[self.output_combo.currentIndex()][0]

            # Avvia il flusso audio
            self.stream = sd.Stream(
                samplerate=RATE,
                channels=CHANNELS,
                blocksize=BLOCKSIZE,
                device=(self.input_device_index, self.output_device_index),
                callback=self.audio_callback
            )
            self.stream.start()

            # Aggiorna lo stato della GUI
            self.label.setText("Streaming in corso...")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante lo streaming audio:\n{e}")

    def stop_streaming(self):
        """Ferma lo streaming audio."""
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None

            # Aggiorna lo stato della GUI
            self.label.setText("Streaming fermato.")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore durante l'arresto dello streaming:\n{e}")

    @staticmethod
    def audio_callback(indata, outdata, frames, time, status):
        """Callback per copiare l'audio dall'input all'output."""
        if status:
            print(f"Status: {status}")
        outdata[:] = indata


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioStreamerApp()
    window.show()
    sys.exit(app.exec())
