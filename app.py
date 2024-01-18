import tkinter as tk
from tkinter import ttk, filedialog
import vlc
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Beautiful Video Player")
        
        icon_image = tk.PhotoImage(file='images/appicon.png')  # Replace 'path_to_your_image.png' with your PNG image file

        # Set the icon for the window
        self.master.iconphoto(True, icon_image)

        # Create a VLC instance
        self.instance = vlc.Instance("--no-xlib")

        # Create a media player
        self.media_player = self.instance.media_player_new()

        # Create a Tkinter canvas for the video
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill="both", expand=True)

        # Store references to icons
        self.play_icon = ImageTk.PhotoImage(Image.open("images/play.png").resize((24, 24)))
        self.pause_icon = ImageTk.PhotoImage(Image.open("images/pause.png").resize((24, 24)))
        self.stop_icon = ImageTk.PhotoImage(Image.open("images/stop.png").resize((24, 24)))
        self.open_icon = ImageTk.PhotoImage(Image.open("images/open.png").resize((24, 24)))

        # Create playback controls
        self.create_controls()

        # Create time slider, fullscreen toggle, and playback speed control
        self.create_extra_controls()

    def create_controls(self):
        # Create a frame for controls
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side="bottom", pady=10)

        # Create buttons with icons
        play_button = ttk.Button(control_frame, image=self.play_icon, command=self.play)
        pause_button = ttk.Button(control_frame, image=self.pause_icon, command=self.pause)
        stop_button = ttk.Button(control_frame, image=self.stop_icon, command=self.stop)
        open_button = ttk.Button(control_frame, image=self.open_icon, command=self.open_file)

        # Grid layout for buttons
        play_button.grid(row=0, column=0, padx=5)
        pause_button.grid(row=0, column=1, padx=5)
        stop_button.grid(row=0, column=2, padx=5)
        open_button.grid(row=0, column=3, padx=5)

        # Create a volume control slider
        volume_label = ttk.Label(control_frame, text="Volume:")
        volume_slider = ttk.Scale(control_frame, from_=0, to=100, orient="horizontal", command=self.set_volume)
        volume_slider.set(50)  # Default volume

        # Grid layout for volume control
        volume_label.grid(row=0, column=4, padx=5)
        volume_slider.grid(row=0, column=5, padx=5)

    def create_extra_controls(self):
        # Create a frame for additional controls
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side="bottom", pady=10)

        # Create a time slider for video progress
        self.time_slider = ttk.Scale(control_frame, from_=0, to=100, orient="horizontal", command=self.set_time)
        self.time_slider.set(0)  # Default position
        self.time_slider.grid(row=0, column=0, columnspan=4, padx=5)

        # Bind 'F' key to toggle fullscreen mode
        self.master.bind("<F>", self.toggle_fullscreen)

        # Playback speed control dropdown
        playback_speeds = [0,0.5,1.0, 1.5, 2.0]  # Adjust as needed   
        self.speed_var = tk.StringVar(self.master)
        self.speed_var.set(playback_speeds[1])  # Default speed
        speed_dropdown = ttk.OptionMenu(control_frame, self.speed_var, *playback_speeds, command=self.set_speed)
        speed_dropdown.grid(row=1, column=0, columnspan=4, padx=5)

    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv,*.avi,*.wmv")])
        if file_path:
            self.play_video(file_path)

    def play_video(self, file_path):
        media = self.instance.media_new(file_path)
        self.media_player.set_media(media)
        self.media_player.set_hwnd(self.get_handle())
        self.media_player.play()

    def get_handle(self):
        return self.canvas.winfo_id()

    def set_volume(self, value):
        volume = int(float(value))
        self.media_player.audio_set_volume(volume)

    def set_time(self, value):
        # Set the playback time based on the slider position
        time_position = int(float(value) * self.media_player.get_length() / 1000)
        self.media_player.set_time(time_position * 1000)

    def toggle_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen"))

    def set_speed(self, value):
        # Set the playback speed
        speed = float(value)
        self.media_player.set_rate(speed)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
