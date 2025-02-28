import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from config import config

class Visualizer:
    def __init__(self):
        plt.style.use('dark_background')
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 6))
        self.fig.canvas.manager.set_window_title('BCI Signal Visualization')

        # Signal plot
        self.line1, = self.ax1.plot([], [], 'g-', linewidth=1)
        self.ax1.set_title('Raw BCI Signal')
        self.ax1.set_ylim(-100, 100)
        self.ax1.set_xlim(0, config.BUFFER_SIZE)
        self.ax1.grid(True)

        # Feature plot
        self.bars = self.ax2.bar(['Theta', 'Alpha', 'Beta'], [0, 0, 0])
        self.ax2.set_title('Frequency Band Powers')
        self.ax2.set_ylim(0, 100)

        plt.tight_layout()

    def update_plot(self, frame, signal_data_func, feature_data_func):
        # Get current data
        signal_data = signal_data_func()
        features = feature_data_func(signal_data)

        # Update signal plot
        x = np.arange(len(signal_data))
        self.line1.set_data(x, signal_data)

        # Update feature bars
        if features:
            heights = [features['theta'], features['alpha'], features['beta']]
            for bar, height in zip(self.bars, heights):
                bar.set_height(height)

        return self.line1, *self.bars

    def start_visualization(self, signal_data_func, feature_data_func):
        # Set up animation with fixed frame count
        frames = 100  # Počet snímků v animaci
        ani = FuncAnimation(
            self.fig,
            self.update_plot,
            frames=frames,
            fargs=(signal_data_func, feature_data_func),
            interval=100,
            blit=True,
            cache_frame_data=False
        )
        plt.show()