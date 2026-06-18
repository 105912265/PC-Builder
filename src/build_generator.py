# Author: Kshitij Kshirsagar
# Filename: build_generator.py
# Last edited: 07/06/2026

from pc_build import PCBUILD
from src.compatibility_checker import calculate_total_wattage


def cpu_score(cpu, budget):
    """
    used to score CPUs based on both performance and value
    :param cpu: CPU object
    :param budget: user budget
    :return score: weighted CPU score
    """
    value_score = cpu.cpu_mark / cpu.price
    performance_score = cpu.cpu_mark

    if budget >= 2500:
        return performance_score * 0.75 + value_score * 500 * 0.25
    else:
        return performance_score * 0.40 + value_score * 500 * 0.60


def gpu_score(gpu, budget):
    """
    used to score GPUs based on both performance and value
    :param gpu: GPU object
    :param budget: user budget
    :return score: weighted GPU score
    """
    value_score = gpu.g3d_mark / gpu.price
    performance_score = gpu.g3d_mark

    if budget >= 2500:
        return performance_score * 0.80 + value_score * 500 * 0.20
    else:
        return performance_score * 0.45 + value_score * 500 * 0.55


def choose_top_cpus(cpus, budget, limit=60):
    """
    used to choose the best CPU candidates before generating builds
    :param cpus: list of CPU objects
    :param budget: user budget
    :param limit: maximum number of CPUs to keep
    :return affordable_cpus: list of selected CPU objects
    """
    affordable_cpus = [
        cpu for cpu in cpus
        if cpu.price <= budget * 0.40
    ]

    affordable_cpus.sort(
        key=lambda cpu: cpu_score(cpu, budget),
        reverse=True
    )

    return affordable_cpus[:limit]


def choose_top_gpus(gpus, budget, limit=60):
    """
    used to choose the best GPU candidates before generating builds
    :param gpus: list of GPU objects
    :param budget: user budget
    :param limit: maximum number of GPUs to keep
    :return affordable_gpus: list of selected GPU objects
    """
    affordable_gpus = [
        gpu for gpu in gpus
        if gpu.price <= budget * 0.70
    ]

    affordable_gpus.sort(
        key=lambda gpu: gpu_score(gpu, budget),
        reverse=True
    )

    return affordable_gpus[:limit]


def choose_top_motherboards(cpu, motherboards, limit=3):
    """
    used to choose compatible motherboards for a CPU
    :param cpu: CPU object
    :param motherboards: list of motherboard objects
    :param limit: maximum number of motherboards to keep
    :return matching_motherboards: list of compatible motherboard objects
    """
    matching_motherboards = [
        motherboard for motherboard in motherboards
        if motherboard.socket == cpu.socket
    ]

    matching_motherboards.sort(key=lambda motherboard: motherboard.price)

    return matching_motherboards[:limit]


def choose_top_ram(motherboard, ram_list, limit=4):
    """
    used to choose compatible RAM for a motherboard
    :param motherboard: motherboard object
    :param ram_list: list of RAM objects
    :param limit: maximum number of RAM options to keep
    :return matching_ram: list of compatible RAM objects
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


def choose_top_storage(storage_list, limit=4):
    """
    used to choose storage options based on capacity per dollar
    :param storage_list: list of storage objects
    :param limit: maximum number of storage options to keep
    :return storage_list: list of selected storage objects
    """
    storage_list.sort(
        key=lambda storage: storage.capacity_gb / storage.price,
        reverse=True
    )

    return storage_list[:limit]


def choose_valid_psus(total_wattage, psus, limit=3):
    """
    used to choose valid PSUs for the build wattage
    :param total_wattage: wattage of CPU, GPU, motherboard, RAM and storage
    :param psus: list of PSU objects
    :param limit: maximum number of PSU options to keep
    :return valid_psus: list of PSU objects that can power the build
    """
    required_wattage = total_wattage * 1.3

    valid_psus = [
        psu for psu in psus
        if psu.wattage >= required_wattage
    ]

    valid_psus.sort(key=lambda psu: psu.price)

    return valid_psus[:limit]


def calculate_build_price(cpu, gpu, motherboard, ram, storage, psu):
    """
    used to calculate total build price
    :return total_price: total price of all selected components
    """
    return (
        cpu.price
        + gpu.price
        + motherboard.price
        + ram.price
        + storage.price
        + psu.price
    )


def is_build_in_budget_range(total_price, budget, budget_gap=None):
    """
    used to recommend if price of build is within budget range
    :param total_price: total price of build calculated from 'def calculate_build_price'
    :param budget: budget of build based on user input
    :param budget_gap: how much cheaper than the budget the recommended build can be
    :return: Boolean value of whether price of build is valid
    """
    if budget_gap is None:
        budget_gap = max(300, budget * 0.30)

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
    cpu_limit=60,
    gpu_limit=60,
    motherboard_limit=3,
    ram_limit=4,
    storage_limit=4,
    psu_limit=3,
    budget_gap=None
):
    """
    used to generate compatible PC builds based on user budget and component compatibility
    :param cpus: list of CPU objects loaded from CPU benchmark data
    :param gpus: list of GPU objects loaded from GPU benchmark data
    :param motherboards: list of motherboard objects used to match CPU socket and RAM type
    :param ram_list: list of RAM objects used to match motherboard RAM type
    :param storage_list: list of storage objects used for build storage options
    :param psus: list of PSU objects used to find power supplies that support total wattage
    :param budget: maximum budget entered by the user
    :param cpu_limit: maximum number of CPU options selected
    :param gpu_limit: maximum number of GPU options selected
    :param motherboard_limit: maximum number of compatible motherboards selected per CPU
    :param ram_limit: maximum number of RAM options selected per motherboard
    :param storage_limit: maximum number of storage options selected
    :param psu_limit: maximum number of valid PSU options selected per build
    :param budget_gap: how much cheaper than the budget the recommended build can be
    :return compatible_builds: list of valid PCBUILD objects
    """
    compatible_builds = []

    top_cpus = choose_top_cpus(cpus, budget, cpu_limit)
    top_gpus = choose_top_gpus(gpus, budget, gpu_limit)
    top_storage = choose_top_storage(storage_list, storage_limit)

    for cpu in top_cpus:
        top_motherboards = choose_top_motherboards(cpu, motherboards, motherboard_limit)

        if not top_motherboards:
            continue

        for motherboard in top_motherboards:
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

                        valid_psus = choose_valid_psus(total_wattage, psus, psu_limit)

                        if not valid_psus:
                            continue

                        for psu in valid_psus:
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