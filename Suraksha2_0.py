import streamlit as st
import os
import shutil
import base64

# --- Helpers ---------------------------------------------------------------
def safe_filename(filename: str) -> str:
    # Remove any path components
    return os.path.basename(filename)

def parse_custom_params(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
        else:
            out[line] = True
    return out

def simulate_obfuscation(input_file_path, output_file_path, params):
    """
    For prototype: copy file. Real implementation: run clang/llvm toolchain & passes.
    """
    shutil.copy(input_file_path, output_file_path)

    report = {
        "input_parameters": params,
        "output_file_size": os.path.getsize(output_file_path),
        "method_of_obfuscation": f"Simulated Obfuscation (Level: {params.get('obfuscation_level')})",
        "bogus_code_generated": "Approximately 50 lines (simulated)",
        "cycles_completed": 3,
        "string_obfuscations": 5,
        "fake_loops_inserted": 2,
    }
    return report, output_file_path

# --- Streamlit UI ---------------------------------------------------------
st.set_page_config(page_title="LLVM Code Obfuscator Prototype", layout="wide")

# Basic CSS (ok for prototype; selectors may not always match Streamlit internals)
st.markdown(
    """
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    /* Prototype-only styles; Streamlit classnames change over time. */
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("LLVM Code Obfuscator Prototype")

# Sidebar inputs
st.sidebar.header("Input Parameters")

uploaded_file = st.sidebar.file_uploader("Upload C/C++ source file", type=["c", "cpp", "h"])
platform = st.sidebar.selectbox("Target Platform", ["Windows", "Linux"])
obfuscation_level = st.sidebar.slider("Obfuscation Level (1-10)", 1, 10, 5)
custom_params_text = st.sidebar.text_area("Custom Parameters (e.g., key1=value1)", "bogus_code_amount=50\nstring_encrypt=true")

# Ensure directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

if st.sidebar.button("Start Obfuscation"):
    if uploaded_file is None:
        st.error("Please upload a C or C++ source file to proceed.")
    else:
        try:
            # Sanitize filename
            original_name = safe_filename(uploaded_file.name)
            base_name, ext = os.path.splitext(original_name)
            # Keep original extension in saved upload to avoid confusion
            saved_input_path = os.path.join("uploads", f"{base_name}{ext}")

            # Save uploaded file
            with open(saved_input_path, "wb") as f:
                f.write(uploaded_file.read())

            # Prepare output filename (don't smash dots, keep base name)
            out_ext = ".exe" if platform == "Windows" else ".bin"
            # Use informative output filename
            output_file_name = f"obfuscated_{base_name}{out_ext}"
            output_file_path = os.path.join("outputs", output_file_name)

            # Parse custom params
            parsed_params = parse_custom_params(custom_params_text)

            params = {
                "platform": platform,
                "obfuscation_level": obfuscation_level,
                "custom_params_raw": custom_params_text,
                "custom_params": parsed_params,
                "original_filename": original_name,
            }

            # Run simulation
            report, obfuscated_path = simulate_obfuscation(saved_input_path, output_file_path, params)

            # Display report
            st.header("Obfuscation Report")
            st.subheader("1. Input Parameters")
            st.json(report["input_parameters"])

            st.subheader("2. Output File Attributes")
            st.write(f"- Size: {report['output_file_size']} bytes")
            st.write(f"- Method of Obfuscation: {report['method_of_obfuscation']}")

            st.subheader("3. Amount of Bogus Code Generated")
            st.write(report["bogus_code_generated"])

            st.subheader("4. Number of Cycles of Obfuscation Completed")
            st.write(f"{report['cycles_completed']} cycles")

            st.subheader("5. Number of String Obfuscations/Encryptions Done")
            st.write(f"{report['string_obfuscations']} strings obfuscated")

            st.subheader("6. Number of Fake Loops Inserted")
            st.write(f"{report['fake_loops_inserted']} fake loops")

            # Provide download (read bytes to be safe)
            with open(obfuscated_path, "rb") as f:
                data_bytes = f.read()
            st.download_button(
                label="Download Obfuscated File",
                data=data_bytes,
                file_name=os.path.basename(obfuscated_path),
                mime="application/octet-stream"
            )

        except Exception as e:
            st.error(f"An error occurred during obfuscation: {e}")

st.markdown("---")
st.write("This is a generic prototype. Obfuscation is simulated for demonstration.")
