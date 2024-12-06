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
make install
```

Use the following command to run the cli app:

```bash
make
```

or

```bash
make cli
```

Use the following command to run the gui app:

```bash
make gui
```

Create a portable executable for cli app:

```bash
make build-cli
```

Create a portable executable for gui app:

```bash
make build-gui
```

Create a portable executable for cli and gui app:

```bash
make build
```
