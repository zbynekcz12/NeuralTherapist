from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

def create_interface_preview():
    # Create a new image with a light gray background
    width = 1200
    height = 800
    image = Image.new('RGB', (width, height), '#f0f0f0')
    draw = ImageDraw.Draw(image)

    # Colors
    primary_color = '#2196F3'
    success_color = '#4CAF50'
    danger_color = '#ff4444'
    dark_text = '#333333'

    # Draw main container with white background
    margin = 20
    draw.rectangle((margin, margin, width-margin, height-margin), 
                  fill='white', outline='#e0e0e0', width=2)

    # Title
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
    except:
        title_font = ImageFont.load_default()
    draw.text((40, 40), "BCI Therapeutic Robot Control", 
              fill=dark_text, font=title_font)

    # Status Panel
    draw.rectangle((40, 100, width-40, 180), 
                  fill='white', outline='#e0e0e0', width=1)
    draw.text((60, 110), "Stav systému", fill=dark_text, font=title_font)
    draw.text((60, 150), "BCI: Připojeno", fill=success_color, font=title_font)
    draw.text((300, 150), "Robot: Připojeno", fill=success_color, font=title_font)

    # Control Panel
    draw.rectangle((40, 200, width-40, 300), 
                  fill='white', outline='#e0e0e0', width=1)

    # Buttons
    button_height = 40
    # Connect BCI button
    draw.rectangle((60, 230, 200, 230+button_height), 
                  fill=primary_color, outline=None)
    draw.text((80, 238), "Připojit BCI", fill='white', font=title_font)

    # Start System button
    draw.rectangle((220, 230, 360, 230+button_height), 
                  fill=primary_color, outline=None)
    draw.text((240, 238), "Spustit Systém", fill='white', font=title_font)

    # Emergency button
    draw.rectangle((width-200, 230, width-60, 230+button_height), 
                  fill=danger_color, outline=None)
    draw.text((width-180, 238), "NOUZOVÉ ZASTAVENÍ", fill='white', font=title_font)

    # Visualization Panel
    draw.rectangle((40, 320, width-40, 600), 
                  fill='white', outline='#e0e0e0', width=1)
    draw.text((60, 330), "Vizualizace signálu", fill=dark_text, font=title_font)

    # Signal plot
    plot_margin = 20
    plot_height = 100
    x = np.linspace(0, 2*np.pi, 100)
    for i, freq in enumerate([1, 2, 3]):
        y = np.sin(freq * x) * plot_height/2
        points = []
        for j in range(len(x)):
            points.append((
                60 + plot_margin + j * (width-160)/len(x),
                380 + plot_height + y[j]
            ))
        for j in range(len(points)-1):
            draw.line([points[j], points[j+1]], 
                     fill=primary_color, width=2)

    # Features plot
    bar_width = 60
    bar_spacing = 40
    bar_height = 120
    baseline_y = 570
    for i, (label, height) in enumerate([
        ('Theta', 0.7), ('Alpha', 0.9), ('Beta', 0.5)
    ]):
        x = 60 + plot_margin + i * (bar_width + bar_spacing)
        bar_h = height * bar_height
        draw.rectangle((x, baseline_y-bar_h, x+bar_width, baseline_y),
                      fill=primary_color, outline=None)
        draw.text((x, baseline_y+10), label, fill=dark_text, font=title_font)

    # Log Panel
    draw.rectangle((40, 620, width-40, height-40), 
                  fill='white', outline='#e0e0e0', width=1)
    draw.text((60, 630), "Systémový log", fill=dark_text, font=title_font)
    draw.text((60, 670), "18:05:26 - BCI zařízení úspěšně připojeno", 
              fill=dark_text, font=title_font)
    draw.text((60, 700), "18:05:27 - Robot připojen a připraven", 
              fill=dark_text, font=title_font)

    # Save the image
    image.save("generated-preview.png")

if __name__ == "__main__":
    create_interface_preview()