import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk
import logging
import os

# Stream Logger Setup
logger = logging.getLogger("ImageSlideshow")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(stream_handler)


image_paths = [
    r"C:\Users\HP\OneDrive\Pictures\Saved Pictures\WhatsApp Image 2025-02-26 at 08.26.42_840f9bf5.jpg",
    r"C:\Users\HP\OneDrive\Pictures\Screenshots\Screenshot 2025-02-11 190318.png",
    r"C:\Users\HP\OneDrive\Pictures\Screenshots\Screenshot 2025-02-03 215952.png"
]


def load_images(paths, size=(1080, 1080)):
    images = []
    for path in paths:
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image not found: {path}")
            img = Image.open(path).resize(size)
            images.append(img)
            logger.info(f"Loaded image (PIL): {path}")
        except Exception as e:
            logger.error(f"Failed to load image '{path}': {e}")
    return images


def main():
    try:
        
        root = tk.Tk()
        root.title("Image Slideshow Viewer")
        root.geometry("1080x1080")

        # Load PIL images
        pil_images = load_images(image_paths)

        if not pil_images:
            logger.critical("No valid images to display. Exiting.")
            return

        # Now convert PIL images to Tkinter-compatible
        photo_images = [ImageTk.PhotoImage(img) for img in pil_images]
        image_cycle = cycle(photo_images)

        label = tk.Label(root)
        label.pack()

        def update_image():
            try:
                next_image = next(image_cycle)
                label.config(image=next_image)
                root.after(3000, update_image)
            except Exception as e:
                logger.error(f"Error updating image : {e}")


        def start_slideshow():
            logger.info("Slideshow started.")
            update_image()

        play_button = tk.Button(root, text="Play Slideshow", command=start_slideshow, font=("Helvetica", 14))
        play_button.pack(pady=10)

        logger.info("Image Slideshow Viewer initialized.")
        root.mainloop()

    except Exception as e:
        logger.exception(f"Application crashed : {e}")


if __name__ == "__main__":
    main()