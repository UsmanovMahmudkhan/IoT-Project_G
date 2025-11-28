import sys
import threading
import time
from unittest.mock import MagicMock

# Mock modules
sys.modules['gpiozero'] = MagicMock()
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['picamera'] = MagicMock()
sys.modules['gps'] = MagicMock()

# Mock specific attributes
sys.modules['gps'].WATCH_ENABLE = 1
sys.modules['gps'].WATCH_NEWSTYLE = 2

sys.modules['simpleaudio'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['Adafruit_DHT'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()

# Mock gpiozero.DistanceSensor
class MockDistanceSensor:
    def __init__(self, *args, **kwargs):
        self.value = 0.5
        self.distance = 1.0 # 1 meter
sys.modules['gpiozero'].DistanceSensor = MockDistanceSensor

# Mock gps.gps class
class MockGps:
    def __init__(self, *args, **kwargs):
        pass
    def next(self):
        return {'class': 'TPV', 'lat': 37.7749, 'lon': -122.4194} # Fake location
sys.modules['gps'].gps = MockGps

# Mock picamera.PiCamera
class MockPiCamera:
    def __init__(self, *args, **kwargs):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def start_recording(self, output, format=None):
        # Simulate writing frames to output
        def record():
            while True:
                time.sleep(1)
                # Write a fake frame header/content if needed, or just ignore
                # The StreamingOutput expects bytes starting with \xff\xd8
                if hasattr(output, 'write'):
                    output.write(b'\xff\xd8' + b'\x00' * 100)
        t = threading.Thread(target=record, daemon=True)
        t.start()
    def stop_recording(self):
        pass
sys.modules['picamera'].PiCamera = MockPiCamera

# Import main
import main

if __name__ == "__main__":
    print("Starting Smart Shoe Server with Mocks...")
    try:
        main.main()
    except KeyboardInterrupt:
        print("Stopping...")
