import psutil
import time
import speedtest
import threading
import subprocess
import re


class SpeedFetcher():
    def __init__(self):
        self.write_speed = None
        self.read_speed = None
        self.disk_queue_length = None
        self.download_speed = None
        self.upload_speed = None
        self.is_speed_test_running = False
    

    def fetch_disk_speed_async(self):
        threading.Thread(target=self.get_disk_io_speed, daemon=True).start()
    

    # Only want to run this once while in the view
    def fetch_download_upload_speed_async(self):
        if not self.is_speed_test_running:
            self.is_speed_test_running = True
            threading.Thread(target=self.run_speed_test, daemon=True).start()


    def get_disk_io_speed(self, interval=1, samples=3):
        max_read_speed = 0
        max_write_speed = 0
        total_queue_length = 0

        # Get the average speeds over 3 readings
        for i in range(samples):
            disk_io_start = psutil.disk_io_counters()
            time.sleep(interval)
            disk_io_end = psutil.disk_io_counters()

            read_speed = (disk_io_end.read_bytes - disk_io_start.read_bytes) / interval
            write_speed = (disk_io_end.write_bytes - disk_io_start.write_bytes) / interval

            read_operations = disk_io_end.read_count - disk_io_start.read_count
            write_operations = disk_io_end.write_count - disk_io_start.write_count
            queue_length = (read_operations + write_operations) / interval

            max_read_speed = max(max_read_speed, read_speed)
            max_write_speed = max(max_write_speed, write_speed)
            total_queue_length += queue_length

        # Store the best observed speeds and average queue length
        self.read_speed = max_read_speed
        self.write_speed = max_write_speed
        self.disk_queue_length = round(total_queue_length / samples, 2)  


    def run_speed_test(self):
        try:
            # Attempt to use the speedtest Python package
            st = speedtest.Speedtest()
            st.get_best_server()
            self.download_speed = st.download() / 1_000_000  # Convert to Mbps
            self.upload_speed = st.upload() / 1_000_000      # Convert to Mbps
            return self.download_speed, self.upload_speed
        except (speedtest.ConfigRetrievalError, speedtest.SpeedtestException):
            print("Python Speedtest package failed. Falling back to subprocess.")
            return self.run_speed_test_cli()
    

    def run_speed_test_cli(self):
        try:
            # Run the speedtest-cli command and capture the output
            result = subprocess.run(["speedtest-cli"], capture_output=True, text=True)

            # Extract download and upload speeds from the result using regex
            download_match = re.search(r"Download: (\d+\.\d+) Mbit/s", result.stdout)
            upload_match = re.search(r"Upload: (\d+\.\d+) Mbit/s", result.stdout)

            if download_match and upload_match:
                self.download_speed = float(download_match.group(1))
                self.upload_speed = float(upload_match.group(1))
                return self.download_speed, self.upload_speed
            else:
                print("Failed to parse speedtest-cli output.")
                return 0, 0
        except FileNotFoundError:
            print("speedtest-cli not installed. Please install it with: sudo apt install speedtest-cli")
            return 0, 0

