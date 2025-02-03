import platform
import subprocess
import threading



class CharismaMonitor():
    def __init__(self, base_ip, gateway_ip, special_view):
        self.base_ip = base_ip
        self.gateway_ip = gateway_ip
        self.special_view = special_view #for updating the frontend while pinging devices on the network


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
        count = 0
        for i in range(45, 55):
            ip = f"{self.base_ip}.{i}"
            latency = self.ping_device(ip)
            if latency is not None:
                count += 1
                active_devices[ip] = latency
                #This will take awhile to get through every address so for every 2 devices that are active, update the frontend
                if count >= 2:
                    threading.Thread(target=self.special_view.update_frontend_with_charisma_data, args=(active_devices, 
                                                                                                len(active_devices), 
                                                                                                self.ping_device(self.gateway_ip) is not None),
                                                                                                daemon=True).start()
                    count = 0
        return active_devices


    def get_charisma_factors(self):
        devices = self.scan_local_network()
        return devices, len(devices), self.ping_device(self.gateway_ip) is not None
    

