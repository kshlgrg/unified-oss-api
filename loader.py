import sys
import os
import importlib.util

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_from_init(module_path, class_name):
    """Load a class from a module's __init__.py"""
    init_path = os.path.join(BASE, module_path, "__init__.py")
    spec = importlib.util.spec_from_file_location(f"module_{class_name}", init_path)
    module = importlib.util.module_from_spec(spec)
    
    # Add parent directory to sys.path for relative imports
    parent = os.path.join(BASE, module_path)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    
    spec.loader.exec_module(module)
    return getattr(module, class_name)

# Load all classes
MaintainerDashboard = load_from_init("gh_maintainer_dashboard", "MaintainerDashboard")
MilestoneCelebrations = load_from_init("milestone-celebrations/app", "MilestoneCelebrations")
CookieLickingDetector = load_from_init("cookie-licking-detector/app", "CookieLickingDetector")
OSSDiscoveryEngine = load_from_init("oss-discovery-engine/app", "OSSDiscoveryEngine")
