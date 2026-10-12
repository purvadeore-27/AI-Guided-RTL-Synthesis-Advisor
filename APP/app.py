import streamlit as st
import pandas as pd
import sys
import subprocess
from pathlib import Path

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_SCRIPT = PROJECT_ROOT / "FEATURE_EXTRACTION" / "extract_features.py"
DATASET_FILE = PROJECT_ROOT / "DATA" / "raw" / "synthesis_results.csv"
PYTHON_EXE = Path(sys.executable)
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI RTL Synthesis Advisor",
    page_icon="⚡",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("⚡ AI-Guided RTL Synthesis Advisor")

st.markdown(
    """
    **Early prediction of FPGA implementation characteristics from VHDL RTL**

    Analyze RTL features, explore synthesis measurements, and obtain
    experimental machine-learning predictions.
    """
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "RTL Analyzer",
        "Dataset Explorer",
        "About Project"
    ]
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("Project Dashboard")

    col1, col2, col3 = st.columns(3)

    total_designs = 0

    if DATASET_FILE.exists():
        try:
            dataset = pd.read_csv(DATASET_FILE)
            total_designs = len(dataset)
        except Exception:
            dataset = pd.DataFrame()
    else:
        dataset = pd.DataFrame()

    col1.metric("Recorded Designs", total_designs)
    col2.metric("FPGA Platform", "Spartan-6")
    col3.metric("Synthesis Tool", "Xilinx ISE 14.7")

    st.subheader("System Workflow")

    st.markdown(
        """
        1. Upload a VHDL source file.
        2. Extract structural RTL features.
        3. Predict delay using a trained ML model.
        4. Examine feature importance and optimization opportunities.
        5. Compare predictions with actual ISE synthesis measurements.
        """
    )

    st.info(
        "Predictions are experimental. Model reliability must be "
        "evaluated using unseen designs."
    )

# --------------------------------------------------
# RTL ANALYZER
# --------------------------------------------------

elif page == "RTL Analyzer":

    st.header("RTL Feature Analyzer")

    st.write(
        "Upload a VHDL file to extract its structural features."
    )

    uploaded_file = st.file_uploader(
        "Upload VHDL source",
        type=["vhd", "vhdl"]
    )

    if uploaded_file is not None:

        st.success(f"Selected file: {uploaded_file.name}")

        if st.button("Analyze RTL", type="primary"):

            if not FEATURE_SCRIPT.exists():
                st.error(
                    f"Feature extractor not found: {FEATURE_SCRIPT}"
                )

            else:
                temp_dir = PROJECT_ROOT / "APP" / "uploads"
                temp_dir.mkdir(parents=True, exist_ok=True)

                vhdl_path = temp_dir / uploaded_file.name
                vhdl_path.write_bytes(uploaded_file.getvalue())

                try:
                    result = subprocess.run(
                        [
                            str(PYTHON_EXE),
                            str(FEATURE_SCRIPT),
                            str(vhdl_path)
                        ],
                        cwd=str(PROJECT_ROOT),
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    if result.returncode == 0:
                        st.subheader("RTL Feature Extraction Results")
                        st.code(result.stdout, language="text")

                        if result.stderr.strip():
                            with st.expander("Additional output"):
                                st.text(result.stderr)

                    else:
                        st.error("Feature extraction failed.")
                        st.code(result.stderr or result.stdout)

                except subprocess.TimeoutExpired:
                    st.error("Feature extraction timed out.")

                except Exception as exc:
                    st.error(f"Unexpected error: {exc}")

# --------------------------------------------------
# DATASET EXPLORER
# --------------------------------------------------

elif page == "Dataset Explorer":

    st.header("Synthesis Dataset")

    if DATASET_FILE.exists():

        try:
            dataset = pd.read_csv(DATASET_FILE)

            st.write(f"Total recorded designs: {len(dataset)}")

            st.dataframe(
                dataset,
                use_container_width=True,
                hide_index=True
            )

            if "worst_delay_ns" in dataset.columns:
                st.subheader("Measured Delay by Design")

                chart_data = dataset[
                    ["design_name", "worst_delay_ns"]
                ].set_index("design_name")

                st.bar_chart(chart_data)

        except Exception as exc:
            st.error(f"Could not read dataset: {exc}")

    else:
        st.warning("The synthesis dataset was not found.")

# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

elif page == "About Project":

    st.header("About the Project")

    st.markdown(
        """
        ### AI-Guided RTL Synthesis Advisor

        **Objective:** Investigate whether machine-learning models can
        predict FPGA implementation characteristics from VHDL RTL
        features before running synthesis.

        **Target FPGA:** Xilinx Spartan-6 XC6SLX45-CSG324-3

        **Synthesis tool:** Xilinx ISE 14.7

        **Technology stack:**
        - VHDL
        - Python
        - Pandas
        - Scikit-learn
        - Streamlit
        - Xilinx ISE

        **Planned capabilities:**
        - RTL feature extraction
        - Delay prediction
        - Resource-utilization prediction
        - Feature-importance analysis
        - Rule-based RTL optimization suggestions
        - Comparison against measured synthesis results
        """
    )

st.divider()

st.caption("AI RTL Synthesis Advisor | Research Prototype")