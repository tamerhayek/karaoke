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

Use the following command to run the app:

```bash
python main.py
```

Create a portable executable:

```bash
pyinstaller --onefile --windowed --name "Karaoke" --icon "./static/icon.icns" main.py
```

