from cpu import CPU
from gpu import GPU
from ram import RAM
from storage import Storage
from psu import PSU
from file_reading import read_files

cpu_list = read_files('data/cpus.csv', CPU)
gpu_list = read_files('data/gpus.csv', GPU)
psu_list = read_files('data/psus.csv', PSU)
ram_list = read_files('data/ram.csv', RAM)
storage_list = read_files('data/storage.csv', Storage)

