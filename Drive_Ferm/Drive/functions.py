from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO
import random
from django.contrib.auth import get_user_model



def generate_initial_image(username):
    # Generate a random background color
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new('RGB', (100, 100), color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        #"/Users/oggyis/Documents/GitHub/Drive/Drive_Ferm/static/fonts/LTPerfume-2.ttf"
        # Use a common font, adjust the path or font as necessary
        font = ImageFont.truetype("/Users/oggyis/Documents/GitHub/Drive/Drive_Ferm/static/fonts/Rogena Display.ttf", 100)
    except IOError:
        font = ImageFont.load_default()
    
    # Get the first letter of the username
    text = username[0].upper()
    text_width, text_height = draw.textsize(text, font=font)
    
    # Center the text
    text_x = (img.width - text_width) / 2
    text_y = (img.height - text_height) / 2
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    # Save the image to a bytes buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)  # Move to the start of the buffer
    content_file = ContentFile(buffer.getvalue())
    file_name = f"{username}_initial.png"
    
    return content_file, file_name  # Ensure this matches what you're expecting in the save() call



def generate_unique_username(first_name, last_name):
    UserAuth = get_user_model()
    base_username = f"{first_name}{last_name}".lower()
    unique_username = base_username
    num = 1
    while UserAuth.objects.filter(username=unique_username).exists():
        unique_username = f"{base_username}{num}"
        num += 1
    return unique_username