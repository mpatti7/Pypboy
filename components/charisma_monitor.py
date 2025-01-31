import os
import platform
import subprocess



class CharismaMonitor():
    def __init__(self, base_ip, gateway_ip):
        self.base_ip = base_ip
        self.gateway_ip = gateway_ip
    

    def ping_device(self, ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", ip]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                output = result.stdout.decode()
                latency = self.extract_latency(output)
                return latency
            return None
        except Exception:
            return None


    def extract_latency(self, ping_output):
        if "time=" in ping_output:
            try:
                return float(ping_output.split("time=")[1].split(" ")[0])
            except (ValueError, IndexError):
                pass
        return None


    def scan_local_network(self):
        active_devices = {}
        for i in range(1, 255):
            ip = f"{self.base_ip}.{i}"
            latency = self.ping_device(ip)
            if latency is not None:
                active_devices[ip] = latency
        return active_devices


    def get_charisma_factors(self):
        devices = self.scan_local_network()
        return devices, len(devices), self.ping_device(self.gateway_ip) is not None
    

