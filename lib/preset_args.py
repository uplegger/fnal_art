from pathlib import Path


def preset_args(source_path):
    if (Path(source_path) / "CMakePresets.json").exists():
        return ["--preset", "default"]
    return []
