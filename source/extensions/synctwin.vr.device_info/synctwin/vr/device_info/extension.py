# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import omni.ext
import omni.ui as ui
import carb
from omni.kit.xr.core import (
    XRCore,
    XRCoreEventType,
    XRInputDevice,

)


# Any class derived from `omni.ext.IExt` in the top level module (defined in
# `python.modules` of `extension.toml`) will be instantiated when the extension
# gets enabled, and `on_startup(ext_id)` will be called. Later when the
# extension gets disabled on_shutdown() is called.
class DeviceInfoExtension(omni.ext.IExt):
    """This extension manages a simple counter UI."""
    # ext_id is the current extension id. It can be used with the extension
    # manager to query additional information, like where this extension is
    # located on the filesystem.
    def on_startup(self, _ext_id):
        """This is called every time the extension is activated."""
        print("[synctwin.vr.device_info] Extension startup")

        self._count = 0
        self._window = ui.Window(
            "SyncTwin VR Device Info", width=300, height=300
        )
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("- Device Info -", height=30)
                self._device_info = ui.Label("- need to start VR mode -")

        self.xr_enabled = False
        xr_core = XRCore.get_singleton()

        message_bus = xr_core.get_message_bus()
        self.xr_enabled_sub = message_bus.create_subscription_to_pop_by_type(XRCoreEventType.xr_enabled, self.on_xr_enable)
        self.xr_disabled_sub = message_bus.create_subscription_to_pop_by_type(XRCoreEventType.xr_disabled, self.on_xr_disable)
        self.update_device_info()


    def on_shutdown(self):
        """This is called every time the extension is deactivated. It is used
        to clean up the extension state."""
        print("[synctwin.vr.device_info] Extension shutdown")

    def on_xr_enable(self, event: XRCoreEventType):
        self.xr_enabled = True
        self.update_device_info()

    def on_xr_disable(self, event: XRCoreEventType):
        self.xr_enabled = False
        self.update_device_info()

    def update_device_info(self):
        if self.xr_enabled:
            self._device_info.text = "VR mode is enabled"
            xr_core = XRCore.get_singleton()
            num_devices = len(xr_core.get_all_input_devices())
            info = f"Number of devices: {num_devices}"
            for input_device in xr_core.get_all_input_devices():
                info += f"\n{input_device.get_name()}"
            self._device_info.text = info
        else:
            self._device_info.text = "- please start VR mode -"
