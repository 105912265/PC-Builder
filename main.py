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

myPC = PCBUILD()

myPC.add_component(CPU1)
myPC.add_component(GPU1)
myPC.add_component(RAM1)
myPC.add_component(SSD1)
myPC.add_component(PSU1)

print(PCBUILD.display_build(myPC))
print(PCBUILD.total_price(myPC))