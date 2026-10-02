# RoboMaster EP ATIPS

Python scripts for trying DJI RoboMaster EP LEDs, blaster control, and robot
information through the RoboMaster SDK. The current runtime targets Windows and
connects to the robot in access point (AP) mode.

## Prerequisites

- Windows with 64-bit Python. [pyproject.toml](pyproject.toml) requires Python
  3.8 or newer; [.python-version](.python-version) selects 3.8 by default.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) and Git.
- A RoboMaster EP powered on in AP mode, with your computer connected to its
  Wi-Fi network.
- A local [RoboMaster SDK](https://github.com/dji-sdk/RoboMaster-SDK) checkout
  named `RoboMaster-SDK` in this project's root for the native DLLs.

## Quick start

Run these commands in PowerShell from the project root. Skip the clone command
if `RoboMaster-SDK` already exists.

```powershell
git clone https://github.com/dji-sdk/RoboMaster-SDK.git RoboMaster-SDK
uv sync --locked
```

`uv` installs the Python SDK from the Git source configured in `pyproject.toml`
and uses `uv.lock` for dependency resolution. The separate local SDK checkout
provides the DLL directories expected by the runtime; it is ignored by Git.

> [!WARNING]
> Running `src/main.py` operates the robot: it changes the LEDs and fires the
> blaster once. Prepare the robot and a safe firing area before running it.

```powershell
uv run python src/main.py
```

The script runs the LED sequence, runs the blaster sequence, then opens another
connection to print the robot version and serial number, select `GIMBAL_LEAD`
mode, and close that final connection. The LED sequence sets a warm color before
cycling through eight grayscale brightness levels, one second apart.

## Project layout

| File | Purpose |
| --- | --- |
| [src/main.py](src/main.py) | Runs the hardware sequences and reads robot information. |
| [src/led_tests.py](src/led_tests.py) | Defines `run_led_tests()` for the LED sequence. |
| [src/blaster_tests.py](src/blaster_tests.py) | Defines `run_blaster_tests()` for robot information, mode selection, and one blaster shot. |
| [src/robomaster_runtime.py](src/robomaster_runtime.py) | Registers Windows DLL directories before loading the robot API. |

The files named `*_tests.py` are hardware routines, with no standalone entry
points or automated test runner. Their functions each create a robot connection
and currently do not close it explicitly.

## SDK imports and native libraries

Scripts in `src/` can import the robot API with:

```python
from robomaster_runtime import robot
```

The shared module registers the Windows DLL directories once per Python process,
before loading the SDK, and keeps the directory handles alive. It expects the
SDK's native libraries under `RoboMaster-SDK/lib/libmedia_codec/src/`.

For other SDK modules, import `robomaster_runtime` before importing from
`robomaster` so the DLL directories are registered first.

```python
from robomaster_runtime import robot
from robomaster import led
```

All current connections use `initialize(conn_type="ap")`. There are no
environment variables or separate connection configuration files; connection
mode is set in the scripts.

## Development

`uv sync --locked` also installs the default development dependency group.
Run lint and formatting checks without connecting to the robot:

```powershell
uv run ruff check src
uv run ruff format --check src
```

The repository configures Ruff in `pyproject.toml` and a Commitizen commit-message
hook in [.pre-commit-config.yaml](.pre-commit-config.yaml). To enable the hook:

```powershell
uv run pre-commit install --hook-type commit-msg
```

## Troubleshooting

- **Missing DLL directory:** Check that both
  `RoboMaster-SDK/lib/libmedia_codec/src/ffmpeg-dll/` and
  `RoboMaster-SDK/lib/libmedia_codec/src/opus-dll/` exist. Dependency installation
  alone does not create this local checkout.
- **DLL load failure:** Use 64-bit Python with the SDK's Windows native libraries.
  The runtime calls `os.add_dll_directory`, so it requires Windows.
- **Connection failure:** Check that the robot is powered on in AP mode and the
  computer is connected to its Wi-Fi network. See the
  [RoboMaster Developer Guide](https://robomaster-dev.rtfd.io/) for SDK setup and
  connection details.
