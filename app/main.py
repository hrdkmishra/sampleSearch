from web_scrapper import scrape_samples , extract_and_change_case
import asyncio
from shazamio import Shazam, Serialize
import threading
import tkinter as tk
from tkinter import ttk
import os
import soundcard as sc
import soundfile as sf
from pydub import AudioSegment
from PIL import Image, ImageTk
import sv_ttk
import requests
import shutil
import time


class Shazaming:
    @classmethod
    async def recognize_audio_shazam(cls):
        shazam = Shazam()
        try:
            out = await shazam.recognize_song("audio/out.ogg")
            serialized = Serialize.full_track(out)
            result = {"title": serialized.track.title, "subtitle": serialized.track.subtitle}
            return result
        except Exception as e:
            print("Error during Shazam identification:", e)
            return None

    @classmethod
    def snippets(cls):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(cls.recognize_audio_shazam())

class SampleShazaming:
        
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")

        self.record_button = ttk.Button(self.root, text="Start Recording", command=self.start_recording, style="TButton")
        self.record_button.pack(pady=20)

        self.recording = False
        self.recording_thread = None
        

    def start_recording(self):
        self.recording = True
        self.record_button.config(state="disabled")
        self.recording_thread = threading.Thread(target=self.capturing_audio)
        self.recording_thread.start()



    def convert_wav_to_ogg(self, filename):
        dest_song = os.path.splitext(filename)[0] + ".ogg"
        song = AudioSegment.from_wav(filename)
        song.export(dest_song, format="ogg")
        print("Conversion to OGG complete.")
        
    def process_audio(self):
        result = Shazaming.snippets()
        if result is not None:
            self.current_song = result["title"] + " - " + result["subtitle"]
            song_name, artist_name = extract_and_change_case(result["title"], result["subtitle"])
            sample_details = scrape_samples(song_name, artist_name)
            print(type(sample_details))
            print(sample_details)
            self.display_sample_details(sample_details)
                
                
            

    def download_image(self, image_url, filename):
        try:
            response = requests.get(image_url, stream=True, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
            else:
                print(f"Failed to download image. Status Code: {response.status_code}")
        except Exception as e:
            print("Error during image download:", e)
            
        
    def display_sample_details(self, sample_details):
        if sample_details == []:
            self.sample_details_label = tk.Label(self.root, text="No samples found.")
            self.sample_details_label.pack(pady=10)
        else:
            self.sample_details_label = tk.Label(self.root, text="Sample used:", font=("SF Mono", 16, "bold"))
            self.sample_details_label.pack(pady=10)
            self.current_song_label = tk.Label(self.root, text=self.current_song, font=("SF Mono", 12, "bold"))
            self.current_song_label.pack(pady=10)
            
            

            def display_image(image_url, index):
                try:
                    # Create a directory named "images" if it doesn't exist
                    if not os.path.exists("images"):
                        os.makedirs("images")

                    # Create the image filename
                    image_filename = f"image_{index}.jpg"

                    # Download the image
                    self.download_image(image_url, f"images/{image_filename}")

                    # Create a PIL Image object from the downloaded image
                    img = Image.open(f"images/{image_filename}")
                    img = img.resize((100, 100))  # Resize the image to fit in the UI
                    photo = ImageTk.PhotoImage(img)

                    # Create a label and set the image as its content
                    label = tk.Label(sample_frame, image=photo)
                    label.image = photo
                    label.pack()

                except Exception as e:
                    print(f"Error displaying image {index}: {e}")

            for index, sample in enumerate(sample_details):
                sample_frame = ttk.Frame(self.root)
                sample_frame.pack(pady=10, padx=10, fill=tk.X)

                display_image(sample["image_url"], index)

                sample_text = f"{sample['sample_name']}\n\n{sample['sample_artist']}\n"
                label_text = ttk.Label(sample_frame, text=sample_text, font=("SF Mono", 12, "bold"))
                label_text.pack()
            

        
        
            
    # def clear_ui(self):
    #     # Clear the sample details from the UI
    #     # Reset the sample details and current song data
    #     self.sample_details =  []
    #     self.current_song = None
        

    def capturing_audio(self):
        OUTPUT_FILE_NAME = "audio/out.wav"
        SAMPLE_RATE = 48000
        RECORD_SEC = 10

        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
            print("Recording started...")
            data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
            sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)
            print("Recording finished.")
            self.convert_wav_to_ogg(OUTPUT_FILE_NAME)
            self.process_audio()
            self.record_button.config(state="normal")
            # self.clear_ui()


            


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x900")
    sv_ttk.set_theme("dark")
    app = SampleShazaming(root)
    root.mainloop()
