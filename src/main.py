import os
from pathlib import Path

sdk_root = Path(__file__).resolve().parents[1] / "RoboMaster-SDK"

_ffmpeg_dll = os.add_dll_directory(str(sdk_root / "lib" / "libmedia_codec" / "src" / "ffmpeg-dll"))

_opus_dll = os.add_dll_directory(str(sdk_root / "lib" / "libmedia_codec" / "src" / "opus-dll"))

from robomaster import robot  # noqa: E402

print("RoboMaster imported successfully")
