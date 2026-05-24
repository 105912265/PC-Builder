from cpu import CPU
from gpu import GPU
from ram import RAM
from storage import Storage
from psu import PSU
from file_reading import read_files


build_type = int(input("Enter what build do you want: cheap, okay or expensive (type 1, 2, or 3 respectively)"))
if build_type not in (1, 2, 3):
    print("only enter 1, 2, or 3")
else:
    cpu_list = read_files('data/cpus.csv', CPU, build_type)
    gpu_list = read_files('data/gpus.csv', GPU, build_type)
    psu_list = read_files('data/psus.csv', PSU, build_type)
    ram_list = read_files('data/ram.csv', RAM, build_type)
    storage_list = read_files('data/storage.csv', Storage, build_type)

if build_type == 1:
    budget = "cheap"
elif    build_type == 2:
    budget = "okay"
else:
    budget = "expensive"

print("\n")
print(f"These are the {budget} Component options")
print("\n")

print("CPU:")
for cpu in cpu_list:
    print(cpu.display_info())

print("\n")
print("GPU:")
for gpu in gpu_list:
    print(gpu.display_info())

print("\n")
print("PSU:")
for psu in psu_list:
    print(psu.display_info())

print("\n")
print("RAM:")
for ram in ram_list:
    print(ram.display_info())

print("\n")
print("Storage:")
for storage in storage_list:
    print(storage.display_info())

  