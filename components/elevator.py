import magicbot

from phoenix6.hardware import TalonFX
from phoenix6.controls import PositionDutyCycle
from phoenix6.configs import (
    Slot0Configs,
    FeedbackConfigs,
    TalonFXConfiguration,
    MotionMagicConfigs,
)

POS_HOME = 0
POS_LVL1 = 11.01
POS_LVL2 = 19.07
POS_LVL3 = 30.22


class Elevator:
    elevator_motor: TalonFX = TalonFX(41)
    target: float = POS_HOME

    def createObjects(self) -> None:
        # TODO: Add limit switches to the TalonFX?

        # Configure the sensor to mechanism ratio for rotations
        encoder_cfg = FeedbackConfigs().with_sensor_to_mechanism_ratio(1.0)
        
        # https://v6.docs.ctr-electronics.com/en/stable/docs/api-reference/device-specific/talonfx/motion-magic.html
        motor_configs = TalonFXConfiguration()
        slot0_configs = motor_configs.slot0
        slot0_configs.k_s = 0.25  # static friction 
        slot0_configs.k_v = 0.12  # target vel of 1 rps results in 0.12V
        slot0_configs.k_a = 0.01  # accel of 1 rps/s requires 0.01V
        slot0_configs.k_p = 4.8 
        slot0_configs.k_i = 0
        slot0_configs.k_d = 0.1

        # set Motion Magic settings
        motion_magic_configs = motor_configs.motion_magic
        # Target cruise velocity (rps) 
        motion_magic_configs.motion_magic_cruise_velocity = 12 
        # Target acceleration in rps/s
        motion_magic_configs.motion_magic_acceleration = 48
        # Target jerk of in rps/s/s
        motion_magic_configs.motion_magic_jerk = 1600 

        self.elevator_motor.configurator.apply(motor_configs)
        self.elevator_motor.configurator.apply(encoder_cfg)
        self.elevator_motor.set_position(POS_HOME)
        self.target = POS_HOME 

    def go_home(self) -> None:
        self.target = POS_HOME
    
    def go_level_1(self) -> None:
        self.target = POS_LVL1

    def go_level_2(self) -> None:
        self.target = POS_LVL2

    def go_level_3(self) -> None:
        self.target = POS_LVL3

    def get_position(self) -> float:
        return self.elevator_motor.get_position().value

    def at_target(self, target=None) -> bool:
        if target is None:
            target = self.target
        diff = abs(self.target - self.get_position())
        return (diff < 0.02)

    def execute(self) -> None:
        print(f'Elvevator target {self.target}')
        if self.at_target():
            return  # Nothing to do. We're at the correct location
        
        # We're not there yet, so power the motor to get to the right setpoint
        self.elevator_motor.set_control(
            PositionDutyCycle(self.target)
        )
