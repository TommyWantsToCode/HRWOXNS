#!/usr/bin/env python3

import asyncio
import math

from array import array

# Edit this array to map the steering wheel keys to nintendo switch inputs 'wheel input': 'switch input'
# This can only change non-analog inputs (Note: Triggets on nintendo switch are not analog)
# Switch names: y, x, b, a, r, zr, minus, plus, r_stick, l_stick, home, capture, down, up, right, left, l, zl
RACING_WHEEL_CONTROLLER_MAPS = {
                                    'btn_menu':             'plus',
                                    'btn_change_view':      'minus',
                                    'btn_a':                'b',
                                    'btn_b':                'a',
                                    'btn_x':                'y',
                                    'btn_y':                'x',
                                    'btn_up':               'up',
                                    'btn_down':             'down',
                                    'btn_left':             'left',
                                    'btn_right':            'right',
                                    'btn_ldb':              'l_stick',
                                    'btn_rdb':              'r_stick',
                                    'btn_lb':               'l',
                                    'btn_rb':               'r',
                                    'pedal_brake':          'zl',
                                    'pedal_throttle':       'zr',
                                    'btn_start':            'capture',
                                    'btn_home':             'home'
                                } 

# Expected serial messages headers
RACING_WHEEL_HEADER_CONTROL_STATE = array('B', [32, 0])
RACING_WHEEL_HEADER_HOME_STATE = array('B', [7, 32])
RACING_WHEEL_HEADER_HEARTBEAT = array('B', [3, 32])

# Threshold for trigger, switch triggers are not analog (0 - 1024)
RACING_WHEEL_BRAKE_THRESHOLD = 512
RACING_WHEEL_THROTTLE_THRESHOLD = 512

from joycontrol.controller_state import ControllerState, button_push, button_press, button_release

# Simple interpolation
def lerp(a, b, percentage):
    return (percentage * a) + ((1 - percentage) * b)

# Translator between XBOX and Switch
class RacingWheel:

    def __init__(self, controller_state: ControllerState):

        # Saves controller state reference
        self.controller_state = controller_state

        # Centers stick and saves its reference
        self.controller_state.l_stick_state.set_center()
        self.controller_state.r_stick_state.set_center()
        self.stick = controller_state.l_stick_state

        # Calculates stick range
        calibration = self.stick.get_calibration()
        self.stick_maxUp = calibration.v_center + calibration.v_max_above_center
        self.stick_maxDown = calibration.v_center - calibration.v_max_below_center
        self.stick_maxRight = calibration.h_center + calibration.h_max_above_center
        self.stick_maxLeft = calibration.h_center - calibration.h_max_below_center
        self.stick_center_x =  int(lerp(self.stick_maxRight, self.stick_maxLeft, 0.5))
        self.stick_center_y = int(lerp(self.stick_maxUp, self.stick_maxDown, 0.5))

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
        self.pedal_brake = False
        self.pedal_throttle = False

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

    async def handleSteering(self, x, y):

        # Ensures controller conection via bluetooth
        await self.controller_state.connect()

        self.stick.set_h(x)
        self.stick.set_v(y)
        await asyncio.sleep(0) # HACK: It doesnt work with out this for some reason

    async def handleButton(self, btn_name, newStatus):

        # Only act if the new status is different
        if getattr(self, btn_name) != newStatus:

            # Saves the new state
            setattr(self, btn_name, newStatus)

            # Ensures controller conection via bluetooth
            await self.controller_state.connect()

            # Presses or releases button on nintendo
            if newStatus:
                await button_press(self.controller_state, RACING_WHEEL_CONTROLLER_MAPS[btn_name])
            else:
                await button_release(self.controller_state, RACING_WHEEL_CONTROLLER_MAPS[btn_name])

    async def handle(self, hexData):

        # Gets header from message
        hexHeader = hexData[0:2]

        # Detects message type
        if hexHeader == RACING_WHEEL_HEADER_CONTROL_STATE:

            # Reads raw steering value
            steerintByteA = hexData[10]
            steeringByteB = hexData[11]
            steering_raw_value = int(((steeringByteB & 0b01111111) << 8) | steerintByteA) / 0b1111111

            # Percentage from min to max of X axis
            steering_x_value = self.stick_center_x

            if steeringByteB & 0b10000000:
                steering_x_value = int(lerp(self.stick_center_x, self.stick_maxLeft, steering_raw_value))

            elif steeringByteB | steerintByteA:
                steering_x_value = int(lerp(self.stick_maxRight, self.stick_center_x, steering_raw_value))

            # Steers the wheel
            await self.handleSteering(steering_x_value, self.stick_center_y)

            # ABXY and action buttons except start
            hexData_abxy_actions = hexData[4];
            if hexData_abxy_actions != self.last_hexData_abxy_actions:
                self.last_hexData_abxy_actions = hexData_abxy_actions

                await self.handleButton('btn_menu', hexData_abxy_actions & 0b100)
                await self.handleButton('btn_change_view', hexData_abxy_actions & 0b1000)

                await self.handleButton('btn_a', hexData_abxy_actions & 0b10000)
                await self.handleButton('btn_b', hexData_abxy_actions & 0b100000)
                await self.handleButton('btn_x', hexData_abxy_actions & 0b1000000)
                await self.handleButton('btn_y', hexData_abxy_actions & 0b10000000)

            # Cross arrows and l/r buttons
            hexData_lr_dir = hexData[5];
            if hexData_lr_dir != self.last_hexData_lr_dir:
                self.last_hexData_lr_dir = hexData_lr_dir

                await self.handleButton('btn_up', hexData_lr_dir & 0b1)
                await self.handleButton('btn_down', hexData_lr_dir & 0b10)
                await self.handleButton('btn_left', hexData_lr_dir & 0b100)
                await self.handleButton('btn_right', hexData_lr_dir & 0b1000)

                await self.handleButton('btn_ldb', hexData_lr_dir & 0b10000)
                await self.handleButton('btn_rdb', hexData_lr_dir & 0b100000)
                await self.handleButton('btn_lb', hexData_lr_dir & 0b1000000)
                await self.handleButton('btn_rb', hexData_lr_dir & 0b10000000)

            # Pedals with analog to digital conversion
            await self.handleButton('pedal_brake', hexData[7] * 256 + hexData[6] > RACING_WHEEL_BRAKE_THRESHOLD)
            await self.handleButton('pedal_throttle', hexData[9] * 256 + hexData[8] > RACING_WHEEL_BRAKE_THRESHOLD)

            # Start button
            await self.handleButton('btn_start', hexData[18] & 0b1)

        elif hexHeader == RACING_WHEEL_HEADER_HOME_STATE:
            
            #Home button mapping
            await self.handleButton('btn_home', hexData[4] & 0b1)

        elif hexHeader != RACING_WHEEL_HEADER_HEARTBEAT:
            print("Unknown header from USB device: " + str(hexHeader) + " with data: " + str(hexData))