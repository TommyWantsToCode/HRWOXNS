#!/usr/bin/env python3

import asyncio

from array import array

# Expected serial messages headers
RACING_WHEEL_HEADER_CONTROL_STATE = array('B', [32, 0])
RACING_WHEEL_HEADER_HOME_STATE = array('B', [7, 32])
RACING_WHEEL_HEADER_HEARTBEAT = array('B', [3, 32])

from joycontrol.controller_state import ControllerState, button_push, button_press, button_release

class RacingWheel:

    def __init__(self, controller_state: ControllerState):

        # Saves controller state reference
        self.controller_state = controller_state

        # ABXY buttons
        self.last_btn_status_abxy = 0
        self.btn_a = False
        self.btn_b = False
        self.btn_x = False
        self.btn_y = False

        # CROSS buttons
        self.last_btn_status_cross = 0
        self.btn_up = False
        self.btn_down = False
        self.btn_left = False
        self.btn_right = False

        # HOME button
        self.btn_home = False

        # LSB is the same as break, RSB is the same as throttle
        self.pedal_brake = float(0)
        self.pedal_throttle = float(0)

        # L and R buttons
        self.last_btn_status_lr = 0
        self.btn_ldb = False
        self.btn_lb = False
        self.btn_rb = False
        self.btn_rdb = False

        # Action buttons
        self.last_btn_status_action = 0
        self.btn_change_view = False
        self.btn_menu = False
        self.btn_start = False

    async def handleButton(self, btn_name, mappedNintendoButtons, newStatus):

        # Only act if the new status is different
        if getattr(self, btn_name) != newStatus:

            # Saves the new state
            setattr(self, btn_name, newStatus)

            # Ensures controller conection via bluetooth
            await controller_state.connect()

            # Presses or releases button on nintendo
            if newStatus:
                await button_press(controller_state, mappedNintendoButtons)
            else:
                await button_release(controller_state, mappedNintendoButtons)
            print(newStatus)

    async def handle(self, hexData):

        # Gets header from message
        hexHeader = hexData[0:2]

        # Detects message type
        if hexHeader == RACING_WHEEL_HEADER_CONTROL_STATE:
            print("controller state")
        elif hexHeader == RACING_WHEEL_HEADER_HOME_STATE:
            
            await handleButton(self, 'btn_home', 'home', hexData[4] & 0b1)

        elif hexHeader != RACING_WHEEL_HEADER_HEARTBEAT:
            print("Unknown header from USB device: " + str(hexHeader) + " with data: " + str(hexData))