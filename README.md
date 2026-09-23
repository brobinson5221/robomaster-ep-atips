# RoboMaster EP ATIPS

Scripts in `src/` can import the robot API with:

```python
from robomaster_runtime import robot
```

The shared module registers the Windows DLL directories once per Python process,
before loading the SDK, and keeps the directory handles alive. It expects the
SDK's native libraries under `RoboMaster-SDK/lib/libmedia_codec/src/`.

For other SDK modules, import `robomaster_runtime` before importing from
`robomaster` so the DLL directories are registered first.
