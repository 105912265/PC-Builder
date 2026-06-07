# Author: Kshitij Kshirsagar
# Filename: build_generator.py
# Last edited: 24/05/2026

from src.compatibility_checker import (
    calculate_total_wattage,
    is_psu_compatible
)
from pc_build import PCBUILD


def get_top_cpus(cpus, budget, limit=20):
    affordable_cpus = [
        cpu for cpu in cpus
        if cpu.price <= budget * 0.35
    ]

    affordable_cpus.sort(
        key=lambda cpu: cpu.cpu_mark / cpu.price,
        reverse=True
    )

    return affordable_cpus[:limit]


def get_top_gpus(gpus, budget, limit=20):
    affordable_gpus = [
        gpu for gpu in gpus
        if gpu.price <= budget * 0.50
    ]

    affordable_gpus.sort(
        key=lambda gpu: gpu.g3d_mark / gpu.price,
        reverse=True
    )

    return affordable_gpus[:limit]


def get_matching_motherboards(cpu, motherboards):
    return [
        motherboard for motherboard in motherboards
        if motherboard.socket == cpu.socket
    ]


def get_matching_ram(motherboard, ram_list):
    return [
        ram for ram in ram_list
        if ram.ram_type == motherboard.ram_type
    ]


def get_valid_psus(total_wattage, psus):
    return [
        psu for psu in psus
        if is_psu_compatible(total_wattage, psu)
    ]


def calculate_build_price(cpu, gpu, motherboard, ram, storage, psu):
    return (
        cpu.price
        + gpu.price
        + motherboard.price
        + ram.price
        + storage.price
        + psu.price
    )


def generate_compatible_builds(
    cpus,
    gpus,
    motherboards,
    ram_list,
    storage_list,
    psus,
    budget,
    cpu_limit=20,
    gpu_limit=20,
    max_builds=1000
):
    compatible_builds = []

    top_cpus = get_top_cpus(cpus, budget, cpu_limit)
    top_gpus = get_top_gpus(gpus, budget, gpu_limit)

    # Keep storage/RAM choices small and useful
    ram_list = sorted(ram_list, key=lambda ram: ram.size_gb / ram.price, reverse=True)[:5]
    storage_list = sorted(storage_list, key=lambda storage: storage.capacity_gb / storage.price, reverse=True)[:5]

    for cpu in top_cpus:
        matching_motherboards = get_matching_motherboards(cpu, motherboards)

        for motherboard in matching_motherboards:
            matching_ram = get_matching_ram(motherboard, ram_list)

            for gpu in top_gpus:
                for ram in matching_ram:
                    for storage in storage_list:

                        total_wattage = calculate_total_wattage(
                            cpu,
                            gpu,
                            motherboard,
                            ram,
                            storage
                        )

                        valid_psus = get_valid_psus(total_wattage, psus)

                        for psu in valid_psus:
                            total_price = calculate_build_price(
                                cpu,
                                gpu,
                                motherboard,
                                ram,
                                storage,
                                psu
                            )

                            if total_price > budget:
                                continue

                            build = PCBUILD()
                            build.add_component(cpu)
                            build.add_component(gpu)
                            build.add_component(motherboard)
                            build.add_component(ram)
                            build.add_component(storage)
                            build.add_component(psu)

                            compatible_builds.append(build)

                            if len(compatible_builds) >= max_builds:
                                return compatible_builds

    return compatible_builds