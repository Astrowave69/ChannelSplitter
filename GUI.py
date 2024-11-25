import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import soundfile as sf
import os
import ctypes

# Function to handle audio processing
def process_audio():
    try:
        # Open file dialog to select audio file
        audio_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")]
        )
        if not audio_path:
            return

        # Load the stereo audio file (keeping the stereo channels intact)
        y, sr = librosa.load(audio_path, sr=None, mono=False)

        if len(y.shape) != 2 or y.shape[0] != 2:
            messagebox.showerror("Error", "Selected audio file is not stereo.")
            return

        # Separate Mid (M) and Side (S) channels
        left_channel = y[0]
        right_channel = y[1]
        mid_channel = (left_channel + right_channel) / 2
        side_channel = (left_channel - right_channel) / 2

        # Select folder to save the files
        save_folder = filedialog.askdirectory()
        if not save_folder:
            return

        # Save Mid and Side channels as separate files
        mid_path = os.path.join(save_folder, "mid_channel.wav")
        side_path = os.path.join(save_folder, "side_channel.wav")
        sf.write(mid_path, mid_channel, sr)
        sf.write(side_path, side_channel, sr)

        # Notify the user
        messagebox.showinfo("Success", f"Files saved:\n{mid_path}\n{side_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# Function to apply dark mode
def set_dark_mode(window):
    window.configure(bg="#2e2e2e")
    style = {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "font": ("Segoe UI", 12),
        "relief": "flat",
        "highlightthickness": 0,
        "borderwidth": 0,
    }
    return style

# Function to customize the title bar and match the app color
def set_custom_title_bar(window):
    # Remove the default title bar
    window.overrideredirect(True)

    # Extend the client area (to blend the title bar with the app background)
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(
        hwnd, ctypes.byref(ctypes.c_int(-1))
    )

    # Add a custom title bar
    def on_close():
        window.destroy()

    title_bar = tk.Frame(window, bg="#2e2e2e", height=30, relief="flat")
    title_bar.pack(side="top", fill="x")

    title_label = tk.Label(
        title_bar,
        text="Stereo to Mid-Side Converter",
        bg="#2e2e2e",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        anchor="w",
        padx=10,
    )
    title_label.pack(side="left", fill="y")

    close_button = tk.Button(
        title_bar,
        text="X",
        bg="#2e2e2e",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        command=on_close,
    )
    close_button.pack(side="right", padx=5)

    # Allow dragging the window by the title bar
    def start_move(event):
        window.x = event.x
        window.y = event.y

    def on_drag(event):
        x = window.winfo_x() + (event.x - window.x)
        y = window.winfo_y() + (event.y - window.y)
        window.geometry(f"+{x}+{y}")

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", on_drag)

# Create the main GUI window
root = tk.Tk()
root.geometry("500x300")
root.resizable(False, False)

# Apply dark mode
style = set_dark_mode(root)

# Set custom title bar
set_custom_title_bar(root)

# Add widgets
main_frame = tk.Frame(root, bg=style["bg"])
main_frame.pack(expand=True, fill="both", padx=10, pady=10)

info_label = tk.Label(
    main_frame, text="Convert stereo audio to mid-side channels.\nClick the button to start.", bg=style["bg"], fg=style["fg"], font=("Segoe UI", 10)
)
info_label.pack(pady=10)

convert_button = tk.Button(main_frame, text="Select and Convert Audio", command=process_audio, bg="#4caf50", fg="white", font=("Segoe UI", 12), relief="flat")
convert_button.pack(pady=20)

# Run the app
root.mainloop()
