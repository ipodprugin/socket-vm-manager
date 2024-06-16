from typing import List


class Disk:
    def __init__(self, id: str, size: int):
        self.id = id
        self.size = size


class VM:
    def __init__(self, id: str, ram: int, cpu: int, password: str, disks: List[Disk] = []):
        self.id = id
        self.ram = ram
        self.cpu = cpu
        self.password = password
        self.disks = disks

