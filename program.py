#!/usr/bin/python

import rospy
import math
from ardrone_autonomy.msg import Navdata
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers
from visualization_msgs.msg import Marker
from math import copysign
from std_msgs.msg import String
from geometry_msgs.msg import Twist  	 # for sending commands to the drone
from std_msgs.msg import Empty       	 # for land/takeoff/emergency

global ax
global ay
global az
global x1
global x2
global x3
global x4
global x5
          
def callback(data):
	global x1
	global x2
	global x3
	global x4
	global x5
	x1 = data.pose.position.x
	x2 = data.pose.position.y
	x3 = data.pose.position.z
	x4 = data.pose.orientation.x
	x5 = data.pose.orientation.y
def fax(mssg):
	global ax
	global ay
	global az
	ax = mssg.ax
	ay = mssg.ay
	az = mssg.az

def glowna():
	global x1
	global x2
	global x3
	global x4
	global x5
	global ax
	global ay
	global az
	global tagx
	global tagy
	global tagz
	global oldz
	oldz=0
	ax = 0
	ay = 0
	az = 0
	x1 = 0
	x2 = 0
	x3 = 0
	x4 = 0
	x5 = 0
	
	px1_error4=0
	px1_error3=0
	px1_error2=0
	px1_error1=0
	
	px2_error4=0
	px2_error3=0
	px2_error2=0
	px2_error1=0
	
	xerror=0
	yerror=0
	prevx1=0
	prevx2=0
	rospy.init_node('info')
	Sax = rospy.Subscriber('/ardrone/navdata', Navdata, fax)
	tagDet = rospy.Subscriber('/visualization_marker', Marker, callback)
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=30)
	vel_msg = Twist()
	#Pfi = rospy.Publisher("~fi", Float32, queue_size=30)
	Tagx = rospy.Publisher("~tagxpos", Float32, queue_size=30)
	Pteta = rospy.Publisher("~teta", Float32, queue_size=30)
	czekajka = rospy.Rate(12)
	#fi = Float32()
	#teta = Float32()
	tagxpos = Float32()
	licz=0
	prev1x1=0
	prev2x1=0
	prev3x1=0
	prev1x2=0
	prev2x2=0
	prev3x2=0
	while not rospy.is_shutdown():
		dt=1.0/12
		
		yperror=yerror+dt*x1
		xperror=xerror+dt*x2	
		yderror=(-25.0/12)+4*px1_error1-3*px1_error2+(4.0/3)*px1_error3-(1.0/4)*px1_error4	#x1	
		xderror=(-25.0/12)+4*px2_error1-3*px2_error2+(4.0/3)*px2_error3-(1.0/4)*px2_error4	#x2
		pidy=-(0.05*x1+0.0*yperror+0.007*yderror)
		pidx=-(0.2*x2+0.0*xperror+0.015*xderror)
		
		
		px1_error4=px1_error2-0.0
		px1_error3=px1_error2
		px1_error2=px1_error1
		px1_error1=x1
		
		px2_error4=px2_error3
		px2_error3=px2_error2
		px2_error2=px2_error1
		px2_error1=x2
		#rate = rospy.Rate(1/dt)
		vel_msg = Twist()
		vel_msg.angular.x=0.1
		vel_msg.angular.y=0.1
		#vel_msg.angular.z=0			
		
		if x3>1.5:
			if x1>0.001*x3:
				vel_msg.linear.y = pidy
				print 'zmieniam y',pidy
			elif x1<-0.001*x3:
				vel_msg.linear.y = pidy
				print 'zmieniam y',pidy
			else:
				vel_msg.linear.y =0.0
			
			if x2>0.001*x3:
				vel_msg.linear.z = pidx
				print 'zmieniam x',pidx
			elif x2<-0.001*x3:
				vel_msg.linear.z = pidx
				print 'zmieniam x',pidx
			else:
				#vel_msg.linear.z =0.0
				print 'zmieniam x'
			if x1<0.2*x3 and x1>-0.2*x3 and x2>-0.2*x3 and x2<0.2*x3:#and oldz!=x3
				#vel_msg.linear.z = -0.3
				print 'do dolu etap 1'
			else:
				#vel_msg.linear.z = 0.0
				print 'stop etap 1'
		elif x3<=1.5 and x3>0.7:
			if x1>0.001*x3:
				vel_msg.linear.y = pidy
				print 'zmieniam y',pidy
			elif x1<-0.001*x3:
				vel_msg.linear.y = pidy
				print 'zmieniam y',pidy
			else:
				vel_msg.linear.y =0.0
			
			if x2>0.001*x3:
				vel_msg.linear.z = pidx
				print 'zmieniam x',pidx
			elif x2<-0.001*x3:
				vel_msg.linear.z = pidx
				print 'zmieniam x',pidx
			else:
				#vel_msg.linear.x =0.0
				print 'zmieniam x'
			if x1<0.1*x3 and x1>-0.1*x3 and x2>-0.1*x3 and x2<0.1*x3 :
				#vel_msg.linear.z = -0.2
				print 'do dolu etap dwa'
			else:
					#vel_msg.linear.z = 0.0
					print 'stop etap 2'
		elif x3<=0.7 and x3>0.2:
			print 'trzeci etjjjjjjjjjjjjjap'
			#vel_msg.linear.z = -0.2
			if x1>0.001*x3:
				vel_msg.linear.y = pidy
				print 'zmieniam y',pidy
			elif x1<-0.001*x3:
				vel_msg.linear.y = pidy
				print 'zmieniam y',pidy
			else:
				vel_msg.linear.y =0.0
			
			if x2>0.001*x3:
				vel_msg.linear.z = pidx
				print 'zmieniam x',pidx
			elif x2<-0.001*x3:
				vel_msg.linear.z = pidx
				print 'zmieniam x',pidx
			else:
				#vel_msg.linear.z =0.0
				print 'zmieniam x'
			empty = Empty()
			print 'trzeci etap'
			land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
			#land.publish(empty)
			print 'koniec'
		else:
			vel_msg.linear.y = 0
			vel_msg.linear.x = 0
			vel_msg.linear.z = 0.0
			print 'nie ma platformy'
		prev3x1=prev2x1
		#print 'prev3x1',prev3x1
		prev2x1=prev1x1
		#print 'prev2x1',prev2x1
		prev1x1=x1
		#print 'prev1x1',prev1x1
		prev3x2=prev2x2
		prev2x2=prev1x2
		prev1x2=x2
		
		
		#if x1==(prev1x1) and x1==(prev2x1) and x1==(prev3x1) and x2==(prev1x2) and x2==(prev2x2) and x2==(prev3x2):
		#	vel_msg.linear.y = 0
		#	vel_msg.linear.x = 0
		#	vel_msg.linear.z = 0.0
		#	print 'ifffffffffffffffffffffffffffffffffff'

		#vel_msg.linear.y = 3*x2
		tagxpos.data=10*x1
		Tagx.publish(tagxpos)	
		print 'cmd x ',vel_msg.linear.x 
		print 'cmd y ',vel_msg.linear.y 
		print 'cmd z ',vel_msg.linear.z 

		
		velocity_publisher.publish(vel_msg)
		
		
		czekajka.sleep()

if __name__=='__main__':
	try:
		glowna()
	except rospy.ROSInterruptException:
		pass
