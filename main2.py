# Author: Kshitij Kshirsagar
# Filename: main2.py
# Last edited: 18/06/2026

from pc_build import PCBUILD

from src.data_loader import (
    load_cpus,
    load_gpus,
    load_motherboards,
    load_psu,
    load_ram,
    load_storage
)

from src.build_generator import (
    recommend_three_builds,
    find_compatible_motherboards,
    find_compatible_ram,
    find_affordable_storage,
    final_build_is_compatible
)


def get_number_input(message, minimum=0):
    """
    used to receive and validate a number entered by the user
    :param message: input message shown to user
    :param minimum: smallest accepted number
    :return value: validated float value
    """
    while True:
        try:
            value = float(input(message))

            if value < minimum:
                print(
                    f"Please enter a value of at least {minimum}."
                )
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_menu_choice(message, options):
    """
    used to receive a valid numbered choice from the user
    :param message: heading shown before menu options
    :param options: list of available choices
    :return: selected option value
    """
    print(message)

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        try:
            choice = int(input("Select an option: "))

            if 1 <= choice <= len(options):
                return options[choice - 1]

            print("Please select a valid option number.")

        except ValueError:
            print("Please enter a number.")


def choose_component(message, components):
    """
    used to let the user choose one component from a filtered list
    :param message: heading shown before component options
    :param components: list of compatible component objects
    :return: component selected by user or None
    """
    if not components:
        return None

    print(f"\n{message}")

    for index, component in enumerate(components, start=1):
        print(
            f"{index}. {component.name} - ${component.price:.2f}"
        )

    while True:
        try:
            choice = int(input("Select an option: "))

            if 1 <= choice <= len(components):
                return components[choice - 1]

            print("Please select a valid option number.")

        except ValueError:
            print("Please enter a number.")


cpus = load_cpus("data/cpu_bench.csv")
gpus = load_gpus("data/gpu_bench.csv")
rams = load_ram("data/ram.csv")
psus = load_psu("data/psus.csv")
motherboards = load_motherboards("data/motherboards.csv")
storages = load_storage("data/storage.csv")

budget = get_number_input("What is your total PC budget? $", minimum=1)

preferred_cpu_brand = get_menu_choice("\nChoose your CPU preference:", ["Any", "AMD", "Intel"])
preferred_gpu_brand = get_menu_choice("\nChoose your GPU preference:", ["Any", "NVIDIA", "Radeon"])

recommendations = recommend_three_builds(
    cpus=cpus,
    gpus=gpus,
    motherboards=motherboards,
    ram_list=rams,
    storage_list=storages,
    psus=psus,
    budget=budget,
    preferred_cpu_brand=preferred_cpu_brand,
    preferred_gpu_brand=preferred_gpu_brand
)

if not recommendations:
    print(
        "\nNo core component recommendations were found "
        "for the selected budget and preferences."
    )

    raise SystemExit

print("\nRecommended Core Component Options")

for index, recommendation in enumerate(
    recommendations,
    start=1
):
    print(f"\nOption {index}: {recommendation['type']}")
    print(recommendation["description"])

    print(
        f"CPU: {recommendation['cpu'].name} - "
        f"${recommendation['cpu'].price:.2f}"
    )

    print(
        f"GPU: {recommendation['gpu'].name} - "
        f"${recommendation['gpu'].price:.2f}"
    )

    print(
        f"PSU: {recommendation['psu'].name} - "
        f"${recommendation['psu'].price:.2f}"
    )

    print(
        f"Suggested motherboard: "
        f"{recommendation['motherboard'].name}"
    )

    print(
        f"Suggested RAM: "
        f"{recommendation['ram'].name}"
    )

    print(
        f"Suggested storage: "
        f"{recommendation['storage'].name}"
    )

    print(
        f"Estimated complete price: "
        f"${recommendation['estimated_total']:.2f}"
    )

    difference = (
        recommendation["estimated_total"]
        - budget
    )

    if difference > 0:
        print(f"Above budget by: ${difference:.2f}")
    else:
        print(f"Below budget by: ${abs(difference):.2f}")

print("\nChoose a recommended core component option:")

while True:
    try:
        recommendation_choice = int(input("Select an option: "))

        if 1 <= recommendation_choice <= len(recommendations):
            selected_recommendation = recommendations[recommendation_choice - 1]
            break

        print("Please select a valid option number.")

    except ValueError:
        print("Please enter a number.")

selected_cpu = selected_recommendation["cpu"]
selected_gpu = selected_recommendation["gpu"]
selected_psu = selected_recommendation["psu"]

remaining_budget = budget - selected_recommendation["core_price"]

compatible_motherboards = find_compatible_motherboards(selected_cpu, motherboards, remaining_budget)

selected_motherboard = choose_component("Choose a compatible motherboard:", compatible_motherboards)

if selected_motherboard is None:
    print(
        "No compatible motherboards were found "
        "within the remaining budget."
    )

    raise SystemExit

remaining_budget -= selected_motherboard.price

compatible_ram = find_compatible_ram(selected_motherboard, rams, remaining_budget)

selected_ram = choose_component("Choose compatible RAM:", compatible_ram)

if selected_ram is None:
    print(
        "No compatible RAM was found "
        "within the remaining budget."
    )

    raise SystemExit

remaining_budget -= selected_ram.price

affordable_storage = find_affordable_storage(storages, remaining_budget)

selected_storage = choose_component("Choose a storage option:", affordable_storage)

if selected_storage is None:
    print(
        "No storage options were found "
        "within the remaining budget."
    )

    raise SystemExit

final_build = PCBUILD()

final_build.add_component(selected_cpu)
final_build.add_component(selected_gpu)
final_build.add_component(selected_motherboard)
final_build.add_component(selected_ram)
final_build.add_component(selected_storage)
final_build.add_component(selected_psu)

is_compatible = final_build_is_compatible(
    selected_cpu,
    selected_gpu,
    selected_psu,
    selected_motherboard,
    selected_ram,
    selected_storage
)

if not is_compatible:
    print("\nThe final build contains incompatible components.")
    raise SystemExit

print("\nFinal PC Build")
final_price = final_build.total_price()
price_difference = final_price - budget

if price_difference > 0:
    print(
        f"\nThis build is ${price_difference:.2f} "
        f"above your budget."
    )
else:
    print(
        f"\nYou have ${abs(price_difference):.2f} "
        f"remaining in your budget."
    )

final_build.save_build()
print("\nBuild saved to output/build.txt")