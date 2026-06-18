# Author: Kshitij Kshirsagar
# Filename: main2.py
# Last edited: 07/06/2026

import csv

from src.data_loader import (
    load_cpus,
    load_gpus,
    load_motherboards,
    load_psu,
    load_ram,
    load_storage
)

from src.build_generator import generate_compatible_builds
from src.build_labeler import label_builds


cpus = load_cpus("data/cpu_bench.csv")
gpus = load_gpus("data/gpu_bench.csv")
rams = load_ram("data/ram.csv")
psus = load_psu("data/psus.csv")
motherboards = load_motherboards("data/motherboards.csv")
storages = load_storage("data/storage.csv")

budget = float(input("What is your budget? "))

builds = generate_compatible_builds(
    cpus,
    gpus,
    motherboards,
    rams,
    storages,
    psus,
    budget,
    cpu_limit=40,
    gpu_limit=40,
    ram_limit=3,
    storage_limit=3,
    budget_gap=300
)

print(f"Compatible builds found: {len(builds)}")

#if len(builds) > 0:
 #   print("\nFirst build:")
  #  print(builds[0].display_build())

with open("builds.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "CPU",
        "GPU",
        "Motherboard",
        "RAM",
        "Storage",
        "PSU",
        "Total Price",
        "Total Wattage"
    ])

    for build in builds:
        components = build.show_components()

        writer.writerow([
            components[0].name,
            components[1].name,
            components[2].name,
            components[3].name,
            components[4].name,
            components[5].name,
            build.total_price(),
            build.total_watts()
        ])

#print("Builds saved to builds.csv")

labelled_builds = label_builds(builds, "gaming")

for item in labelled_builds[:5]:
    print(item["build"].display_build())
    print(item["build"].total_price())
    print("Score:", item["score"])
    print("Label:", item["label"])
    print("----------------")