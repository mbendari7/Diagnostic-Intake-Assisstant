import platform
import psutil
import json
import datetime

class DiagnosticsScanner:
    def __init__(self):
        self.timestamp = str(datetime.datetime.now())

    def get_basic_system_info(self):
        try:
            return {
                "os": platform.system(),
                "os_release": platform.release(),
                "architecture": platform.machine()
            }
        except Exception as e:
            return {"error": f"Failed to get OS info: {e}"}

    def get_cpu_info(self):
        try:
            return {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "current_usage_percent": psutil.cpu_percent(interval=1)
            }
        except Exception as e:
            return {"error": f"Failed to get CPU info: {e}"}

    def get_memory_info(self):
        try:
            svmem = psutil.virtual_memory()
            gb_conversion = 1024 ** 3
            return {
                "total_gb": round(svmem.total / gb_conversion, 2),
                "available_gb": round(svmem.available / gb_conversion, 2),
                "used_percent": svmem.percent
            }
        except Exception as e:
            return {"error": f"Failed to get memory info: {e}"}

    def get_disk_info(self):
        try:
            partitions = psutil.disk_partitions()
            boot_drive = next((p.mountpoint for p in partitions if p.mountpoint in ('C:\\', '/')), partitions[0].mountpoint)
            disk_usage = psutil.disk_usage(boot_drive)
            
            gb_conversion = 1024 ** 3
            return {
                "drive_path": boot_drive,
                "total_gb": round(disk_usage.total / gb_conversion, 2),
                "free_gb": round(disk_usage.free / gb_conversion, 2),
                "used_percent": disk_usage.percent
            }
        except Exception as e:
            return {"error": f"Failed to get disk info: {e}"}

    def get_top_processes(self, count=5):
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:count]
            top_memory = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:count]
            
            return {
                "top_cpu_consumers": top_cpu,
                "top_memory_consumers": top_memory
            }
        except Exception as e:
            return {"error": f"Failed to get process info: {e}"}

    def get_live_diagnostics_dictionary(self):
        return {
            "timestamp": self.timestamp,
            "system_profile": self.get_basic_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "active_software": self.get_top_processes()
        }

def get_live_data():
    scanner = DiagnosticsScanner()
    return scanner.get_live_diagnostics_dictionary()

if __name__ == "__main__":
    print(json.dumps(get_live_data(), indent=4))