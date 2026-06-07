from src.data_loader import load_cpus, load_gpus, load_motherboards, load_psu, load_ram, load_storage

cpus = load_cpus("data/cpu_bench.csv")
gpus = load_gpus("data/gpu_bench.csv")
rams = load_ram("data/ram.csv")
psus = load_psu("data/psus.csv")
motherboards = load_motherboards("data/motherboards.csv")
storages = load_storage("data/storage.csv")

print(f"Loaded {len(cpus)} CPUs")
print(f"Loaded {len(gpus)} GPUs")
print(f"Loaded {len(rams)} RAM entries")
print(f"Loaded {len(psus)} PSUs")
print(f"Loaded {len(motherboards)} motherboards")
print(f"Loaded {len(storages)} storage entries")

