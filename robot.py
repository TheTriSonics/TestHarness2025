#!/usr/bin/env python3

import wpilib
import magicbot
from phoenix6.hardware import TalonFX
from phoenix6.configs import Slot0Configs, FeedbackConfigs
from phoenix6.controls import DutyCycleOut
from wpimath.controller import PIDController

pn = wpilib.SmartDashboard.putNumber
gn = wpilib.SmartDashboard.getNumber


class MyRobot(magicbot.MagicRobot):
    # Basic robot program showing different functions in TimedRobot
    # Each function prints when it runs to understand the robot's lifecycle

    def createObjects(self):
        # Called when robot starts up to create objects (like motor controllers)
        print("Robot is starting up!")
        
        self.motor = TalonFX(11, 'canivore')
        
        # Configure the sensor to mechanism ratio for rotations
        configs = FeedbackConfigs().with_sensor_to_mechanism_ratio(1.0)
        self.motor.configurator.apply(configs)

        p, i, d = 0.002, 0, 0
        pn('P', p)
        pn('Target RPM', 20)
        
        # Create PID controller for velocity control (2 RPS = 120 RPM target)
        self.pid_controller = PIDController(p, i, d)
        
        print("Robot objects created!")

    def robotPeriodic(self) -> None:
        # Called every robot packet (~20ms) regardless of mode
        print("Robot periodic running!")

    def disabledInit(self) -> None:
        # Called once when the robot enters disabled mode
        print("Robot is now disabled!")

    def disabledPeriodic(self) -> None:
        # Called periodically when the robot is disabled
        print("Disabled periodic running!")

    def autonomousInit(self) -> None:
        # Called once when autonomous mode starts
        print("Autonomous mode is starting!")

    def autonomousPeriodic(self) -> None:
        # Called periodically during autonomous mode
        print("Autonomous periodic running!")

    def teleopInit(self) -> None:
        # Called once when teleop mode starts
        print("Teleop mode is starting!")

    def teleopPeriodic(self) -> None:
        # Called periodically during teleop mode
        current_velocity = self.motor.get_velocity().value
        
        # Calculate PID output for 2 RPS target
        p = gn('P', 0.002) 
        target = gn('Target RPM', 20)
        self.pid_controller.setP(p)
        output = self.pid_controller.calculate(current_velocity, target)
        pn('PID Output', output) 
        pn('Velocity', current_velocity)
        duty = DutyCycleOut(output)
        self.motor.set_control(duty)
        
        print("Teleop periodic running!")

    def testInit(self) -> None:
        # Called once when test mode starts
        print("Test mode is starting!")

    def testPeriodic(self) -> None:
        # Called periodically during test mode
        print("Test periodic running!")


if __name__ == "__main__":
    # Main entry point of our program
    wpilib.run(MyRobot)
