#!/usr/bin/env python3

import asyncio

# Expected serial messages headers
RACING_WHEEL_HEADER_CONTROL_STATE = '\x20\x00';
RACING_WHEEL_HEADER_HOME_STATE = '\x07\x20';
RACING_WHEEL_HEADER_HEARTBEAT = '\x03\x20';

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
        self.last_btn_status_home = 0
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

    async def handle(self, hexData):

        # Gets header from message
        hexHeader = hexData[0:4]

        # Detects message type
        if hexHeader == RACING_WHEEL_HEADER_CONTROL_STATE:
            print("controller state")
        elif hexHeader == RACING_WHEEL_HEADER_HOME_STATE:
            print("home state")
        elif hexHeader == RACING_WHEEL_HEADER_HEARTBEAT:
            print("Heartbeat")