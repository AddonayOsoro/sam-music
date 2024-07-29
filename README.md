# Sam's Music Player

This is a custom music player application built with Tkinter and CustomTkinter, using the Pygame library for audio playback. The application supports playing, pausing, and navigating through songs, with a dynamic UI that updates based on the current song.

## Features

- Home view with song and album artwork display
- Songs view with a list of all available songs
- Playback controls (play/pause, skip, backward)
- Progress bar and time display

## Prerequisites

- Python 3.7 or higher
- Git

## Installation

Follow these steps to set up and run the application:

### 1. Clone the Repository

```bash
git clone https://github.com/AddonayOsoro/sam-music.git
cd sam-music
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies. You can create one using `venv`:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment:

  ```bash
  .venv\Scripts\activate
  ```

### 4. Install Dependencies

Install the required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Run the Application

Run the application using:

```bash
python app.py
```

Make sure you have all your songs in the `songs` directory and corresponding images in the `assets/images` directory. The songs should be in MP3 format and images should be in JPG format with the same name as the songs.

### Notes

- The `requirements.txt` file should include all the necessary packages for the application. If it's not present, you can create it using the following command:

  ```bash
  pip freeze > requirements.txt
  ```

- Ensure that you have the `songs` and `assets/images` directories populated with the required files.

## Contributing

Feel free to open issues or create pull requests if you find any bugs or want to add new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Sample `requirements.txt` File

Make sure you have a `requirements.txt` file with the necessary dependencies. Here is a sample:

```
pygame==2.1.2
Pillow==9.1.1
mutagen==1.45.1
customtkinter==5.1.2
CTkListbox==0.2.0
```