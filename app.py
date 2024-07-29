import tkinter as tk
import customtkinter as ctk
from threading import Thread
from datetime import timedelta
from PIL import Image, ImageTk
from CTkListbox import CTkListbox
import re, time, os, pygame, glob
from tkinter import filedialog, Label, END
from mutagen.id3 import ID3, ID3NoHeaderError

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Initialization of pygame with optimal settings
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

# Store current position of the music
current_pos = 0
paused = False
selected_folder_path = "C:/Users/oaddo/Music"


# Functions
class StaticPanel(ctk.CTkFrame):
    def __init__(self, parent, width):
        super().__init__(master=parent)
        self.width = width
        self.parent = parent
        self.place(relx=0, rely=0, relwidth=self.width, relheight=1)
        self.configure(fg_color="#2B2B2B")

        # Adding Home button
        self.home_button_image = tk.PhotoImage(
            file="mycollection\\png\\home.png"
        ).subsample(1, 1)
        self.home_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.home_button_image,
            width=40,
            height=40,
            command=self.parent.show_home,
        )
        self.home_button.place(relx=0.5, rely=0.1, anchor="center")

        # Adding Songs button
        self.songs_button_image = tk.PhotoImage(
            file="mycollection\\png\\003-musical-note-1.png"
        ).subsample(1, 1)
        self.songs_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.songs_button_image,
            width=40,
            height=40,
            command=self.parent.show_songs,
        )
        self.songs_button.place(relx=0.5, rely=0.2, anchor="center")

        # Adding Favorites button
        self.favorites_button_image = tk.PhotoImage(
            file="mycollection\\png\\favourite.png"
        ).subsample(1, 1)
        self.favorites_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.favorites_button_image,
            width=40,
            height=40,
            command=self.parent.show_favorites,
        )
        self.favorites_button.place(relx=0.5, rely=0.3, anchor="center")


class Home(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent.main_frame)
        self.parent = parent
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Initialize UI components
        self.song_name_label = ctk.CTkLabel(self, text="", font=("Arial", 20))
        self.song_name_label.place(relx=0.5, rely=0.01, anchor="n")

        self.background_label = tk.Label(self)
        self.background_label.place(relx=0.5, rely=0.4, anchor="center")

        self.progress_bar = ctk.CTkSlider(self, orientation="horizontal", height=8, width=250,progress_color="green")
        self.progress_bar.set(0)
        self.progress_bar.place(relx=0.5, rely=0.7, anchor="center")

        self.time_display = ctk.CTkLabel(self, text="--:-- / --:--", font=("Arial", 12))
        self.time_display.place(relx=0.5, rely=0.75, anchor="center")
        
        self.favorites_button_image = tk.PhotoImage(
            file="mycollection\\png\\favourite.png"
        ).subsample(1, 1)
        self.favorites_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.favorites_button_image,
            width=8,
            height=8,
            command=self.parent.show_favorites,
        )
        self.favorites_button.place(relx=0.75, rely=0.75, anchor="center")

        # Get the list of songs
        self.songs_list = self.parent.songs()
        self.song_names = list(self.songs_list.keys())
        self.current_index = 0

        # Set up the first song
        self.update_song()

        # Add control buttons
        self.add_control_buttons()

        # Start the progress update loop
        self.update_progress()

    def update_song(self):
        # Get the current song details
        self.current_song = self.song_names[self.current_index]
        self.playing_song = self.songs_list[self.current_song]["path"]
        self.current_song_name = self.current_song
        self.current_song_image_path = f"assets/images/{self.current_song}.jpg"

        # Load and display the background image
        if os.path.isfile(self.current_song_image_path):
            self.current_song_image = Image.open(self.current_song_image_path)
            self.current_song_image = self.current_song_image.resize(
                (400, 400), Image.LANCZOS
            )
            self.current_song_image_tk = ImageTk.PhotoImage(self.current_song_image)
            self.background_label.configure(image=self.current_song_image_tk)
            self.background_label.image = self.current_song_image_tk
        else:
            self.background_label.configure(image="")  # Clear image if not found

        # Display the song name
        self.song_name_label.configure(text=self.current_song_name)

        # Play the song
        self.parent.play_song(self.playing_song)

    def add_control_buttons(self):
        # Adding backward button
        self.backward_button_image = tk.PhotoImage(
            file="mycollection\\png\\014-backward-track.png"
        ).subsample(1, 1)
        self.backward_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.backward_button_image,
            command=self.parent.backward,
            width=50,
            height=50,
        )
        self.backward_button.place(relx=0.25, rely=0.9, anchor="center")

        # Adding skip back button
        self.skip_back_button_image = tk.PhotoImage(
            file="mycollection\\png\\015-backward.png"
        ).subsample(1, 1)
        self.skip_back_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.skip_back_button_image,
            command=self.parent.skip_back,
            width=50,
            height=50,
        )
        self.skip_back_button.place(relx=0.35, rely=0.9, anchor="center")

        # Adding play button
        self.play_button_image = tk.PhotoImage(
            file="mycollection\\png\\001-play-button-arrowhead.png"
        ).subsample(1, 1)
        self.pause_button_image = tk.PhotoImage(
            file="mycollection\\png\\004-pause-button.png"
        ).subsample(1, 1)

        self.play_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.play_button_image,
            command=self.parent.play_pause_song,
            width=50,
            height=50,
        )
        self.play_button.place(relx=0.5, rely=0.9, anchor="center")

        # Adding skip forward button
        self.skip_forward_button_image = tk.PhotoImage(
            file="mycollection\\png\\013-skip-button.png"
        ).subsample(1, 1)
        self.skip_forward_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.skip_forward_button_image,
            command=self.parent.skip_forward,
            width=50,
            height=50,
        )
        self.skip_forward_button.place(relx=0.65, rely=0.9, anchor="center")

        # Adding next button
        self.next_button_image = tk.PhotoImage(
            file="mycollection\\png\\012-next.png"
        ).subsample(1, 1)
        self.next_button = ctk.CTkButton(
            master=self,
            text="",
            image=self.next_button_image,
            command=self.next_song,
            width=50,
            height=50,
        )
        self.next_button.place(relx=0.75, rely=0.9, anchor="center")

    def next_song(self):
        # Move to the next song
        self.current_index = (self.current_index + 1) % len(self.song_names)
        self.progress_bar.set(0)
        self.update_song()

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            # Update the progress bar and time display
            current_time = pygame.mixer.music.get_pos() / 1000
            song_length = pygame.mixer.Sound(self.playing_song).get_length()
            progress = current_time / song_length

            # Update progress bar
            self.progress_bar.set(progress)

            # Update time display
            current_time_formatted = str(timedelta(seconds=int(current_time)))
            song_length_formatted = str(timedelta(seconds=int(song_length)))
            self.time_display.configure(
                text=f"{current_time_formatted} / {song_length_formatted}"
            )

            # Schedule the next update
            self.after(1000, self.update_progress)
        else:
            # If the song has ended, automatically play the next song
            self.next_song()


class SongsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent.main_frame)
        self.parent = parent

        # Create a canvas and scrollbar
        self.canvas = ctk.CTkCanvas(self, bg="#2B2B2B")
        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )

        # Pack the scrollbar to the right and the canvas to the left
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas
        self.inner_frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Update the scroll region when the inner_frame is resized
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Bind mouse wheel scrolling to the canvas
        self.bind_mouse_wheel_scrolling()

        # Load images and names
        self.load_images_and_names()

    def load_songs(self):
        self.songs_list = self.parent.songs()
        self.song_names = list(self.songs_list.keys())
        return self.song_names

    def get_first_song(self):
        if self.songs_list:
            return self.songs_list[self.song_names[0]]
        return None

    def load_images_and_names(self):
        # Load images
        image_folder = "assets/images"
        images = os.listdir(image_folder)

        # Constants for image dimensions and padding
        num_images_per_row = 5
        image_width = 127
        image_height = 127
        padding = 20

        # Calculate the total width needed for the inner_frame
        total_width = (image_width + padding) * num_images_per_row - padding
        self.inner_frame.configure(width=total_width)

        # Create a grid layout for images and names
        for i, song_name in enumerate(self.load_songs()):
            image_path = os.path.join(image_folder, f"{self.load_songs()[i]}.jpg")
            if not os.path.isfile(image_path):
                continue

            img = Image.open(image_path)
            img = img.resize(
                (image_width, image_height)
            )  # Resize image to fit in the frame
            img_tk = ImageTk.PhotoImage(img)

            # Create a frame for the image and description
            image_frame = ctk.CTkFrame(
                self.inner_frame,
                width=image_width,
                height=image_height + 20,  # Extra space for description
                corner_radius=60,
                fg_color="#2B2B2B",  # Background color for the image frame
            )
            row = i // num_images_per_row
            column = i % num_images_per_row
            image_frame.grid(
                row=row, column=column, padx=padding // 2, pady=padding // 2
            )

            # Create and place image label
            image_label = ctk.CTkLabel(image_frame, text="", image=img_tk)
            image_label.pack(pady=(0, 10))  # Leave space for description at the bottom

            # Create and place name label
            name_label = ctk.CTkLabel(image_frame, text=song_name, anchor="center")
            name_label.pack(side="bottom", fill="x")

            # Store a reference to the image to prevent garbage collection
            image_label.image = img_tk

        # Configure row and column weights to make them expand
        for col in range(num_images_per_row):
            self.inner_frame.grid_columnconfigure(col, weight=1)
        self.inner_frame.grid_rowconfigure(row, weight=1)

    def bind_mouse_wheel_scrolling(self):
        # Bind mouse wheel scroll to canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        # Scroll canvas based on the mouse wheel movement
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class FavoritesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent.main_frame)
        self.parent = parent
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.favorites_listbox = tk.Listbox(self, height=400, width=300)
        self.favorites_listbox.place(relx=0.5, rely=0.5, anchor="center")

        for song_name in self.parent.favorites().keys():
            self.favorites_listbox.insert(tk.END, song_name)

        self.favorites_listbox.bind("<<ListboxSelect>>", self.on_favorite_select)

    def on_favorite_select(self, event):
        selected_favorite_name = self.favorites_listbox.get(
            self.favorites_listbox.curselection()
        )
        self.parent.current_song = selected_favorite_name
        self.parent.play_song(self.parent.songs()[selected_favorite_name]["path"])


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (640 / 2))
        y = int((screen_height / 2) - (480 / 2))

        self.geometry(f"+{x}+{y}")
        self.title("Phonoid")
        self.geometry("740x580")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.sidebar = StaticPanel(self, width=0.2)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

        icon_path = os.path.join("mycollection", "png", "011-music.png")
        self.iconphoto(True, tk.PhotoImage(file=icon_path))

        self.after(100, lambda: self.iconbitmap("mycollection\\png\\011-music.png"))

        # Initialize songs and favorites
        self.songs_data = {}
        self.favorites_data = {}

        # Load songs data
        self.load_songs()

        self.home_view = Home(self)
        self.songs_view = SongsView(self)
        self.favorites_view = FavoritesView(self)

        self.show_home()

    def on_closing(self):
        pygame.mixer.music.stop()
        self.destroy()

    def show_home(self):
        self.songs_view.place_forget()
        self.favorites_view.place_forget()
        self.home_view.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_songs(self):
        self.home_view.place_forget()
        self.favorites_view.place_forget()
        self.songs_view.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_favorites(self):
        self.home_view.place_forget()
        self.songs_view.place_forget()
        self.favorites_view.place(relx=0, rely=0, relwidth=1, relheight=1)

    def load_songs(self):
        if selected_folder_path:
            for file_path in glob.glob(f"{selected_folder_path}/*.mp3"):
                try:
                    audio = ID3(file_path)
                    title = audio.get("TIT2", os.path.basename(file_path)).text[0]
                    self.songs_data[title] = {"path": file_path}
                except ID3NoHeaderError:
                    print(f"Skipping file: {file_path}, no ID3 header found.")

    def songs(self):
        return self.songs_data

    def favorites(self):
        return self.favorites_data

    def play_song(self, song_path):
        global paused, current_pos

        if paused:
            pygame.mixer.music.unpause()
            paused = False
            self.home_view.play_button.configure(
                image=self.home_view.pause_button_image
            )
        else:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(loops=0, start=current_pos)

    def play_pause_song(self):
        global paused, current_pos

        if pygame.mixer.music.get_busy():
            if paused:
                pygame.mixer.music.unpause()
                paused = False
                self.home_view.play_button.configure(
                    image=self.home_view.pause_button_image
                )
            else:
                pygame.mixer.music.pause()
                paused = True
                self.home_view.play_button.configure(
                    image=self.home_view.play_button_image
                )
        else:
            self.play_song(self.home_view.playing_song)

    def backward(self):
        global current_pos
        current_pos = 0
        self.play_song(self.home_view.playing_song)

    def skip_back(self):
        global current_pos
        current_pos = max(current_pos - 10, 0)
        self.play_song(self.home_view.playing_song)

    def skip_forward(self):
        global current_pos
        song_length = pygame.mixer.Sound(self.home_view.playing_song).get_length()
        current_pos = min(current_pos + 10, song_length)
        self.play_song(self.home_view.playing_song)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
