import csv
from components.cpu import CPU
from components.gpu import GPU
from components.ram import RAM
from components.storage import Storage
from components.psu import PSU
from components.motherboard import Motherboard

def read_files(file_path, object_type, build_type):
    items = []
    total_wattage = 0
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
                item = CPU(row['name'], row['brand'], float(row['price']), int(row['wattage']), int(row['cores']), row['socket'])
                total_wattage += int(row['wattage'])
            elif object_type is GPU:
                item = GPU(row['name'], row['brand'], float(row['price']), int(row['wattage']), int(row['vram_gb']))
                total_wattage += int(row['wattage'])
            elif object_type is PSU:
                item = PSU(row['name'], row['brand'], float(row['price']), int(row['wattage']))
            elif object_type is RAM:
                item = RAM(row['name'], row['brand'], float(row['price']), int(row['wattage']), int(row['capacity_gb']), row['type'], row['speed_mhz'])
                total_wattage += int(row['wattage'])
            elif object_type is Storage:
                item = Storage(row['name'], row['brand'], float(row['price']), int(row['wattage']),row['type'], int(row['capacity_gb']))
                total_wattage += int(row['wattage'])
            elif object_type is Motherboard:
                item = Motherboard(row['name'], row['brand'], float(row['price']), int(row['wattage']), row['socket'], row['ram_type'], row['wifi'])
                total_wattage += int(row['wattage'])
            else:
                raise ValueError(f"Unsupported object_type: {object_type}")

            # Motherboards don't have build_type in the CSV; include all
            if object_type is Motherboard:
                items.append(item)
                continue

            if object_type is PSU:
                items.append(item)
                continue

            build_value = row.get('build_type', '').strip().lower()
            if build_value == budget:
                items.append(item)

    return items