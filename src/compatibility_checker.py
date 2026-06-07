# Author: Kshitij Kshirsagar
# Filename: compatibility_checker.py
# Last edited: 07/06/2026


def is_cpu_motherboard_compatible(cpu, motherboard):
    return cpu.socket == motherboard.socket


def is_ram_motherboard_compatible(ram, motherboard):
    return ram.ram_type == motherboard.ram_type


def calculate_total_price(cpu, gpu, motherboard, ram, storage, psu):
    return (
        cpu.price
        + gpu.price
        + motherboard.price
        + ram.price
        + storage.price
        + psu.price
    )


def calculate_total_wattage(cpu, gpu, motherboard, ram, storage):
    return (
        cpu.wattage
        + gpu.wattage
        + motherboard.wattage
        + ram.wattage
        + storage.wattage
    )


def is_psu_compatible(total_wattage, psu):
    required_wattage = total_wattage * 1.3 # *1.3 to protect system from hardware spikes and future upgrades
    return psu.wattage >= required_wattage


def is_within_budget(total_price, budget):
    return total_price <= budget


def is_build_compatible(cpu, gpu, motherboard, ram, storage, psu, budget):
    if not is_cpu_motherboard_compatible(cpu, motherboard):
        #print("cpu and mobo not")
        return False

    if not is_ram_motherboard_compatible(ram, motherboard):
        #print("ram and mobo not")
        return False

    total_wattage = calculate_total_wattage(cpu, gpu, motherboard, ram, storage)

    if not is_psu_compatible(total_wattage, psu):
        #print("psu not")
        return False

    total_price = calculate_total_price(cpu, gpu, motherboard, ram, storage, psu)

    if not is_within_budget(total_price, budget):
        #print("poor")
        return False

    return True