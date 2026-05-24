from cpu import CPU
from gpu import GPU
from ram import RAM
from storage import Storage
from psu import PSU
from motherboard import Motherboard
from file_reading import read_files
from pc_build import PCBUILD

build_type = int(input("Enter what build do you want: cheap, okay or expensive (type 1, 2, or 3 respectively)"))
if build_type not in (1, 2, 3):
    print("only enter 1, 2, or 3")
else:
    cpu_list = read_files('data/cpus.csv', CPU, build_type)
    gpu_list = read_files('data/gpus.csv', GPU, build_type)
    psu_list = read_files('data/psus.csv', PSU, build_type)
    ram_list = read_files('data/ram.csv', RAM, build_type)
    storage_list = read_files('data/storage.csv', Storage, build_type)
    motherboard_list = read_files('data/motherboards.csv', Motherboard, build_type)

if build_type == 1:
    budget = "cheap"
elif    build_type == 2:
    budget = "okay"
else:
    budget = "expensive"

custom_build = input("Do you want to custom build? (yes/no): ").strip().lower()
if custom_build == "yes":
    user_build = PCBUILD()

    print("Choose a CPU:")
    for index, cpu in enumerate(cpu_list):
        print(f"{index}: {cpu.display_info()}")
    index = int(input("Choose CPU index: "))
    user_build.add_component(cpu_list[index])
    selected_cpu = cpu_list[index]

    print("Choose a GPU:")
    for index, gpu in enumerate(gpu_list):
        print(f"{index}: {gpu.display_info()}")
    index = int(input("Choose GPU index: "))
    user_build.add_component(gpu_list[index])

    print("Choose a PSU:")
    for index, psu in enumerate(psu_list):
        print(f"{index}: {psu.display_info()}")
    index = int(input("Choose PSU index: "))
    user_build.add_component(psu_list[index])

    print("Choose RAM:")
    for index, ram in enumerate(ram_list):
        print(f"{index}: {ram.display_info()}")
    index = int(input("Choose RAM index: "))
    user_build.add_component(ram_list[index])

    print("Choose Storage:")
    for index, storage in enumerate(storage_list):
        print(f"{index}: {storage.display_info()}")
    index = int(input("Choose Storage index: "))
    user_build.add_component(storage_list[index])

    # show only motherboards compatible with selected CPU socket
    compatible_mbs = [m for m in motherboard_list if m.socket == selected_cpu.socket]
    if not compatible_mbs:
        print("No motherboards match the selected CPU socket; showing all options.")
        compatible_mbs = motherboard_list

    print("Choose a Motherboard:")
    for index, motherboard in enumerate(compatible_mbs):
        print(f"{index}: {motherboard.display_info()}")
    index = int(input("Choose Motherboard index: "))
    user_build.add_component(compatible_mbs[index])

    print("\nYour custom build:")
    user_build.display_build()
    print("Total price:", user_build.total_price())
else:
    build = PCBUILD()
    selected_cpu = build.choose_random_component(cpu_list)
    build.choose_random_component(gpu_list)
    build.choose_random_component(psu_list)
    build.choose_random_component(ram_list)
    build.choose_random_component(storage_list)
    # pick a motherboard that matches the CPU socket when possible
    compatible_mbs = [m for m in motherboard_list if selected_cpu and getattr(selected_cpu, 'socket', None) == getattr(m, 'socket', None)]
    if compatible_mbs:
        build.choose_random_component(compatible_mbs)
    else:
        build.choose_random_component(motherboard_list)
    print("\n")
    print("Random build selected:")
    build.display_build()
    print("\n")
    print("Total price:")
    print(build.total_price())
