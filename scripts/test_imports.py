libs = [
    'torch', 'torch_geometric', 'pymc', 'lime', 'shap', 'graphviz', 
    'matplotlib', 'numpy', 'pandas', 'scipy', 'sklearn', ]

# Function to check if a library can be imported
def check_library(lib_name):
    try:
        __import__(lib_name)
        try:
            ver = __import__(lib_name).__version__
        except AttributeError:
            ver = "unknown"
        print(f"{lib_name} version {ver} is installed.")
    except ImportError:
        print(f"ERROR: {lib_name} is NOT installed or cannot be loaded.")

print("Checking for installed libraries...")
for lib in libs:
    check_library(lib)
