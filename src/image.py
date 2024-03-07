from PIL import Image
import numpy as np

from rlwe_concept import RingLWECrypto

# Assuming the RingLWECrypto class is defined as in the previous example

# Process the image
input_image_path = "data/input.jpg"  # Update this path
encrypted_output_path = "data/encrypted_output.jpg"  # Update this path
decrypted_output_path = "data/decrypted_output.jpg"  # Update this path

# Initialize the Ring-LWE crypto system (using previously defined parameters)
crypto = RingLWECrypto(n=256, q=7681)


# Redefining the image processing functions from the provided scripts
def load_image(image_path, new_width):
    """Loads an image in color and resizes it while maintaining aspect ratio."""
    with Image.open(image_path) as img:
        # Maintain aspect ratio
        aspect_ratio = img.height / img.width
        new_height = int(new_width * aspect_ratio)

        # Resize image without converting to grayscale
        img_resized = img.resize((new_width, new_height))
        img_array = np.asarray(img_resized)

    return img_array

def save_image(image_array, output_path):
    """Saves a numpy array as a color image."""
    # Determine the mode based on the shape of the array
    if len(image_array.shape) == 3 and image_array.shape[2] == 3:
        mode = 'RGB'  # Color image
    else:
        mode = 'L'  # Grayscale image
    img = Image.fromarray(image_array.astype(np.uint8), mode=mode)
    img.save(output_path)

def process_and_save_encrypted_image(image_path, encrypted_output_path, decrypted_output_path, crypto):
    # Load the original image without resizing to get original dimensions
    with Image.open(image_path) as orig_img:
        orig_size = orig_img.size  # Store the original size

    # Load the image in color and resize it to match crypto.n width
    img_array = load_image(image_path, new_width=crypto.n)

    encrypted_image = np.zeros_like(img_array)  # To store the encrypted pixels
    decrypted_image = np.zeros_like(img_array)  # Ensures the output image has the same dimensions

    # To keep track of 'a' values for decryption verification
    a_values = []

    # Process each color channel separately
    for channel in range(img_array.shape[-1]):  # Assuming the last dimension is color channels
        for i, row in enumerate(img_array[:, :, channel]):
            a, encrypted_row = crypto.encrypt(row)
            encrypted_image[i, :, channel] = encrypted_row
            a_values.append(a)

            decrypted_row = crypto.decrypt(a, encrypted_row)
            decrypted_image[i, :, channel] = decrypted_row

    # Resize the decrypted image back to the original size
    decrypted_image = np.array(Image.fromarray(decrypted_image).resize(orig_size, Image.LANCZOS))

    # Save the encrypted and decrypted images
    save_image(encrypted_image, encrypted_output_path)
    save_image(decrypted_image, decrypted_output_path)


process_and_save_encrypted_image(input_image_path, encrypted_output_path, decrypted_output_path, crypto)
