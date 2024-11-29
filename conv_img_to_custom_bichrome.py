import os
from tkinter import Tk, filedialog, colorchooser
from PIL import Image

def replace_colors(image_path, black_color, white_color, output_path, cleanup=False, resize_dim=None):
    """
    Replace black and white in an image with specified colors and clean up after conversion.

    :param image_path: Path to the input image.
    :param black_color: Color to replace black (as a tuple, e.g., (0, 0, 0)).
    :param white_color: Color to replace white (as a tuple, e.g., (243, 239, 221)).
    :param output_path: Path to save the output image.
    :param cleanup: If True, performs cleanup by removing metadata and compressing the image.
    :param resize_dim: Optional tuple (width, height) to resize the image.
    """
    image = Image.open(image_path)

    # Convert the image to black and white
    bw_image = image.convert("L")
    threshold = 128
    bw_image = bw_image.point(lambda x: 255 if x > threshold else 0, '1')

    # Convert black and white to RGB for color replacement
    bw_image = bw_image.convert("RGB")

    def replace_pixel_color(pixel):
        if pixel == (255, 255, 255):  # White
            return white_color
        elif pixel == (0, 0, 0):  # Black
            return black_color
        return pixel

    replaced_image = Image.new("RGB", bw_image.size)
    pixels = bw_image.load()

    for y in range(bw_image.size[1]):
        for x in range(bw_image.size[0]):
            replaced_image.putpixel((x, y), replace_pixel_color(pixels[x, y]))

    # Resize the image if specified
    if resize_dim:
        replaced_image = replaced_image.resize(resize_dim, Image.ANTIALIAS)

    # Save the image with cleanup
    if cleanup:
        replaced_image.save(output_path, optimize=True, quality=85)  # Compressed output
    else:
        replaced_image.save(output_path)  # Standard output

    print(f"Processed image saved to {output_path}")

def process_images_in_folder(folder_path, black_color, white_color, cleanup=False, resize_dim=None):
    """
    Process all images in a folder with optional cleanup.

    :param cleanup: If True, performs cleanup by removing metadata and compressing the images.
    :param resize_dim: Optional tuple (width, height) to resize the images.
    """
    output_folder = os.path.join(folder_path, "processed_images")
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(folder_path, file_name)
            output_path = os.path.join(output_folder, file_name)
            replace_colors(input_path, black_color, white_color, output_path, cleanup, resize_dim)

    print(f"All images processed and saved to {output_folder}")

def pick_color_or_default(prompt, default_color):
    """
    Ask the user to either use the default color or customize it via a picker or RGB input.

    :param prompt: Description of what the color is for (e.g., "black" or "white").
    :param default_color: The default color to use as an RGB tuple.
    :return: An RGB tuple (R, G, B).
    """
    choice = input(f"Do you want to customize the color for {prompt}? (default is {default_color}). Type 'yes' to customize or 'no' to use default: ").strip().lower()

    if choice == "yes":
        use_picker = input(f"Do you want to use the color picker for {prompt}? (yes or no): ").strip().lower()
        if use_picker == "yes":
            # Open color picker
            color_code = colorchooser.askcolor(title=f"Select a color to replace {prompt}")
            if color_code[0]:
                return tuple(map(int, color_code[0]))  # Convert to RGB tuple
            else:
                print(f"No color selected for {prompt}. Exiting.")
                exit()
        else:
            # Manual RGB input
            while True:
                try:
                    r = int(input(f"Enter the red value for {prompt} (0-255): "))
                    g = int(input(f"Enter the green value for {prompt} (0-255): "))
                    b = int(input(f"Enter the blue value for {prompt} (0-255): "))
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        return (r, g, b)
                    else:
                        print("RGB values must be between 0 and 255. Try again.")
                except ValueError:
                    print("Invalid input. Please enter integers between 0 and 255.")
    else:
        # Use default color
        return default_color

def main():
    # Initialize the Tkinter GUI (no visible window)
    root = Tk()
    root.withdraw()

    # Default colors
    default_black_color = (0, 0, 0)  # Black remains unchanged by default
    default_white_color = (243, 239, 221)  # White replaced with #f3efdd by default

    # Pick colors for black and white replacement
    print("Select color for black:")
    black_color = pick_color_or_default("black", default_black_color)

    print("Select color for white:")
    white_color = pick_color_or_default("white", default_white_color)

    # Cleanup options
    cleanup = input("Do you want to clean up the images (compress and remove metadata)? (yes or no): ").strip().lower() == "yes"
    resize_dim = None
    if input("Do you want to resize the images? (yes or no): ").strip().lower() == "yes":
        try:
            width = int(input("Enter the width in pixels: "))
            height = int(input("Enter the height in pixels: "))
            resize_dim = (width, height)
        except ValueError:
            print("Invalid dimensions. Skipping resizing.")

    # Ask user to choose single image or folder
    choice = input("Do you want to process a single image or a folder? (type 'image' or 'folder'): ").strip().lower()

    if choice == "image":
        image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if image_path:
            output_path = filedialog.asksaveasfilename(title="Save the processed image", defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if output_path:
                replace_colors(image_path, black_color, white_color, output_path, cleanup, resize_dim)
    elif choice == "folder":
        folder_path = filedialog.askdirectory(title="Select a folder of images")
        if folder_path:
            process_images_in_folder(folder_path, black_color, white_color, cleanup, resize_dim)
    else:
        print("Invalid choice. Please type 'image' or 'folder'.")

if __name__ == "__main__":
    main()
