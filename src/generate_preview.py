from PIL import Image, ImageDraw, ImageFont
import os

def create_interface_preview():
    # Create a new image with a white background
    width = 800
    height = 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Draw main sections
    draw.rectangle((50, 50, 750, 150), outline='black', width=2)  # Status panel
    draw.rectangle((50, 170, 750, 270), outline='black', width=2)  # Control panel
    draw.rectangle((50, 290, 750, 490), outline='black', width=2)  # Visualization
    draw.rectangle((50, 510, 750, 580), outline='black', width=2)  # Log panel

    # Add text
    font_size = 20
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Headers
    draw.text((60, 60), "BCI Therapeutic Robot Control", fill='black', font=font)
    draw.text((60, 100), "Status: BCI Connected, Robot Ready", fill='green', font=font)

    # Controls
    draw.rectangle((60, 190, 160, 230), fill='lightblue', outline='black')  # Connect button
    draw.text((70, 200), "Connect BCI", fill='black', font=font)

    draw.rectangle((180, 190, 280, 230), fill='lightblue', outline='black')  # Start button
    draw.text((190, 200), "Start System", fill='black', font=font)

    draw.rectangle((600, 190, 740, 230), fill='red', outline='black')  # Emergency button
    draw.text((610, 200), "EMERGENCY", fill='white', font=font)

    # Visualization mockup
    draw.line([(60, 390), (740, 390)], fill='gray', width=1)  # Center line
    for i in range(60, 740, 10):
        y = 390 + int(30 * (i % 3 - 1))  # Simple wave pattern
        draw.line([(i, y), (i+5, y)], fill='green', width=2)

    # Save the image
    image.save("generated-preview.png")

if __name__ == "__main__":
    create_interface_preview()