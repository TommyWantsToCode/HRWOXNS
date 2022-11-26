#!/usr/bin/env python3

import argparse
import asyncio
import logging
import os

from aioconsole import ainput

from joycontrol import logging_default as log, utils
from joycontrol.command_line_interface import ControllerCLI
from joycontrol.controller import Controller
from joycontrol.controller_state import ControllerState, button_push, button_press, button_release
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server


# Hold a button command
async def hold(*args):

    await controller_state.connect()
    await button_press(controller_state, *args)

# Release a button command
async def release(*args):

    await controller_state.connect()
    await button_release(controller_state, *args)

# Configure control, set up bluetooth, start listening and forwarding input
async def main():

    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    # Create memory containing default controller stick calibration
    spi_flash = FlashMemory()

    # Get controller name to emulate from arguments
    controller = Controller.from_arg('PRO_CONTROLLER')

    # prepare the the emulated controller
    factory = controller_protocol_factory(controller, spi_flash=spi_flash)
    ctl_psm, itr_psm = 17, 19
    transport, protocol = await create_hid_server(factory, reconnect_bt_addr='58:B0:3E:07:25:14',
                                                        ctl_psm=ctl_psm,
                                                        itr_psm=itr_psm
                                                       )

    controller_state = protocol.get_controller_state()

    # validates controller state
    if controller_state.get_controller() != Controller.PRO_CONTROLLER:
        raise ValueError('This script only works with the Pro Controller!')

    # prints buttons for ease
    print('Available buttons: ' + str(controller_state.button_state.get_available_buttons()))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())