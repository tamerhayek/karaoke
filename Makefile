# Nome del file principale Python
MAIN_SCRIPT = main.py

# Nome dell'applicazione
APP_NAME = Karaoke

# Cartelle
CLI_DIR = cli
GUI_DIR = gui
OUTPUT_DIR = output
DIST_DIR = dist
BUILD_DIR = build
CLI_SCRIPT = $(CLI_DIR)/$(MAIN_SCRIPT)
GUI_SCRIPT = $(GUI_DIR)/$(MAIN_SCRIPT)
CLI_OUTPUT_DIR = $(CLI_DIR)/$(OUTPUT_DIR)
GUI_OUTPUT_DIR = $(GUI_DIR)/$(OUTPUT_DIR)
CLI_DIST_DIR = $(CLI_DIR)/$(OUTPUT_DIR)/$(DIST_DIR)
GUI_DIST_DIR = $(GUI_DIR)/$(OUTPUT_DIR)/$(DIST_DIR)
CLI_BUILD_DIR = $(CLI_DIR)/$(OUTPUT_DIR)/$(BUILD_DIR)
GUI_BUILD_DIR = $(GUI_DIR)/$(OUTPUT_DIR)/$(BUILD_DIR)

# Icona (se disponibile)
ICON = icon.icns

.PHONY: cli gui clean build build-cli build-gui install

# Esegui lo script Python
cli:
	@echo "Executing the $(MAIN_SCRIPT) in CLI mode..."
	python ${CLI_DIR}/$(MAIN_SCRIPT)

gui:
	@echo "Executing the $(MAIN_SCRIPT) in GUI mode..."
	python ${GUI_DIR}/$(MAIN_SCRIPT)

# Installa le dipendenze necessarie
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Crea l'eseguibile con PyInstaller
build:
	@echo "Creazione dell'eseguibile GUI con PyInstaller..."
	pyinstaller --onefile --windowed --noconfirm --name "$(APP_NAME)" --distpath ${GUI_DIST_DIR} --workpath ${GUI_BUILD_DIR} --specpath ${GUI_OUTPUT_DIR} $(if $(ICON),--icon $(ICON)) ${GUI_SCRIPT}
	@echo "Creazione dell'eseguibile CLI con PyInstaller..."
	pyinstaller --onefile --windowed --noconfirm --name "$(APP_NAME)" --distpath ${CLI_DIST_DIR} --workpath ${CLI_BUILD_DIR} --specpath ${CLI_OUTPUT_DIR} $(if $(ICON),--icon $(ICON)) ${CLI_SCRIPT}

build-cli:
	@echo "Creazione dell'eseguibile CLI con PyInstaller..."
	pyinstaller --onefile --windowed --noconfirm --name "$(APP_NAME)" --distpath ${CLI_DIST_DIR} --workpath ${CLI_BUILD_DIR} --specpath ${CLI_OUTPUT_DIR} $(if $(ICON),--icon $(ICON)) ${CLI_SCRIPT}

build-gui:
	@echo "Creazione dell'eseguibile GUI con PyInstaller..."
	pyinstaller --onefile --windowed --noconfirm --name "$(APP_NAME)" --distpath ${GUI_DIST_DIR} --workpath ${GUI_BUILD_DIR} --specpath ${GUI_OUTPUT_DIR} $(if $(ICON),--icon $(ICON)) ${GUI_SCRIPT}

# Pulisci i file temporanei generati da PyInstaller
clean:
	@echo "Pulizia dei file generati..."
	rm -rf ${CLI_DIST_DIR} ${GUI_DIST_DIR} ${CLI_BUILD_DIR} ${GUI_BUILD_DIR} ${CLI_OUTPUT_DIR}/*.spec ${GUI_OUTPUT_DIR}/*.spec
	@echo "Pulizia completata."
