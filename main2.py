#Author: Kshitij Kshirsagar
#Filename: main2.py
#Last edited: 07/06/2026

from src.data_loader import load_cpus, load_gpus, load_motherboards, load_psu, load_ram, load_storage
from src.compatibility_checker import is_build_compatible, calculate_total_price, calculate_total_wattage


cpus = load_cpus("data/cpu_bench.csv")
gpus = load_gpus("data/gpu_bench.csv")
rams = load_ram("data/ram.csv")
psus = load_psu("data/psus.csv")
motherboards = load_motherboards("data/motherboards.csv")
storages = load_storage("data/storage.csv")

budget = 3000

print(cpus[0].display_info())
print(gpus[0].display_info())
print(motherboards[0].display_info())
print(rams[0].display_info())
print(storages[0].display_info())
print(psus[0].display_info())

print(calculate_total_wattage(cpus[0], gpus[0], motherboards[0], rams[0], storages[0]))
print(calculate_total_price(cpus[0], gpus[0], motherboards[0], rams[0], storages[0], psus[0]), f"Budget: {budget}")
print(is_build_compatible(cpus[0], gpus[0], motherboards[0], rams[0], storages[0], psus[3], budget))

