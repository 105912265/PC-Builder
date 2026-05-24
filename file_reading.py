import csv
from cpu import CPU
from gpu import GPU
from ram import RAM
from storage import Storage
from psu import PSU
from motherboard import Motherboard

def read_files(file_path, object_type, build_type):
    items = []
    budget = ""
    if build_type == 1:
        budget = "cheap"
    elif build_type == 2:
        budget = "okay"
    elif build_type == 3:
        budget = "expensive"

    with open(file_path, 'r', encoding='utf8') as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        for row in reader:
            if object_type is CPU:
                item = CPU(row['name'], row['brand'], float(row['price']), int(row['cores']), row['socket'])
            elif object_type is GPU:
                item = GPU(row['name'], row['brand'], float(row['price']), int(row['vram_gb']))
            elif object_type is PSU:
                item = PSU(row['name'], row['brand'], float(row['price']), int(row['wattage']))
            elif object_type is RAM:
                item = RAM(row['name'], row['brand'], float(row['price']), int(row['capacity_gb']), row['type'], row['speed_mhz'])
            elif object_type is Storage:
                item = Storage(row['name'], row['brand'], float(row['price']), row['type'], int(row['capacity_gb']))
            elif object_type is Motherboard:
                item = Motherboard(row['name'], row['brand'], float(row['price']), row['socket'], row['ram_type'], row['wifi'])
            else:
                raise ValueError(f"Unsupported object_type: {object_type}")

            # Motherboards don't have build_type in the CSV; include all
            if object_type is Motherboard:
                items.append(item)
                continue

            build_value = row.get('build_type', '').strip().lower()
            if build_value == budget:
                items.append(item)

    return items