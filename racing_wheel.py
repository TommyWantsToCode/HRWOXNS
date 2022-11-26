#!/usr/bin/env python3

import asyncio

from array import array

# Expected serial messages headers
RACING_WHEEL_HEADER_CONTROL_STATE = array('B', [32, 0])
RACING_WHEEL_HEADER_HOME_STATE = array('B', [7, 32])
RACING_WHEEL_HEADER_HEARTBEAT = array('B', [3, 32])

from joycontrol.controller_state import ControllerState, button_push, button_press, button_release

# Translator between XBOX and Switch
# Switch names: y, x, b, a, r, zr, minus, plus, r_stick, l_stick, home, capture, down, up, right, left, l, zl
class RacingWheel:

    def __init__(self, controller_state: ControllerState):

        # Saves controller state reference
        self.controller_state = controller_state

        # ABXY buttons
        self.btn_a = False
        self.btn_b = False
        self.btn_x = False
        self.btn_y = False

        # CROSS buttons
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
        self.btn_ldb = False
        self.btn_lb = False
        self.btn_rb = False
        self.btn_rdb = False

        # Action buttons
        self.btn_change_view = False
        self.btn_menu = False
        self.btn_start = False

        # Useful bits to avoid unecesary computation
        self.last_hexData_lr_dir = 0
        self.last_hexData_abxy_actions = 0

    async def handleButton(self, btn_name, mappedNintendoButtons, newStatus):

        # Only act if the new status is different
        if getattr(self, btn_name) != newStatus:

            # Saves the new state
            setattr(self, btn_name, newStatus)

            # Ensures controller conection via bluetooth
            await self.controller_state.connect()

            # Presses or releases button on nintendo
            if newStatus:
                await button_press(self.controller_state, mappedNintendoButtons)
            else:
                await button_release(self.controller_state, mappedNintendoButtons)

    async def handle(self, hexData):

        # Gets header from message
        hexHeader = hexData[0:2]

        # Detects message type
        if hexHeader == RACING_WHEEL_HEADER_CONTROL_STATE:

            # ABXY and action buttons except start
            hexData_abxy_actions = hexData[4];
            if hexData_abxy_actions != self.last_hexData_abxy_actions:
                self.last_hexData_abxy_actions = hexData_abxy_actions

                await self.handleButton('btn_menu', 'plus', hexData_abxy_actions & 0b100)
                await self.handleButton('btn_change_view', 'minus', hexData_abxy_actions & 0b1000)

                await self.handleButton('btn_a', 'b', hexData_abxy_actions & 0b10000)
                await self.handleButton('btn_b', 'a', hexData_abxy_actions & 0b100000)
                await self.handleButton('btn_x', 'y', hexData_abxy_actions & 0b1000000)
                await self.handleButton('btn_y', 'x', hexData_abxy_actions & 0b10000000)

            # Cross arrows and l/r buttons
            hexData_lr_dir = hexData[5];
            if hexData_lr_dir != self.last_hexData_lr_dir:
                self.last_hexData_lr_dir = hexData_lr_dir

                await self.handleButton('btn_up', 'up', hexData_lr_dir & 0b1)
                await self.handleButton('btn_down', 'down', hexData_lr_dir & 0b10)
                await self.handleButton('btn_left', 'left', hexData_lr_dir & 0b100)
                await self.handleButton('btn_right', 'right', hexData_lr_dir & 0b1000)

                await self.handleButton('btn_ldb', 'l_stick', hexData_lr_dir & 0b10000)
                await self.handleButton('btn_rdb', 'r_stick', hexData_lr_dir & 0b100000)
                await self.handleButton('btn_lb', 'l', hexData_lr_dir & 0b1000000)
                await self.handleButton('btn_rb', 'r', hexData_lr_dir & 0b10000000)

            print(( int(hexData[6]) << 8) | hexData[7])


            # Start button
            await self.handleButton('btn_start', 'capture', hexData[18] & 0b1)

        elif hexHeader == RACING_WHEEL_HEADER_HOME_STATE:
            
            #Home button mapping
            await self.handleButton('btn_home', 'home', hexData[4] & 0b1)

        elif hexHeader != RACING_WHEEL_HEADER_HEARTBEAT:
            print("Unknown header from USB device: " + str(hexHeader) + " with data: " + str(hexData))