#!/usr/bin/env python3

import wpilib
import magicbot
from phoenix6.hardware import TalonFX
from phoenix6.configs import Slot0Configs, FeedbackConfigs
from phoenix6.controls import DutyCycleOut
from wpimath.controller import PIDController

from components.elevator import Elevator 
from components.leds import LEDs

pn = wpilib.SmartDashboard.putNumber
gn = wpilib.SmartDashboard.getNumber


class MyRobot(magicbot.MagicRobot):
    # Basic robot program showing different functions in TimedRobot
    # Each function prints when it runs to understand the robot's lifecycle

    elevator: Elevator
    leds: LEDs

    def createObjects(self):
        print("Robot objects created!")

    def robotPeriodic(self) -> None:
        # Called every robot packet (~20ms) regardless of mode
        # print("Robot periodic running!")
        return

    def disabledInit(self) -> None:
        # Called once when the robot enters disabled mode
        print("Robot is now disabled!")

    def disabledPeriodic(self) -> None:
        # Called periodically when the robot is disabled
        # print("Disabled periodic running!")
        if (wpilib.DriverStation.isDSAttached()):
            self.leds.set_colorRGB((0, 255, 0))
        else:
            self.leds.set_colorRGB((255, 0, 0))
        self.leds.execute()
        return

    def autonomousInit(self) -> None:
        # Called once when autonomous mode starts
        self.leds.set_colorRGB((255, 0, 255))
        print("Autonomous mode is starting!")

    def autonomousPeriodic(self) -> None:
        # Called periodically during autonomous mode
        print("Autonomous periodic running!")

    def teleopInit(self) -> None:
        # Called once when teleop mode starts
        self.leds.rainbow()
        print("Teleop mode is starting!")

    def teleopPeriodic(self) -> None:
        print("Teleop periodic running!")

    def testInit(self) -> None:
        # Called once when test mode starts
        print("Test mode is starting!")

    def testPeriodic(self) -> None:
        # Called periodically during test mode
        # print("Test periodic running!")
        return


if __name__ == "__main__":
    # Main entry point of our program
    wpilib.run(MyRobot)
