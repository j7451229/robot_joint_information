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
		self.arm=[0]*12
		self.finger =[0]*8
		self.joint_state = JointState()		    
		self.pub = rospy.Publisher('joint_angle',String, queue_size=10)
		rospy.Subscriber('/joint_states',JointState,self.joint_callback,queue_size=10)       
		rospy.spin()
		rate = rospy.Rate(10)
        	
	def check(self,l_arm,r_arm):
		arm_full=l_arm+r_arm
		
		if all([i == 0 for i in arm_full]):
			print 'start posittion'
					
		elif all([arm_full[i]== self.arm[i] for i in range(len(arm_full))]):
			print 'same' 
		else:
			self.arm = arm_full 
			print'do something'			
			self.decide_data_format(arm_full)
			
				
		#return arm_full
		
    	def joint_callback(self,msg):

		jointangle=msg.position
		jointname=msg.name			
		a=np.degrees(jointangle)
		newrad = [round(float('%.2f' % i),1) for i in a]
		'''		        		
		for i in range(len(newrad)): 
			x=float("%.2f" % newrad[i])
			if x == 0.00 :
				newrad[i]=0.00
		'''
		#rospy.loginfo(jointangle[3:8])	#arm
		#rospy.loginfo(jointangle[17:22]) #r_arm
		l_arm=newrad[3:9]
		r_arm=newrad[17:23]
		self.check(l_arm,r_arm)
		#print self.arm_full

		
			
		
		
	def decide_data_format(self,arm_full) : #arm_full=[x,x,x,x,x,x,x,x,x,x,x,x,x]
		
		
		c=''
		e=''
		#arm_full = self.arm_full
		
		
		
		for i in range(len(arm_full)):
			if i < 6 :
				d='/211'
				a=arm_full[0:6]
				#print len(a)
			elif 6 <= i < 13 :
				d='/111'
				a=arm_full[6:12]
				#print a
			else :
				pass 
			
			for j in range(len(a)) :
				if a[j]==0 :				
					c='0000'
					#print b
		 
				if 0 < a[j] < 100.0 or 0 > a[j] > -100.0:				
					if a[j] > 0:
						if a[j] < 10:						
							b=int(a[j]*10)
							c='00'+str(b)
							#print b
						else :						
							b=int(a[j]*10)
							c='0'+str(b)
							#print b
					else :	
						if a[j] > -10:				
							b=int(a[j]*-10)						
							c='-00'+str(b)
	    						#print b
	    					else :    						
	    						b=int(a[j]*-10)
							c='-0'+str(b)
	    						#print b
	    			if a[j] > 100.0 :    				
	    				b=int(a[j]*10)
	    				c=''+str(b)
	    				#print b
	    			
				
				d+=c+(''if j != 5 else '\\')
			
			if i==5 or i==11 :
				e+=d
		print e	      		      
		(self.pub).publish(e)
		rate = rospy.Rate(10)
		rate.sleep()
        	
              		
    
if __name__ == '__main__':
	try:
          	joint_information()
          	                 
     	except rospy.ROSInterruptException:
         		rospy.loginfo('fail to subscribe and pub')
         		pass
         
