import shutil
import subprocess
import platform
import pytest


OS = platform.system()  # "Windows", "Darwin", "Linux"


def can_run(cmd, version_arg="--version"):
    """
    Check whether a command exists in PATH and runs successfully.
    """
    if shutil.which(cmd) is None:
        return False

    try:
        subprocess.run(
            [cmd, version_arg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=5,
        )
        return True
    except Exception:
        return False


def require_any(commands, name):
    """
    Passes if ANY command in list works.
    """
    for cmd, arg in commands:
        if can_run(cmd, arg):
            return
    pytest.fail(
        f"{name} is not installed or not available in PATH.\n"
        f"Tried: {', '.join(cmd for cmd, _ in commands)}"
    )


def test_pixi_installed():
    require_any(
        commands=[("pixi", "--version")],
        name="pixi"
    )


def test_uv_installed():
    require_any(
        commands=[("uv", "--version")],
        name="uv"
    )


def test_git_installed():
    require_any(
        commands=[("git", "--version")],
        name="git"
    )


def test_qgis_installed():
    if OS == "Windows":
        candidates = [
            ("qgis-bin", "--version"),
            ("qgis", "--version"),
        ]
    elif OS == "Darwin":  # macOS
        candidates = [
            ("qgis", "--version"),
            ("/Applications/QGIS.app/Contents/MacOS/QGIS", "--version"),
        ]
    else:  # Linux
        candidates = [
            ("qgis", "--version"),
            ("qgis-bin", "--version"),
        ]

    require_any(candidates, name="QGIS")

