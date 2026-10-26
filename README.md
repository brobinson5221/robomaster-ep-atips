# RoboMaster EP ATIPS

Python hardware experiments for the DJI RoboMaster EP: distance-guided chassis
movement, gimbal and blaster control, LED feedback, and a polar distance scan.
The current application connects in access point (AP) mode and uses Windows
native libraries from the RoboMaster SDK.

## Prerequisites

- Windows with 64-bit Python. [pyproject.toml](pyproject.toml) declares Python
  3.8 or newer; [.python-version](.python-version) selects 3.8.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) and Git.
- A powered-on RoboMaster EP in AP mode, with the computer connected to its
  Wi-Fi network and a distance sensor available as the first sensor reading.
- The SDK's native DLLs in a local `RoboMaster-SDK` checkout, as described below.
- A desktop session capable of displaying a Matplotlib plot.

## Quick start

From the project root, run these commands in PowerShell. Skip the clone if the
`RoboMaster-SDK` directory already exists.

```powershell
git clone https://github.com/dji-sdk/RoboMaster-SDK.git RoboMaster-SDK
uv sync --locked
```

The Python SDK is installed from the Git source configured in
[pyproject.toml](pyproject.toml), with dependency versions recorded in
[uv.lock](uv.lock). The separate local checkout supplies the native DLL
directories used by the runtime and is ignored by Git.

> [!WARNING]
> Running the application moves the chassis and gimbal and can fire the blaster
> multiple times. Prepare a clear movement area and safe firing targets before
> starting. Closing the scan plot allows the final aiming and firing step to run.

```powershell
uv run python src/main.py
```

## What the application does

[src/main.py](src/main.py) opens one AP connection, prints the robot version and
serial number, selects `CHASSIS_LEAD` mode, and centers the gimbal. It then:

1. Runs the chassis routine with red LEDs. While readings exceed 360 mm, it
   commands movement at `x=-0.1`. If a subsequent reading drops below 360 mm,
   it stops, switches to `FREE` mode, and fires once at each of two gimbal poses:
   `(pitch=0, yaw=90)` and `(pitch=20, yaw=-90)`.
2. Centers the gimbal and restores `CHASSIS_LEAD` after that firing sequence.
   With green LEDs, it commands `x=0.1` for one second per counted movement
   iteration, then stops and sets blue LEDs. This return is based on loop counts,
   rather than measured position.
3. Commands scan angles from -180 through 175 degrees in 5-degree steps,
   retaining distance readings between 100 and 4,000 mm.
4. Displays a polar plot in meters. Nearby samples are joined when angle,
   range-jump, and physical-separation limits allow; the nearest reading is
   marked with a red star.
5. After the plot closes, sets yellow LEDs, aims at the nearest recorded angle,
   and fires once. If the scan has no valid readings, this final shot is skipped.

The connection is closed in a `finally` block after initialization. The current
entry point does not run the separate LED brightness or standalone blaster
routines.

## Configuration

Settings are constants and arguments in the source; there is no environment
variable or command-line configuration layer.

| Setting | Location | Default |
| --- | --- | --- |
| Connection mode | [src/main.py](src/main.py) | `conn_type="ap"` |
| Chassis distance threshold | [src/tests/chassis_tests.py](src/tests/chassis_tests.py) | `DISTANCE_LIMIT = 360` mm |
| Sensor wait timeout | [src/tests/distance_sensor_tests.py](src/tests/distance_sensor_tests.py) | `read_distance(..., timeout=5)` seconds |
| Scan range and step | [src/sensor_mapping/data_collecting.py](src/sensor_mapping/data_collecting.py) | `range(-180, 180, 5)` degrees |
| Accepted scan distances | [src/sensor_mapping/data_collecting.py](src/sensor_mapping/data_collecting.py) | 100–4,000 mm |
| Plot connection limits | [src/sensor_mapping/data_collecting.py](src/sensor_mapping/data_collecting.py) | 5° angle gap, 500 mm point gap, 300 mm range jump |

The `DISTANCE_LIMIT = 403` constant in `main.py` is unused; change the chassis
module's threshold to affect movement. Distance reads use the first sensor's
next update and return `None` on timeout. Scan readings are kept in memory;
the application does not save measurements or plots automatically.

## Project layout

| Path | Purpose |
| --- | --- |
| [src/main.py](src/main.py) | Connects the robot and orchestrates movement, scanning, plotting, and firing. |
| [src/robomaster_runtime.py](src/robomaster_runtime.py) | Registers Windows DLL directories before importing the robot API. |
| [src/sensor_mapping/data_collecting.py](src/sensor_mapping/data_collecting.py) | Collects scan data, draws the polar plot, and fires toward the nearest reading. |
| [src/tests/chassis_tests.py](src/tests/chassis_tests.py) | Provides chassis motion routines, including obstacle response with the blaster. |
| [src/tests/distance_sensor_tests.py](src/tests/distance_sensor_tests.py) | Reads distance updates with a timeout and unsubscribes afterward. |
| [src/tests/led_tests.py](src/tests/led_tests.py) | Runs a warm-color and grayscale LED sequence. |
| [src/tests/blaster_tests.py](src/tests/blaster_tests.py) | Fires the blaster once. |

The functions in `src/tests/` are hardware routines that accept an existing
`ep_robot` connection. They have no standalone entry points and are not an
automated unit-test suite.

## Development

`uv sync --locked` includes the default development dependencies. Run the
configured Ruff checks without operating the robot:

```powershell
uv run ruff check src
uv run ruff format --check src
```

To enable the Conventional Commits message hook configured in
[.pre-commit-config.yaml](.pre-commit-config.yaml):

```powershell
uv run pre-commit install --hook-type commit-msg
```

For new hardware scripts, load the shared runtime before other SDK imports so
the DLL search paths are registered first:

```python
from robomaster_runtime import robot
from robomaster import led
```

The runtime keeps the DLL-directory handles alive for the life of the process.

## Troubleshooting

- **Missing DLL directory or DLL load failure:** Check that
  `RoboMaster-SDK/lib/libmedia_codec/src/ffmpeg-dll/` and
  `RoboMaster-SDK/lib/libmedia_codec/src/opus-dll/` exist and contain the Windows
  native libraries. Installing Python dependencies alone does not create the
  local checkout. The runtime uses `os.add_dll_directory` and requires Windows.
- **Connection failure:** Check robot power, AP mode, and the computer's Wi-Fi
  connection. Consult the [RoboMaster Developer Guide](https://robomaster-dev.rtfd.io/)
  for SDK and connection setup.
- **Missing scan points:** Readings that time out or fall outside 100–4,000 mm
  are excluded. Verify the sensor and inspect its readings before running the
  full movement sequence.
- **Application appears paused at the plot:** The plot is shown before final
  aiming and firing; close its window to continue.
