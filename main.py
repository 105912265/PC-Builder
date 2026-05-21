from cpu import CPU
from gpu import GPU
from ram import RAM
from storage import Storage
from psu import PSU
from pc_build import PCBUILD

CPU1 = CPU("Ryzen 5 3600", "AMD", 150, 6, "AM4")
GPU1 = GPU("RTX2060", "NVIDIA", 180, 6)
RAM1 = RAM("RAM1", "RIPJAWS", 100, "DDR4", 3600)
SSD1 = Storage("SSD1", "SAMSUNG", 100, "SSD", 512)
PSU1 = PSU("PSU1", "DEEPCOOL", 60, 500)

parts = [CPU1, GPU1, RAM1, SSD1, PSU1]

myPC = PCBUILD()

for part in parts:
    myPC.add_component(part)

myPC.display_build()
print(myPC.total_price())
