# karaoke

![Logo Karaoke](./static/logo.webp)

Stream your input device into your output device.

This repository is using venv for development.

Create a virtual environment named venv:

```bash
python3 -m venv venv
```

Use the following command to activate venv:

```bash
source venv/bin/activate
```

Use the following command to deactivate venv:

```bash
deactivate
```

Use the following command to install dependencies:

```bash
pip install -r requirements.txt
```

Use the following command to run the cli app:

```bash
python ./cli/main.py
```

Use the following command to run the gui app:

```bash
python ./gui/main.py
```

Create a portable executable for cli app:

```bash
pyinstaller --onefile --windowed --name "Karaoke" --distpath ./cli/output/dist --workpath ./cli/output/build --specpath ./cli/output --icon "icon.icns" --noconfirm ./cli/main.py
```

Create a portable executable for gui app:

```bash
pyinstaller --onefile --windowed --name "Karaoke" --distpath ./gui/output/dist --workpath ./gui/output/build --specpath ./gui/output --icon "icon.icns" --noconfirm ./gui/main.py
```

