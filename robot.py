import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.solenoidbase import SolenoidBase
from wpilib.interfaces import GenericHID
import wpilib.timer 

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        #drive
        self.frontLeft = wpilib.Talon(0)
        self.frontRight = wpilib.Talon(1)
        self.backLeft = wpilib.Talon(2)
        self.backRight = wpilib.Talon(3)

        self.left = wpilib.SpeedControllerGroup(self.frontLeft,self.backLeft)
        self.right = wpilib.SpeedControllerGroup(self.frontRight,self.backRight)

        self.drive = DifferentialDrive(self.left,self.right)
        self.drive.setExpiration(0.1)

        # Pnematics 
        self.Compressor = wpilib.Compressor(0)
        self.Compressor.setClosedLoopControl(True)

        self.Ps = self.Compressor.getPressureSwitchValue()

        
        self.tank2 = wpilib.DoubleSolenoid(0,0,1)
        self.tank1 = wpilib.DoubleSolenoid(0,2,3)
        self.Compressor.start()
        

        # xbox cont
        self.xbox1 = wpilib.XboxController(1)
        self.yL = self.xbox1.getRawAxis(1)
        self.xL = self.xbox1.getRawAxis(0)
        self.yR = self.xbox1.getRawAxis(5)
        self.xR = self.xbox1.getRawAxis(4)
        self.leftTrig = self.xbox1.getRawAxis(2)
        self.rightTrig = self.xbox1.getRawAxis(3)
        self.buttonB = self.xbox1.getBButtonPressed()
        self.buttonA = self.xbox1.getAButtonPressed()
        self.timer = wpilib.Timer()
        self.loops = 0

        #vision
        wpilib.CameraServer.launch()
    def autonomousInit(self):
        pass
    def autonomousPeriodic(self):
        pass
    def disabledInit(self):
        self.logger.info("%d loops / %f seconds", self.loops, self.timer.get())
    def disabledPeriodic(self):
        pass
    def teleopInit(self):
        self.loops = 0
        self.timer.reset()
        self.timer.start()
    def teleopPeriodic(self):
        
        self.loops += 1
        if self.timer.hasPeriodPassed(1):
            self.logger.info("%d loops / second", self.loops)
            self.loops = 0
        #drive tele
        self.speed= self.yL-((self.yL*self.rightTrig)+.01)
        self.zaxisArcade= self.xR-((self.xR*self.rightTrig)+.01)
        self.drive.arcadeDrive(self.speed,self.zaxisArcade)

        #pnematics tele
        if self.buttonA==True:
            self.tank1.set(1)
            self.tank2.set(2)
        if self.buttonB==True:
            self.tank1.set(2)
            self.tank2.set(1)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
        








