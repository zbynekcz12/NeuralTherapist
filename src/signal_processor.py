import numpy as np
from scipy import signal
from config import config
from logger import logger

class SignalProcessor:
    def __init__(self):
        self.nyquist = config.SAMPLING_RATE / 2
        self.b, self.a = signal.butter(4, 
                                     [config.FILTER_LOW_CUTOFF / self.nyquist,
                                      config.FILTER_HIGH_CUTOFF / self.nyquist],
                                     btype='band')

    def filter_signal(self, data):
        try:
            filtered_data = signal.filtfilt(self.b, self.a, data)
            return filtered_data
        except Exception as e:
            logger.error(f"Error filtering signal: {e}")
            return data

    def extract_features(self, data):
        try:
            # Simple feature extraction: normalized power in different bands
            fft_vals = np.abs(np.fft.rfft(data))
            freqs = np.fft.rfftfreq(len(data), 1.0/config.SAMPLING_RATE)
            
            # Define frequency bands
            theta = np.mean(fft_vals[(freqs >= 4) & (freqs <= 8)])
            alpha = np.mean(fft_vals[(freqs >= 8) & (freqs <= 13)])
            beta = np.mean(fft_vals[(freqs >= 13) & (freqs <= 30)])
            
            return {
                'theta': theta,
                'alpha': alpha,
                'beta': beta
            }
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return None

    def classify_command(self, features):
        if not features:
            return 'none'
        
        try:
            # Simple threshold-based classification
            if features['alpha'] > features['beta'] * 1.5:
                return 'forward'
            elif features['beta'] > features['alpha'] * 1.5:
                return 'stop'
            else:
                return 'none'
        except Exception as e:
            logger.error(f"Error classifying command: {e}")
            return 'none'
