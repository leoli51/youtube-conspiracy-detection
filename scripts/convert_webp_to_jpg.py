import os
from PIL import Image

def convert_webp_to_jpeg(folder_path):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Only process files with .webp extension
        if filename.lower().endswith('.webp'):
            webp_path = os.path.join(folder_path, filename)
            jpeg_path = os.path.splitext(webp_path)[0] + '.jpg'
            
            try:
                # Open the .webp image
                with Image.open(webp_path) as img:
                    # Convert and save as .jpg
                    img.convert('RGB').save(jpeg_path, 'JPEG')
                    print(f"Converted {filename} to {jpeg_path}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

# Example usage
folder_path = '/home/leoli/Uni/Polimi/Thesis/master-thesis/data/myyounicon-01/images'  # Replace with the folder path
convert_webp_to_jpeg(folder_path)
