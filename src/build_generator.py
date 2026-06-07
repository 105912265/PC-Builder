# Author: Kshitij Kshirsagar
# Filename: build_generator.py
# Last edited: 07/06/2026

from pc_build import PCBUILD
from src.compatibility_checker import calculate_total_wattage


def cpu_heuristic(cpu):
    """
    calculates CPU performance/dollar
    :param cpu: object CPU
    :return: performance/dollar
    """
    return cpu.cpu_mark / cpu.price


def gpu_heuristic(gpu):
    """
    calculates GPU performance/dollar
    :param gpu: object GPU
    :return: performance/dollar
    """
    return gpu.g3d_mark / gpu.price


def choose_top_cpus(cpus, budget, limit=40):
    """
    choose top cpus based on budget and their heuristic (performance/dollar)
    :param cpus: list of cpus from cpu_bench.csv
    :param budget: budget based on user input
    :param limit: how many cpus to choose
    :return affordable_cpus: list of cpus that fit budget and heuristc
    """
    affordable_cpus = [
        cpu for cpu in cpus
        if cpu.price <= budget * 0.30
    ]

    affordable_cpus.sort(key=cpu_heuristic, reverse=True)
    return affordable_cpus[:limit]


def choose_top_gpus(gpus, budget, limit=40):
    """
    choose top gpus based on budget and their heuristic (performance/dollar)
    :param cpus: list of gpus from gpu_bench.csv
    :param budget: budget based on user input
    :param limit: how many gpus to choose
    :return affordable_gpus: list of cpus that fit budget and heuristc
    """
    affordable_gpus = [
        gpu for gpu in gpus
        if gpu.price <= budget * 0.50
    ]

    affordable_gpus.sort(key=gpu_heuristic, reverse=True)
    return affordable_gpus[:limit]


def choose_best_motherboard(cpu, motherboards):
    """
    finds motherboards that are compatible with cpu
    :param cpu: object CPU
    :param motherboards: list of motherboards from motherboards.csv
    :return None: if not compatible motherboards are found
    :return: cheapest motherboard compatible
    """
    matching_motherboards = [
        motherboard for motherboard in motherboards
        if motherboard.socket == cpu.socket
    ]

    if not matching_motherboards:
        return None

    return min(matching_motherboards, key=lambda motherboard: motherboard.price)


def choose_top_ram(motherboard, ram_list, limit=3):
    """
    chooses ram compatible with mobo and with best capacity/price ratio
    :param motherboard: object Motherboard
    :param ram_list: list of rams from ram.csv
    :param limit=3: limits how many rams are chosen (3 for this instance)
    :return matching_ram[:limit]: list of top limit amount of rams chosen 
    """
    matching_ram = [
        ram for ram in ram_list
        if ram.ram_type == motherboard.ram_type
    ]

    matching_ram.sort(
        key=lambda ram: ram.size_gb / ram.price,
        reverse=True
    )

    return matching_ram[:limit]


def choose_top_storage(storage_list, limit=3):
    """
    chooses best storage based on capacity/price ratio
    :param storage_list: list of storages from storage.csv
    :param limit=3: limits how many storages are chosen (3 for this instance)
    :return storage_list[:limit]: list of top limit amount of storage options chosen
    """
    storage_list.sort(
        key=lambda storage: storage.capacity_gb / storage.price,
        reverse=True
    )

    return storage_list[:limit]


def choose_best_psu(total_wattage, psus):
    """
    chooses best psu based on wattage and future upgrade considerations
    :param total_wattage: calculated from 'from src.compatibility_checker import calculate_total_wattage'
    :param psus: list of psus from psus.csv
    :return None: if no valid psus are found
    :return min(valid_psus, key=lambda psu: psu.price): cheapest valid psu
    """
    required_wattage = total_wattage * 1.3

    valid_psus = [
        psu for psu in psus
        if psu.wattage >= required_wattage
    ]

    if not valid_psus:
        return None

    return min(valid_psus, key=lambda psu: psu.price)


def calculate_build_price(cpu, gpu, motherboard, ram, storage, psu):
    """
    calculates the build prices
    :param cpu: object CPU
    :param gpu: object GPU
    :param motherboard: object Motherboard
    :param ram: object RAM
    :param storage: object Storage
    :param psu: object PSU
    :return: total build price
    """
    return (
        cpu.price
        + gpu.price
        + motherboard.price
        + ram.price
        + storage.price
        + psu.price
    )


def is_build_in_budget_range(total_price, budget, budget_gap=300):
    """
    used to reccomend if price of build is within budget range
    :param total_price: totral price of build calcualted from 'def calculate_build_price'
    :param budget: budget of build based on user param
    :param budget_gap=300: how much cheaper than the budget the reccomended build can be
    :return minimum_price <= total_price <= budget: Boolean value of whether price of build is valid
    """
    minimum_price = max(0, budget - budget_gap)
    return minimum_price <= total_price <= budget


def generate_compatible_builds(
    cpus,
    gpus,
    motherboards,
    ram_list,
    storage_list,
    psus,
    budget,
    cpu_limit=40,
    gpu_limit=40,
    ram_limit=3,
    storage_limit=3,
    budget_gap=300
):
    
    """
    used to generate compatible PC builds based on user budget and component compatibility
    :param cpus: list of CPU objects loaded from CPU benchmark data
    :param gpus: list of GPU objects loaded from GPU benchmark data
    :param motherboards: list of motherboard objects used to match CPU socket and RAM type
    :param ram_list: list of RAM objects used to match motherboard RAM type
    :param storage_list: list of storage objects used for build storage options
    :param psus: list of PSU objects used to find a power supply that supports total wattage
    :param budget: maximum budget entered by the user
    :param cpu_limit=40: maximum number of top CPU options selected using the CPU heuristic
    :param gpu_limit=40: maximum number of top GPU options selected using the GPU heuristic
    :param ram_limit=3: maximum number of RAM options selected for each compatible motherboard
    :param storage_limit=3: maximum number of storage options selected for build generation
    :param budget_gap=300: how much cheaper than the budget the recommended build can be
    :return compatible_builds: list of valid PCBUILD objects that match compatibility, wattage, and budget rules
    """

    compatible_builds = []

    top_cpus = choose_top_cpus(cpus, budget, cpu_limit)
    top_gpus = choose_top_gpus(gpus, budget, gpu_limit)
    top_storage = choose_top_storage(storage_list, storage_limit)

    for cpu in top_cpus:
        motherboard = choose_best_motherboard(cpu, motherboards)

        if motherboard is None:
            continue

        top_ram = choose_top_ram(motherboard, ram_list, ram_limit)

        if not top_ram:
            continue

        for ram in top_ram:
            for storage in top_storage:
                for gpu in top_gpus:
                    total_wattage = calculate_total_wattage(
                        cpu,
                        gpu,
                        motherboard,
                        ram,
                        storage
                    )

                    psu = choose_best_psu(total_wattage, psus)

                    if psu is None:
                        continue

                    total_price = calculate_build_price(
                        cpu,
                        gpu,
                        motherboard,
                        ram,
                        storage,
                        psu
                    )

                    if not is_build_in_budget_range(total_price, budget, budget_gap):
                        continue

                    build = PCBUILD()
                    build.add_component(cpu)
                    build.add_component(gpu)
                    build.add_component(motherboard)
                    build.add_component(ram)
                    build.add_component(storage)
                    build.add_component(psu)

                    compatible_builds.append(build)

    return compatible_builds