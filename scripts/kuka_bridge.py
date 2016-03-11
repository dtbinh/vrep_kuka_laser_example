#!/usr/bin/python
import rospy
from sensor_msgs.msg import JointState
from vrep_common.msg import JointSetStateData
from vrep_common.srv import simRosGetObjectHandle, simRosSetJointState
from math import sin, cos, pi
class kuka_vrep_bridge:
   
    def __init__(self):
        joint_names=[]
        for i in range(1,8):
            joint_names.append('LBR4p_joint' + `i`)
        
        self.j=JointSetStateData()
        self.j.values.data=[0,0,0,0,0,0,0]
        
        self.j.setModes.data=[1,1,1,1,1,1,1]

      #  self.modes= [1,1,1,1,1,1,1];
       # self.jhandles=[]
        rospy.wait_for_service('vrep/simRosGetObjectHandle')
        #rospy.wait_for_service('vrep/simRosSetJointState')
        try:
            getHandle = rospy.ServiceProxy('vrep/simRosGetObjectHandle', simRosGetObjectHandle)
         #   self.setJointStateHandle = rospy.ServiceProxy('/vrep/simRosSetJointState',simRosSetJointState)
            
            for s in joint_names:
                resp = getHandle(s)
                self.j.handles.data.append(resp.handle)
          #      self.jhandles.append(resp.handle)
                
            
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
        print (self.j)
        self.pubCom2vrep = rospy.Publisher('/vrep/command', JointSetStateData, queue_size=1)
      
        
    def update(self):
        t = rospy.get_time()
        #t=t.secs
        w=0.3;
        a=pi/2
        self.j.values.data=[a*sin(t*w),
              a*sin(t*w*2),
                            a*sin(t*w),a*sin(t*w*0.7),
                            a*sin(t*w*2),a*sin(t*w),a*sin(t*w)]
        data=[a*sin(t*w),
              a*sin(t*w*2),
                            a*sin(t*w),a*sin(t*w),
                            a*sin(t*w*2),a*sin(t*w),a*sin(-t*w)]
        self.pubCom2vrep.publish(self.j)
      #  try:
            
            #print(self.setJointStateHandle(self.jhandles, self.modes, data))
       #     print(self.jhandles)
       #     print(self.modes)
       #     print(data)
       # except rospy.ServiceException, e:
       #     print "Service call failed: %s"%e
        
            

def main():
    rospy.init_node('bridge', anonymous=True)
    kvb = kuka_vrep_bridge()
    rate = rospy.Rate(200) # 10hz
    try:
        while not rospy.is_shutdown():
            kvb.update()
            rate.sleep()
    except rospy.ROSInterruptException:    
        pass

if __name__ == '__main__':
    main()
    
#    simSetObjectIntParameter(jointHandle,sim_jointintparam_motor_enabled,motorEnabledState)
#simSetObjectIntParameter(jointHandle,sim_jointintparam_ctrl_enabled,ctrlEnabledState)
#simSetJointMode(jointHandle,mode,options)
        