import csv
from cpu import CPU
from gpu import GPU
from ram import RAM
from storage import Storage
from psu import PSU

def read_files(file_path, object_type):
    items = []
    with open(file_path, 'r', encoding='utf8') as file:
        reader = csv.DictReader(file)

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
            else:
                raise ValueError(f"Unsupported object_type: {object_type}")

            items.append(item)

    return items