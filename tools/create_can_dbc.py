from collections import OrderedDict
from itertools import chain

import cantools.database.can as can
from cantools.database import dump_file
from cantools.database.conversion import BaseConversion
from odrive.enums import *


def enum_choices(enum_type):
    choices = OrderedDict((item.value, item.name) for item in enum_type)
    if hasattr(enum_type, 'NONE') and enum_type.NONE.value not in choices:
        choices = OrderedDict([(enum_type.NONE.value, enum_type.NONE.name), *choices.items()])
    return choices


def signal(
    name,
    start,
    length,
    *,
    receivers=None,
    is_signed=False,
    is_float=False,
    scale=1,
    offset=0,
    unit=None,
    choices=None,
):
    conversion = BaseConversion.factory(
        scale=scale,
        offset=offset,
        choices=OrderedDict(choices) if choices is not None else None,
        is_float=is_float,
    )
    return can.Signal(
        name,
        start,
        length,
        is_signed=is_signed,
        conversion=conversion,
        receivers=receivers,
        unit=unit,
    )


messages = []
nodes = [can.Node('Master')]
buses = [can.Bus('ODrive', baudrate=100000)]

for axis_id in range(0, 8):
    axis_node = can.Node(f"ODrive_Axis{axis_id}")
    nodes.append(axis_node)

    axis_messages = [
        can.Message(
            0x001,
            "Heartbeat",
            8,
            [
                signal("Axis_Error", 0, 32, receivers=['Master'], choices=enum_choices(AxisError)),
                signal("Axis_State", 32, 8, receivers=['Master'], choices=enum_choices(AxisState)),
                signal("Motor_Error_Flag", 40, 1, receivers=['Master']),
                signal("Encoder_Error_Flag", 48, 1, receivers=['Master']),
                signal("Controller_Error_Flag", 56, 1, receivers=['Master']),
                signal("Trajectory_Done_Flag", 63, 1, receivers=['Master']),
            ],
            send_type='cyclic',
            cycle_time=100,
            senders=[axis_node.name],
        ),
        can.Message(
            0x003,
            "Get_Motor_Error",
            8,
            [signal("Motor_Error", 0, 32, receivers=['Master'], choices=enum_choices(MotorError))],
            senders=[axis_node.name],
        ),
        can.Message(
            0x004,
            "Get_Encoder_Error",
            8,
            [signal("Encoder_Error", 0, 32, receivers=['Master'], choices=enum_choices(EncoderError))],
            senders=[axis_node.name],
        ),
        can.Message(
            0x005,
            "Get_Sensorless_Error",
            8,
            [signal("Sensorless_Error", 0, 32, receivers=['Master'], choices=enum_choices(SensorlessEstimatorError))],
            senders=[axis_node.name],
        ),
        can.Message(
            0x006,
            "Set_Axis_Node_ID",
            8,
            [signal("Axis_Node_ID", 0, 32, receivers=[axis_node.name])],
            senders=['Master'],
        ),
        can.Message(
            0x007,
            "Set_Axis_State",
            8,
            [signal("Axis_Requested_State", 0, 32, receivers=[axis_node.name], choices=enum_choices(AxisState))],
            senders=['Master'],
        ),
        can.Message(
            0x009,
            "Get_Encoder_Estimates",
            8,
            [
                signal("Pos_Estimate", 0, 32, is_float=True, receivers=['Master'], unit='rev'),
                signal("Vel_Estimate", 32, 32, is_float=True, receivers=['Master'], unit='rev/s'),
            ],
            senders=[axis_node.name],
            send_type='cyclic',
            cycle_time=10,
        ),
        can.Message(
            0x00A,
            "Get_Encoder_Count",
            8,
            [
                signal("Shadow_Count", 0, 32, receivers=['Master'], unit='counts'),
                signal("Count_in_CPR", 32, 32, receivers=['Master'], unit='counts'),
            ],
            senders=[axis_node.name],
        ),
        can.Message(
            0x00B,
            "Set_Controller_Mode",
            8,
            [
                signal("Control_Mode", 0, 32, receivers=[axis_node.name], choices=enum_choices(ControlMode)),
                signal("Input_Mode", 32, 32, receivers=[axis_node.name], choices=enum_choices(InputMode)),
            ],
            senders=['Master'],
        ),
        can.Message(
            0x00C,
            "Set_Input_Pos",
            8,
            [
                signal("Input_Pos", 0, 32, is_float=True, receivers=[axis_node.name], unit='rev'),
                signal("Vel_FF", 32, 16, is_signed=True, scale=0.001, receivers=[axis_node.name], unit='rev/s'),
                signal("Torque_FF", 48, 16, is_signed=True, scale=0.001, receivers=[axis_node.name], unit='Nm'),
            ],
            senders=['Master'],
        ),
        can.Message(
            0x00D,
            "Set_Input_Vel",
            8,
            [
                signal("Input_Vel", 0, 32, is_float=True, receivers=[axis_node.name], unit='rev'),
                signal("Input_Torque_FF", 32, 32, is_float=True, receivers=[axis_node.name], unit='rev/s'),
            ],
            senders=['Master'],
        ),
        can.Message(
            0x00E,
            "Set_Input_Torque",
            8,
            [signal("Input_Torque", 0, 32, is_float=True, receivers=[axis_node.name], unit='Nm')],
            senders=['Master'],
        ),
        can.Message(
            0x00F,
            "Set_Limits",
            8,
            [
                signal("Velocity_Limit", 0, 32, is_float=True, receivers=[axis_node.name], unit='rev/s'),
                signal("Current_Limit", 32, 32, is_float=True, receivers=[axis_node.name], unit='A'),
            ],
            senders=['Master'],
        ),
        can.Message(0x010, "Start_Anticogging", 0, [], senders=['Master']),
        can.Message(
            0x011,
            "Set_Traj_Vel_Limit",
            8,
            [signal("Traj_Vel_Limit", 0, 32, is_float=True, receivers=[axis_node.name], unit='rev/s')],
            senders=['Master'],
        ),
        can.Message(
            0x012,
            "Set_Traj_Accel_Limits",
            8,
            [
                signal("Traj_Accel_Limit", 0, 32, is_float=True, receivers=[axis_node.name], unit='rev/s^2'),
                signal("Traj_Decel_Limit", 32, 32, is_float=True, receivers=[axis_node.name], unit='rev/s^2'),
            ],
            senders=['Master'],
        ),
        can.Message(
            0x013,
            "Set_Traj_Inertia",
            8,
            [signal("Traj_Inertia", 0, 32, is_float=True, receivers=[axis_node.name], unit='Nm / (rev/s^2)')],
            senders=['Master'],
        ),
        can.Message(
            0x014,
            "Get_Iq",
            8,
            [
                signal("Iq_Setpoint", 0, 32, is_float=True, receivers=['Master'], unit='A'),
                signal("Iq_Measured", 32, 32, is_float=True, receivers=['Master'], unit='A'),
            ],
            senders=[axis_node.name],
        ),
        can.Message(
            0x015,
            "Get_Sensorless_Estimates",
            8,
            [
                signal("Sensorless_Pos_Estimate", 0, 32, is_float=True, receivers=['Master'], unit='rev'),
                signal("Sensorless_Vel_Estimate", 32, 32, is_float=True, receivers=['Master'], unit='rev/s'),
            ],
            senders=[axis_node.name],
        ),
        can.Message(0x016, "Reboot", 0, [], senders=['Master']),
        can.Message(
            0x017,
            "Get_Bus_Voltage_Current",
            8,
            [
                signal("Bus_Voltage", 0, 32, is_float=True, receivers=['Master'], unit='V'),
                signal("Bus_Current", 32, 32, is_float=True, receivers=['Master'], unit='A'),
            ],
            senders=[axis_node.name],
        ),
        can.Message(0x018, "Clear_Errors", 0, [], senders=['Master']),
        can.Message(
            0x019,
            "Set_Linear_Count",
            8,
            [signal("Position", 0, 32, is_signed=True, receivers=[axis_node.name], unit='counts')],
            senders=['Master'],
        ),
        can.Message(
            0x01A,
            "Set_Pos_Gain",
            8,
            [signal("Pos_Gain", 0, 32, is_float=True, receivers=[axis_node.name], unit='(rev/s) / rev')],
            senders=['Master'],
        ),
        can.Message(
            0x01B,
            "Set_Vel_Gains",
            8,
            [
                signal("Vel_Gain", 0, 32, is_float=True, receivers=[axis_node.name], unit='Nm / (rev/s)'),
                signal("Vel_Integrator_Gain", 32, 32, is_float=True, receivers=[axis_node.name], unit='(Nm / (rev/s)) / s'),
            ],
            senders=['Master'],
        ),
        can.Message(
            0x01C,
            "Get_ADC_Voltage",
            8,
            [signal("ADC_Voltage", 0, 32, is_float=True, receivers=['Master'], unit='V')],
            senders=[axis_node.name],
        ),
        can.Message(
            0x01D,
            "Get_Controller_Error",
            8,
            [signal("Controller_Error", 0, 32, receivers=['Master'], choices=enum_choices(ControllerError))],
            senders=[axis_node.name],
        ),
    ]

    for msg in axis_messages:
        msg.name = f"Axis{axis_id}_{msg.name}"
        msg.frame_id |= axis_id << 5

    messages.append(axis_messages)


messages = list(chain.from_iterable(messages))
db = can.Database(messages=messages, nodes=nodes, buses=buses, version='0.5.6')
dump_file(db, "odrive-cansimple.dbc")

# Keep output stable across environments and avoid CRLF-only diffs.
with open("odrive-cansimple.dbc", "r", encoding="utf-8", newline="") as f:
    content = f.read().replace("\r\n", "\n")
with open("odrive-cansimple.dbc", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
