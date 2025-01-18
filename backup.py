import math
import magicbot
import wpilib
import wpilib.event

from magicbot import tunable
from wpimath.geometry import Rotation3d, Translation3d
from phoenix6.configs import (
    ClosedLoopGeneralConfigs,
    FeedbackConfigs,
    MotorOutputConfigs,
    Slot0Configs,
)
from phoenix6.controls import PositionDutyCycle, VelocityVoltage, VoltageOut
from phoenix6.hardware import CANcoder, TalonFX
from phoenix6.signals import InvertedValue, NeutralModeValue

steer_id = 22  # CANId of a turning motor
encoder_id = 32  # CANId of a turning encoder

pn = wpilib.SmartDashboard.putNumber


class MyRobot(magicbot.MagicRobot):
    _automodes = []
    STEER_GEAR_RATIO = 1 / ((10 / 20) * (14 / 72))  # 10.23

    def createObjects(self) -> None:
        # Create some objects for loggind/displaying data
        self.data_log = wpilib.DataLogManager.getLog()
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData(self.field)

        # Now create some robot specific items
        self.gamepad = wpilib.XboxController(0)
        self.steer = TalonFX(steer_id, 'canivore')
        self.encoder = CANcoder(encoder_id, 'canivore')

        # Reduce CAN status frame rates before configuring
        self.steer.get_fault_field().set_update_frequency(
            frequency_hz=4, timeout_seconds=0.01
        )

        # Configure steer motor
        steer_config = self.steer.configurator

        steer_motor_config = MotorOutputConfigs()
        steer_motor_config.neutral_mode = NeutralModeValue.BRAKE
        steer_motor_config.inverted = InvertedValue.CLOCKWISE_POSITIVE

        steer_gear_ratio_config = FeedbackConfigs().with_sensor_to_mechanism_ratio(
            self.STEER_GEAR_RATIO
        )

        # configuration for motor pid
        steer_pid = Slot0Configs().with_k_p(2.5).with_k_i(0).with_k_d(0.0)
        steer_closed_loop_config = ClosedLoopGeneralConfigs()
        steer_closed_loop_config.continuous_wrap = True

        steer_config.apply(steer_motor_config)
        steer_config.apply(steer_pid, 0.01)
        steer_config.apply(steer_gear_ratio_config)
        steer_config.apply(steer_closed_loop_config)

    def teleopInit(self) -> None:
        self.field.getObject("Intended start pos").setPoses([])
        pos = self.encoder.get_absolute_position().value
        self.steer.set_position(pos)
        self.target_angle = 0

    def disabledPeriodic(self) -> None:
        print('disabled')
        self.display_sd()

    def display_sd(self) -> None:
        pn("target_angle", self.target_angle)
        pn("steer", self.steer.get_position().value)
        pn("encoder", self.encoder.get_absolute_position().value)

    def teleopPeriodic(self) -> None:
        dpad = self.gamepad.getPOV()
        if dpad != -1:
            self.target_angle = dpad

        self.display_sd()

        tgt = math.radians(self.target_angle) / math.tau
        pn("tgt", tgt)
        req = PositionDutyCycle(tgt)
        self.steer.set_control(req)
        pass

    def testInit(self) -> None:
        pass

    def testPeriodic(self) -> None:
        pass
