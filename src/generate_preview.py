import numpy as np
from PIL import Image, ImageDraw, ImageFont
from config import config

def create_interface_preview():
    # Create a new image with a light gray background
    width = 1200
    height = 800
    image = Image.new('RGB', (width, height), '#f0f0f0')
    draw = ImageDraw.Draw(image)

    # Colors
    primary_color = '#2196F3'  # Material Blue
    success_color = '#4CAF50'  # Material Green
    danger_color = '#ff4444'   # Material Red
    dark_text = '#333333'
    light_text = '#ffffff'
    border_color = '#e0e0e0'

    # Draw main container with white background and subtle shadow effect
    margin = 20
    shadow_offset = 2
    # Draw shadow
    draw.rectangle((margin+shadow_offset, margin+shadow_offset, 
                   width-margin+shadow_offset, height-margin+shadow_offset),
                  fill='#d0d0d0')
    # Draw main container
    draw.rectangle((margin, margin, width-margin, height-margin),
                  fill='white', outline=border_color, width=2)

    # Title with larger font
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
        normal_font = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()

    draw.text((40, 40), "BCI Therapeutic Robot Control",
              fill=dark_text, font=title_font)

    # Status Panel with modern design
    status_y = 100
    draw.rectangle((40, status_y, width-40, status_y+80),
                  fill='white', outline=border_color, width=1)
    draw.text((60, status_y+10), "Stav systému", fill=dark_text, font=title_font)

    # Status indicators with colored circles
    circle_radius = 8
    status_text_y = status_y + 45
    # BCI Status
    draw.ellipse((60, status_text_y, 60+circle_radius*2, status_text_y+circle_radius*2),
                 fill=success_color)
    draw.text((85, status_text_y), "BCI: Připojeno", fill=success_color, font=normal_font)
    # Robot Status
    draw.ellipse((300, status_text_y, 300+circle_radius*2, status_text_y+circle_radius*2),
                 fill=success_color)
    draw.text((325, status_text_y), "Robot: Připojen", fill=success_color, font=normal_font)

    # Control Panel with modern buttons
    control_y = 200
    draw.rectangle((40, control_y, width-40, control_y+100),
                  fill='white', outline=border_color, width=1)

    # Modern styled buttons
    button_height = 40
    button_y = control_y + 30

    # Connect BCI button with rounded corners
    draw.rectangle((60, button_y, 200, button_y+button_height),
                  fill=primary_color)
    draw.text((80, button_y+8), "Připojit BCI", fill=light_text, font=normal_font)

    # Start System button
    draw.rectangle((220, button_y, 360, button_y+button_height),
                  fill=primary_color)
    draw.text((240, button_y+8), "Spustit Systém", fill=light_text, font=normal_font)

    # Emergency Stop button
    draw.rectangle((width-200, button_y, width-60, button_y+button_height),
                  fill=danger_color)
    draw.text((width-180, button_y+8), "NOUZOVÉ ZASTAVENÍ", fill=light_text, font=normal_font)

    # Visualization Panel with modern charts
    viz_y = 320
    draw.rectangle((40, viz_y, width-40, viz_y+280),
                  fill='white', outline=border_color, width=1)
    draw.text((60, viz_y+10), "Vizualizace signálu", fill=dark_text, font=title_font)

    # Signal plot with smooth curves
    plot_margin = 20
    plot_height = 100
    x = np.linspace(0, 4*np.pi, 200)  # More points for smoother curve
    # Generate multiple waves for more interesting visualization
    for i, (freq, amp, phase) in enumerate([(1, 1, 0), (2, 0.5, np.pi/4), (3, 0.3, np.pi/3)]):
        y = amp * np.sin(freq * x + phase) * plot_height/2
        points = []
        for j in range(len(x)):
            points.append((
                60 + plot_margin + j * (width-160)/len(x),
                viz_y + 80 + plot_height + y[j]
            ))
        # Draw smooth curve
        for j in range(len(points)-1):
            draw.line([points[j], points[j+1]], fill=primary_color, width=2)

    # Bar chart for frequency bands
    bar_width = 80
    bar_spacing = 60
    bar_height = 140
    baseline_y = viz_y + 240

    # Draw background grid
    for y in range(viz_y+100, baseline_y, 20):
        draw.line([(60, y), (width-60, y)], fill='#f0f0f0', width=1)

    # Draw bars with gradient effect
    for i, (label, height_ratio) in enumerate([
        ('Theta', 0.7), ('Alpha', 0.9), ('Beta', 0.5)
    ]):
        x = 60 + plot_margin + i * (bar_width + bar_spacing)
        bar_h = height_ratio * bar_height
        # Draw bar with gradient effect
        for h in range(int(bar_h)):
            alpha = 255 - int(h * 100 / bar_h)
            color = f'#{primary_color[1:3]}{primary_color[3:5]}{primary_color[5:7]}{alpha:02x}'
            draw.rectangle((x, baseline_y-h, x+bar_width, baseline_y-h+1),
                         fill=color)
        draw.text((x+10, baseline_y+10), label, fill=dark_text, font=normal_font)

    # Log Panel with modern styling
    log_y = viz_y + 300
    log_height = height - log_y - 40
    if log_height > 0:
        draw.rectangle((40, log_y, width-40, log_y+log_height),
                      fill='white', outline=border_color, width=1)
        draw.text((60, log_y+10), "Systémový log", fill=dark_text, font=title_font)
        # Log entries with timestamps
        log_font = normal_font
        draw.text((60, log_y+50), "18:05:26 - BCI zařízení úspěšně připojeno",
                 fill=success_color, font=log_font)
        draw.text((60, log_y+80), "18:05:27 - Robot připojen a připraven",
                 fill=success_color, font=log_font)

    # Save the image with high quality
    image.save("generated-preview.png", quality=95)

if __name__ == "__main__":
    create_interface_preview()