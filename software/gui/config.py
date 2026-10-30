# config.py
import os
import sys


APP_NAME = "HooverTron"
APP_DATA_FOLDER_NAME = "HooverTron Patients"


def get_resource_path(relative_path):
    """Get absolute path to a bundled resource for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def _ensure_directory(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_runtime_dir():
    """Return the folder beside the running app/exe."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def get_app_data_dir():
    return _ensure_directory(os.path.join(get_runtime_dir(), APP_DATA_FOLDER_NAME))


def get_drafts_dir():
    return _ensure_directory(os.path.join(get_app_data_dir(), "drafts"))


def get_settings_file_path():
    return os.path.join(get_app_data_dir(), "settings.json")


def get_documents_dir():
    return get_app_data_dir()


def get_patient_exports_dir():
    return get_app_data_dir()
