# Lab3

This experiment was used to show that we could perform multiple tasks at the
same time but at differring periods. To do this our group essentially made
two similar tasks to Lab 2 but with the correct pins for the two different 
motor. We then used **cotask.py** to run the two tasks simultaniously but at two
differring periods. 

Below is an image of two step responses. One is running at a period of 15 ms and 
the other is running at 80ms. As you can clearly see in the graph below the the 
task going in a 15ms period has a much faster settling time compared to the task 
with the 80ms period. This makes since because the faster the contoller is able to
run the quicker it can correct the positioning of the motor.

![Step Response Graph](/../main/images/graph.png)

It should be noted that both our step responses are considered slow enough to create
a functioning controller but when we tried to run the task at a period of 150ms the 
system became unstable and would continuously overcorrect in either direction and 
never really find its settling point.
