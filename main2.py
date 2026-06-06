from src.data_loader import load_cpus, load_gpus

cpus = load_cpus("data/cpu_bench.csv")
gpus = load_gpus("data/gpu_bench.csv")

print(f"Loaded {len(cpus)} CPUs")
print(f"Loaded {len(gpus)} GPUs")

print(cpus[0].display_info())
print(gpus[0].display_info())