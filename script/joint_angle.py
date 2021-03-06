#!/usr/bin/env python
import rospy
import math
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float64
from math import degrees
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

class joint_information():

	def __init__(self):
		rospy.init_node('robot_joint',anonymous=True)
		self.joint_state = JointState()       
		self.pub = rospy.Publisher('joint_angle',String, queue_size=10)
		rospy.Subscriber('/move_group/fake_controller_joint_states',JointState,self.joint_callback,queue_size=10)        
		rospy.spin()
		
		rate = rospy.Rate(10)
        		
    	def joint_callback(self,msg):
    		#print self.pub
		jointangle=msg.position
		a=np.degrees(jointangle)
		"""        
		decide right or left
		jointname=msg.name[4]
		rospy.loginfo(jointname[0:5])	
		"""
		#decide data format
		c=''
		d='/211'
		newrad = [round(float('%.2f' % i),1) for i in a]
		for j in range(0,6,1):
			if newrad[j]==0 :				
				c='0000'
				#print b
		 
			if 0 < newrad[j] < 100.0 or 0 > newrad[j] > -100.0:				
				if newrad[j] > 0:
					if newrad[j] < 10:						
						b=int(newrad[j]*10)
						c='00'+str(b)
						#print b
					else :						
						b=int(newrad[j]*10)
						c='0'+str(b)
						#print b
				else :	
					if newrad[j] > -10:				
						b=int(newrad[j]*-10)						
						c='-00'+str(b)
    						#print b
    					else :    						
    						b=int(newrad[j]*-10)
						c='-0'+str(b)
    						#print b
    			if newrad[j] > 100.0 :    				
    				b=int(newrad[j]*10)
    				c=''+str(b)
    				#print b
    			d+=c+(''if j != 5 else '\\')
    			      		      
		(self.pub).publish(d)
		rate = rospy.Rate(10)
		rate.sleep()
        		
              		
    
if __name__ == '__main__':
	try:
          	joint_information()
          	                 
     	except rospy.ROSInterruptException:
         		rospy.loginfo('fail to subscribe and pub')
         		pass
         
