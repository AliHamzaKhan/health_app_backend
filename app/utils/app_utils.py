import base64
from io import BytesIO
from PIL import Image
from fastapi import UploadFile


async def convert_image_to_base64(image: UploadFile) -> str:
    # Open the uploaded image file
    open_img = Image.open(image.file)

    # Convert the image to RGB (if needed)
    img = open_img.convert('RGB')

    # Save the image to a bytes buffer
    buffered = BytesIO()
    img.save(buffered, format="JPEG")  # or "PNG", depending on your needs

    # Get the bytes from the buffer
    img_bytes = buffered.getvalue()

    # Encode the bytes to base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return img_base64