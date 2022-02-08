"""!@file                ClosedLoop.py
        A closed loop controller is used to reach desired motor location. The motor
        takes the location of the motor, a specified setpoint of the motor, and uses
        that information with a proportional gain to calculate a new duty cycle for
        the motor such that the motor's location reaches the setpoint.
   @author              Aleya Dolorfino
   @author              Chloe Chou
   @author              Christian Roberts
   @date                February 8, 2022
"""
import utime, shares
class ClosedLoop:
    '''!
    @brief Close-loop controller class
    @details Close loop controller class to controll the speed of the motor 
    '''

    
    def __init__(self,location,setpoint,kp, enc_pos_1):
        '''!
        @brief Object contructor for Closed Loop class
        @param delta This parameter is the measured motor velocity in rad/sec 
               omega_ref This parameter is the desired velocity in rad/sec inputed by the user
               kp This parameter is the proportional gain for the closeloop controller

        '''
        self.setpoint = setpoint
        self.location = location
        self.kp = kp
        self.error = self.setpoint - self.location
        
        self.printout = []
        self.times = []
        self.enc_pos_1 = enc_pos_1
        
    def run(self):
        '''!
        @brief Runs controller function 
        @details The function runs the closedloop feedback system. New calculated duty is below -100 or above 100
                 then the duty is set to the maximum duty of either -100 or 100. 
        @return duty This function returns the new calculated duty cycle for the DC motor 
        '''

        
        self.set_location(self.enc_pos_1.read())
        self.error = self.setpoint - self.location
        
        if abs(self.error) >=5:
            

            
            self.duty = self.kp*(self.error)
#             self.times.append(difference)

#             utime.sleep_ms(10)
        
                
#         try:
#             for x in range (100):
#                 print (self.times[x],self.printout[x])
#         except IndexError:
#             pass
        
        if self.duty >100:
            self.duty = 100
        if self.duty <-100:
            self.duty = -100
        return self.duty
        
    def get_Kp(self,kp):
        """!
        Returns the Kp value assigned to the closed loop
        """
        return self.kp
     
    def set_Kp(self, kp):
        """!
        Changes the input Kp value
        """
        self.kp = kp
        
    def get_setpoint(self):
        """!
        Returns the setpoint value assigned to the closed loop
        """
        return self.setpoint
        
    def set_setpoint(self, setpoint):
        """!
        Changes the setpoint for the closed loop to calculate
        """
        self.setpoint = setpoint
        
    def set_location(self, location):
        """!
        Changes the location for the closed loop to calculate
        """
        self.location = location
        
    def get_error(self):
        """!
        Returns the error calculated in the closed loop
        """
        return self.error