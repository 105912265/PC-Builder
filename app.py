# Author: Kshitij Kshirsagar
# Filename: app.py
# Last edited: 22/06/2026

import textwrap
import streamlit as st

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

from src.association_recommender import (
    create_component_item,
    get_suggested_component_names,
    load_association_rules,
    recommend_associated_parts,
    reorder_components_by_rules
)


st.set_page_config(
    page_title="Smart PC Builder",
    page_icon="🖥️",
    layout="wide"
)


def load_css(css_file):
    """
    used to load an external CSS file into the Streamlit app
    :param css_file: location of the css file
    :return: None
    """
    with open(css_file, "r", encoding="utf8") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )

def render_html(html_string):
    """
    Cleans up string indentation manually and renders raw HTML safely.
    """
    cleaned_lines = [line.strip() for line in html_string.strip().split("\n")]
    inline_html = "".join(cleaned_lines)
    st.markdown(inline_html, unsafe_allow_html=True)  


load_css("assets/style.css")


@st.cache_data
def load_component_data():
    """
    used to load all component CSV data once for the Streamlit app
    :return: loaded component lists
    """
    cpus = load_cpus("data/cpu_bench.csv")
    gpus = load_gpus("data/gpu_bench.csv")
    rams = load_ram("data/ram.csv")
    psus = load_psu("data/psus.csv")
    motherboards = load_motherboards("data/motherboards.csv")
    storages = load_storage("data/storage.csv")

    return (
        cpus,
        gpus,
        rams,
        psus,
        motherboards,
        storages
    )


@st.cache_data
def load_rules():
    """
    used to load trained association rules once for the Streamlit app
    :return: association rules model
    """
    return load_association_rules()


def format_component(component):
    """
    used to format a component for dropdown display
    :param component: selected component object
    :return: formatted component name and price
    """
    return f"{component.name} - ${component.price:.2f}"


def calculate_power_score(recommendation):
    """
    used to calculate a simple gaming power score for a recommended PC build
    :param recommendation: build recommendation dictionary
    :return: power score from 0 to 100
    """
    cpu = recommendation["cpu"]
    gpu = recommendation["gpu"]

    cpu_score = min(
        cpu.cpu_mark / 50000,
        1
    )

    gpu_score = min(
        gpu.g3d_mark / 28000,
        1
    )

    power_score = (
        cpu_score * 0.35
        + gpu_score * 0.65
    ) * 100

    return round(power_score)


def get_power_label(power_score):
    """
    used to convert a power score into a user-friendly label
    :param power_score: power score from 0 to 100
    :return: power label
    """
    if power_score >= 85:
        return "Extreme"

    if power_score >= 70:
        return "High"

    if power_score >= 55:
        return "Strong"

    if power_score >= 40:
        return "Moderate"

    return "Entry"


def display_landing_section():
    """
    used to display the main landing section
    :return: None
    """
    render_html("""
        <div class="hero-card">
            <div class="hero-small-text">Custom PC recommendations</div>
            <h1>Smart PC Builder</h1>
            <p class="hero-subtitle">
                Choose a budget and let the system recommend gaming PC builds using
                benchmark data, compatibility checking, and association-rule suggestions.
            </p>
            <a class="hero-button" href="#build-your-pc">Start Your Build</a>
        </div>
    """)


def display_trust_section():
    """
    used to display system trust cards
    :return: None
    """
    st.markdown("## Why gamers can trust this system")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_html("""
            <div class="trust-card">
                <div class="trust-number">01</div>
                <h4>Benchmark based</h4>
                <p>CPU and GPU choices are ranked using performance and price data.</p>
            </div>
        """)

    with col2:
        render_html("""
            <div class="trust-card">
                <div class="trust-number">02</div>
                <h4>Compatibility checked</h4>
                <p>Motherboard socket, RAM type, and PSU wattage are validated.</p>
            </div>
        """)

    with col3:
        render_html("""
            <div class="trust-card">
                <div class="trust-number">03</div>
                <h4>Smarter pairing</h4>
                <p>Association rules prioritise parts commonly paired together.</p>
            </div>
        """)

    with col4:
        render_html("""
            <div class="trust-card">
                <div class="trust-number">04</div>
                <h4>Budget aware</h4>
                <p>Builds are grouped into value, balanced, and performance options.</p>
            </div>
        """)


def display_pc_choice_card(recommendation, budget, index):
    """
    used to display a simple PC choice card without making specs the main focus
    """
    power_score = calculate_power_score(recommendation)
    power_label = get_power_label(power_score)
    difference = recommendation["estimated_total"] - budget

    if difference > 0:
        budget_text = f"${difference:.2f} over budget"
        budget_class = "warning-text"
    else:
        budget_text = f"${abs(difference):.2f} under budget"
        budget_class = "positive-text"

    render_html(f"""
        <div class="pc-choice-card">
            <div class="pc-choice-title">{recommendation['type']}</div>
            <div class="pc-choice-price">${recommendation['estimated_total']:.2f}</div>
            <div class="pc-choice-power">{power_label} Power</div>
            <div class="mini-meter">
                <div class="mini-meter-fill" style="width: {power_score}%;"></div>
            </div>
            <p>{recommendation['description']}</p>
            <p class="{budget_class}">{budget_text}</p>
        </div>
    """)

    if st.button(f"Select {recommendation['type']}", key=f"select_build_{index}"):
        st.session_state["selected_recommendation_index"] = index
        st.rerun()


def display_speedometer(power_score):
    """
    used to display a speedometer-style power indicator
    """
    rotation = -90 + (power_score * 1.8)
    power_label = get_power_label(power_score)

    render_html(f"""
        <div class="speedometer-card">
            <h2>Power Indicator</h2>
            <div class="speedometer">
                <div class="speedometer-arc"></div>
                <div class="speedometer-needle" style="transform: rotate({rotation}deg);"></div>
                <div class="speedometer-center"></div>
                <div class="speedometer-score">{power_score}</div>
                <div class="speedometer-label">{power_label} Power</div>
            </div>
            <p class="speedometer-note">
                This score is based mainly on GPU benchmark performance, with CPU power also included.
            </p>
        </div>
    """)


def build_association_items(
    cpu=None,
    gpu=None,
    psu=None,
    motherboard=None,
    ram=None
):
    """
    used to create selected association rule items from chosen components
    :return: list of association rule item strings
    """
    selected_items = []

    if cpu is not None:
        selected_items.append(
            create_component_item(
                "CPU",
                cpu.name
            )
        )

    if gpu is not None:
        selected_items.append(
            create_component_item(
                "GPU",
                gpu.name
            )
        )

    if psu is not None:
        selected_items.append(
            create_component_item(
                "PSU",
                psu.name
            )
        )

    if motherboard is not None:
        selected_items.append(
            create_component_item(
                "Motherboard",
                motherboard.name
            )
        )

    if ram is not None:
        selected_items.append(
            create_component_item(
                "RAM",
                ram.name
            )
        )

    return selected_items


def show_selected_core_build(
    recommendation
):
    """
    used to show selected core build specs only after user selects a PC
    :param recommendation: selected build recommendation
    :return: None
    """
    with st.expander(
        "View selected PC core components"
    ):
        st.write(
            f"**CPU:** {recommendation['cpu'].name} "
            f"- ${recommendation['cpu'].price:.2f}"
        )

        st.write(
            f"**GPU:** {recommendation['gpu'].name} "
            f"- ${recommendation['gpu'].price:.2f}"
        )

        st.write(
            f"**PSU:** {recommendation['psu'].name} "
            f"- ${recommendation['psu'].price:.2f}"
        )

        st.write(
            f"**Estimated complete price:** "
            f"${recommendation['estimated_total']:.2f}"
        )


def show_final_build(
    final_build,
    budget
):
    """
    used to display the final build summary
    :param final_build: completed PCBUILD object
    :param budget: user's budget
    :return: None
    """
    final_price = final_build.total_price()
    price_difference = final_price - budget

    st.markdown(
        textwrap.dedent("""
        <div class="final-card">
        <h2>Final PC Build</h2>
        """),
        unsafe_allow_html=True
    )

    for component in final_build.show_components():
        st.markdown(
            textwrap.dedent(f"""
            <div class="component-line">
                {component.display_info()}
            </div>
            """),
            unsafe_allow_html=True
        )

    st.markdown(
        textwrap.dedent(f"""
        <h3>Total price: ${final_price:.2f}</h3>
        <h3>Total wattage: {final_build.total_watts()}W</h3>
        """),
        unsafe_allow_html=True
    )

    if price_difference > 0:
        st.warning(
            f"This build is ${price_difference:.2f} above your budget."
        )
    else:
        st.success(
            f"You have ${abs(price_difference):.2f} remaining in your budget."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


def main():
    """
    used to run the Streamlit PC builder application
    :return: None
    """
    display_landing_section()
    display_trust_section()

    st.markdown(
        textwrap.dedent("""
        <div class="section-card" id="build-your-pc">
            <h2>Build your PC</h2>
            <p>
                Select your budget and brand preferences in the sidebar.
                The system will generate three PC options focused on power and price.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

    try:
        (
            cpus,
            gpus,
            rams,
            psus,
            motherboards,
            storages
        ) = load_component_data()

    except FileNotFoundError as error:
        st.error(error)
        st.stop()

    try:
        rules = load_rules()

    except FileNotFoundError:
        st.error(
            "Association rules model was not found. "
            "Run `py src/train_association_rules.py` first."
        )
        st.stop()

    st.sidebar.header("Build Preferences")

    budget = st.sidebar.number_input(
        "Total PC Budget ($)",
        min_value=500.0,
        max_value=5000.0,
        value=1500.0,
        step=50.0
    )

    preferred_cpu_brand = st.sidebar.selectbox(
        "CPU Preference",
        [
            "Any",
            "AMD",
            "Intel"
        ]
    )

    preferred_gpu_brand = st.sidebar.selectbox(
        "GPU Preference",
        [
            "Any",
            "NVIDIA",
            "Radeon"
        ]
    )

    generate_button = st.sidebar.button(
        "Generate Recommendations"
    )

    if generate_button:
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

        st.session_state["recommendations"] = recommendations
        st.session_state["selected_recommendation_index"] = 0

    if "recommendations" not in st.session_state:
        st.info(
            "Enter your preferences in the sidebar and click "
            "**Generate Recommendations**."
        )
        return

    recommendations = st.session_state["recommendations"]

    if not recommendations:
        st.error(
            "No build recommendations were found for the selected budget and preferences."
        )
        return

    st.markdown("## Choose Your PC")

    recommendation_columns = st.columns(
        len(recommendations)
    )

    for index, recommendation in enumerate(
        recommendations
    ):
        with recommendation_columns[index]:
            display_pc_choice_card(
                recommendation,
                budget,
                index
            )

    if "selected_recommendation_index" not in st.session_state:
        st.session_state["selected_recommendation_index"] = 0

    selected_recommendation_index = st.session_state[
        "selected_recommendation_index"
    ]

    selected_recommendation = recommendations[
        selected_recommendation_index
    ]

    st.markdown("## Selected PC")

    selected_power_score = calculate_power_score(
        selected_recommendation
    )

    display_speedometer(
        selected_power_score
    )

    show_selected_core_build(
        selected_recommendation
    )

    selected_cpu = selected_recommendation["cpu"]
    selected_gpu = selected_recommendation["gpu"]
    selected_psu = selected_recommendation["psu"]

    maximum_final_price = max(
        budget,
        selected_recommendation["estimated_total"]
    )

    remaining_budget = (
        maximum_final_price
        - selected_recommendation["core_price"]
    )

    st.markdown("## Customise Supporting Parts")

    st.markdown(
        textwrap.dedent(f"""
        <div class="section-card">
            <h3>Available for motherboard, RAM and storage: ${remaining_budget:.2f}</h3>
            <p>
                Association rules place commonly paired parts first.
                Compatibility checks still remove invalid parts.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

    selected_association_items = build_association_items(
        cpu=selected_cpu,
        gpu=selected_gpu,
        psu=selected_psu
    )

    motherboard_rule_suggestions = recommend_associated_parts(
        selected_items=selected_association_items,
        rules=rules,
        required_component_type="Motherboard",
        limit=5
    )

    compatible_motherboards = find_compatible_motherboards(
        selected_cpu,
        motherboards,
        remaining_budget
    )

    compatible_motherboards = reorder_components_by_rules(
        compatible_motherboards,
        motherboard_rule_suggestions
    )

    suggested_motherboard_names = get_suggested_component_names(
        motherboard_rule_suggestions
    )

    if not compatible_motherboards:
        st.error(
            "No compatible motherboards were found."
        )
        return

    motherboard_options = [
        format_component(motherboard)
        for motherboard in compatible_motherboards
    ]

    selected_motherboard_label = st.selectbox(
        "Choose Motherboard",
        motherboard_options
    )

    selected_motherboard = compatible_motherboards[
        motherboard_options.index(
            selected_motherboard_label
        )
    ]

    if selected_motherboard.name in suggested_motherboard_names:
        st.success(
            "This motherboard was prioritised by association rules."
        )

    remaining_after_motherboard = (
        remaining_budget
        - selected_motherboard.price
    )

    selected_association_items = build_association_items(
        cpu=selected_cpu,
        gpu=selected_gpu,
        psu=selected_psu,
        motherboard=selected_motherboard
    )

    ram_rule_suggestions = recommend_associated_parts(
        selected_items=selected_association_items,
        rules=rules,
        required_component_type="RAM",
        limit=5
    )

    compatible_ram = find_compatible_ram(
        selected_motherboard,
        rams,
        remaining_after_motherboard
    )

    compatible_ram = reorder_components_by_rules(
        compatible_ram,
        ram_rule_suggestions
    )

    suggested_ram_names = get_suggested_component_names(
        ram_rule_suggestions
    )

    if not compatible_ram:
        st.error(
            "No compatible RAM was found."
        )
        return

    ram_options = [
        format_component(ram)
        for ram in compatible_ram
    ]

    selected_ram_label = st.selectbox(
        "Choose RAM",
        ram_options
    )

    selected_ram = compatible_ram[
        ram_options.index(
            selected_ram_label
        )
    ]

    if selected_ram.name in suggested_ram_names:
        st.success(
            "This RAM was prioritised by association rules."
        )

    remaining_after_ram = (
        remaining_after_motherboard
        - selected_ram.price
    )

    selected_association_items = build_association_items(
        cpu=selected_cpu,
        gpu=selected_gpu,
        psu=selected_psu,
        motherboard=selected_motherboard,
        ram=selected_ram
    )

    storage_rule_suggestions = recommend_associated_parts(
        selected_items=selected_association_items,
        rules=rules,
        required_component_type="Storage",
        limit=5
    )

    affordable_storage = find_affordable_storage(
        storages,
        remaining_after_ram
    )

    affordable_storage = reorder_components_by_rules(
        affordable_storage,
        storage_rule_suggestions
    )

    suggested_storage_names = get_suggested_component_names(
        storage_rule_suggestions
    )

    if not affordable_storage:
        st.error(
            "No storage options were found."
        )
        return

    storage_options = [
        format_component(storage)
        for storage in affordable_storage
    ]

    selected_storage_label = st.selectbox(
        "Choose Storage",
        storage_options
    )

    selected_storage = affordable_storage[
        storage_options.index(
            selected_storage_label
        )
    ]

    if selected_storage.name in suggested_storage_names:
        st.success(
            "This storage option was prioritised by association rules."
        )

    final_build = PCBUILD()

    final_build.add_component(
        selected_cpu
    )

    final_build.add_component(
        selected_gpu
    )

    final_build.add_component(
        selected_motherboard
    )

    final_build.add_component(
        selected_ram
    )

    final_build.add_component(
        selected_storage
    )

    final_build.add_component(
        selected_psu
    )

    is_compatible = final_build_is_compatible(
        selected_cpu,
        selected_gpu,
        selected_psu,
        selected_motherboard,
        selected_ram,
        selected_storage
    )

    if not is_compatible:
        st.error(
            "The final build contains incompatible components."
        )
        return

    show_final_build(
        final_build,
        budget
    )

    if st.button("Save Build"):
        final_build.save_build()
        st.success(
            "Build saved to output/build.txt"
        )


if __name__ == "__main__":
    main()