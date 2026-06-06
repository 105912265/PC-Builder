# Author: Kshitij Kshirsagar
# Filename: data_loader.py
# Last edited: 06/06/2026

import csv

from components.cpu import CPU
from components.gpu import GPU


def load_cpus(file_path):
    cpus = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cpu = CPU(
                row["name"],
                float(row["price"]),
                int(float(row["wattage"])),
                int(float(row["cpu_mark"])),
                int(float(row["single_thread_score"])),
                float(row["power_perf"]),
                int(float(row["cores"])),
                row["socket"]
            )

            cpus.append(cpu)

    return cpus


def load_gpus(file_path):
    gpus = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            gpu = GPU(
                row["name"],
                float(row["price"]),
                int(float(row["wattage"])),
                int(float(row["g3d_mark"])),
                int(float(row["g2d_mark"])),
                float(row["power_perf"])
            )

            gpus.append(gpu)

    return gpus