"""Configure native DLL loading before importing the RoboMaster SDK."""

import os
from pathlib import Path

_sdk_root = Path(__file__).resolve().parents[1] / "RoboMaster-SDK"
_codec_root = _sdk_root / "lib" / "libmedia_codec" / "src"

# Keep these handles alive: closing them removes the DLL search directories.
_dll_handles = [
    os.add_dll_directory(str(_codec_root / name)) for name in ("ffmpeg-dll", "opus-dll")
]

from robomaster import robot  # noqa: E402

__all__ = ["robot"]
