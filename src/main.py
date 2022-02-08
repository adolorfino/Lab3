"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@author Chloe Chou
@author Aleya Dolorfino
@author Christian Roberts

@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import task_encoder,motor_driver, closedloop, shares, utime
from pyb import USB_VCP
vcp = USB_VCP()


def task1_fun ():
    """!
    Task which puts things into a share and a queue.
    """
    
    #Shares for Motor 1: position, delta, zero, and duty
    enc_pos_1 =  shares.Share(0)
    delta_pos_1 = shares.Share(0)
    enc_zero_1 = shares.Share(False)
    enc_duty_1=  shares.Share(0)
    
    ## @brief   A variable enable that is true whenever there is not a fault.
    ## @details This variable is written in task_user.py and is set to True
    ##          if the 'c' key is pressed to reset the fault condition.
    enable = shares.Share()
    
    ## @brief   A variable fault_found that triggers during a fault.
    ## @details This variable is written in DRV8847.py and is set to True
    ##          if a fault is detected.
    fault_found = shares.Share(False)
    
    printout = []
    times = []
    
    
    
    e_pin_1 = pyb.Pin.cpu.B6
    e_pin_2 = pyb.Pin.cpu.B7
    e_channel = 4
    
    m_pin_1 = pyb.Pin.board.PB4
    m_pin_2 = pyb.Pin.board.PB5
    m_enable = pyb.Pin.board.PA10
    m_timer = pyb.Timer(3, freq = 20000)
    
    task1 = task_encoder.Task_Encoder(65535, e_channel,enc_pos_1, delta_pos_1,enc_zero_1, e_pin_1, e_pin_2)
    task2 = motor_driver.MotorDriver(m_enable, m_pin_1, m_pin_2, m_timer)
    task3 = closedloop.ClosedLoop(0, 8192, 1,enc_pos_1)
    
    while True:
        try:
            
            reference_time = utime.ticks_ms()
            current_time = utime.ticks_ms()
            difference = utime.ticks_diff(current_time, reference_time)
            #while difference <= 1000:
            task1.run()
            current_time = utime.ticks_ms()
            difference = utime.ticks_diff(current_time, reference_time)
            #enc_zero_1.write(True)


            task3.set_Kp(.1)
            task3.set_location(enc_pos_1.read())
            duty = task3.run()
            task2.set_pwm(duty)
            printout.append(enc_pos_1.read())
            times.append(difference)
            #task2.set_pwm(0)
        except MemoryError:
            return[printout,times]
        except KeyboardInterrupt:
            return [printout, times]

        yield (0)


def task2_fun ():
    """!
    Task which takes things out of a queue and share to display.
    """
     
    #Shares for Motor 1: position, delta, zero, and duty
    enc_pos_1 =  shares.Share(0)
    delta_pos_1 = shares.Share(0)
    enc_zero_1 = shares.Share(False)
    enc_duty_1=  shares.Share(0)
    
    ## @brief   A variable enable that is true whenever there is not a fault.
    ## @details This variable is written in task_user.py and is set to True
    ##          if the 'c' key is pressed to reset the fault condition.
    enable = shares.Share()
    
    ## @brief   A variable fault_found that triggers during a fault.
    ## @details This variable is written in DRV8847.py and is set to True
    ##          if a fault is detected.
    fault_found = shares.Share(False)
    
    printout = []
    times = []
    
    
    
    e_pin_1 = pyb.Pin.cpu.C6
    e_pin_2 = pyb.Pin.cpu.C7
    e_channel = 8
    
    m_pin_1 = pyb.Pin.board.PA0
    m_pin_2 = pyb.Pin.board.PA1
    m_enable = pyb.Pin.board.PC1
    m_timer = pyb.Timer(5, freq = 20000)
    
    task1 = task_encoder.Task_Encoder(65535, e_channel,enc_pos_1, delta_pos_1,enc_zero_1, e_pin_1, e_pin_2)
    task2 = motor_driver.MotorDriver(m_enable, m_pin_1, m_pin_2, m_timer)
    task3 = closedloop.ClosedLoop(0, 8192, 1,enc_pos_1)
    
    while True:
        try:
            
            reference_time = utime.ticks_ms()
            current_time = utime.ticks_ms()
            difference = utime.ticks_diff(current_time, reference_time)
            task1.run()
            current_time = utime.ticks_ms()
            difference = utime.ticks_diff(current_time, reference_time)
            #enc_zero_1.write(True)


            task3.set_Kp(.1)
            task3.set_location(enc_pos_1.read())
            duty = task3.run()
            task2.set_pwm(duty)
            printout.append(enc_pos_1.read())
            times.append(difference)
            #task2.set_pwm(0)
        except MemoryError:
            return[printout,times]
        except KeyboardInterrupt:
            return [printout, times]

        yield (0)





# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
    q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                           name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
                         period = 15000, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
                         period = 15, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')

