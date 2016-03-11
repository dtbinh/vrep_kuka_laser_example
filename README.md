# vrep_kuka_laser_example
example of integration of vrep with ros

This package (tested in indigo) contains two files: 
##### kuka_bridge.py
Is a node that query for the joint handles, and command a joint position

##### kuka-with-laser.ttt
Is a vrep scene that contains a kuka robot.
- the kinematics is different from the model shipped with vrep (two joints angles are inverted w.r.t. the real robot, in that version)
- the robot has 3 laser on the tip
- the non-threated child script that
  - publish all the joints state 
  - publish the laser values (3 possibilities are tried)
  - control the joints via `simros_strmcmd_set_joint_state`

the 3 modes for publish the laser data are:
- via the `simros_strmcmd_get_float_signal` (the one actually used), the value that is published is set by `simSetFloatSignal`,
- via the `simros_strmcmd_read_proximity_sensor` (commented, shown only for one laser), the message is not really user-friendly, and
- cia the `simros_strmcmd_receive_data_from_script_function`, that runs the function `readLs`



```
-- kuka-with-laser.ttt
-- This is a threaded script, and is just an example!


--function for simros_strmcmd_receive_data_from_script_function
--[[
readLs=function(inInts,inFloats,inStrings,inBuffer)

r1,d1=simReadProximitySensor(Laser1handle)
r2,d2=simReadProximitySensor(Laser2handle)
r3,d3=simReadProximitySensor(Laser3handle)
if r1<0.5 then d1=-1 end
if r2<0.5 then d2=-1 end
if r3<0.5 then d3=-1 end
return {r1,r2,r3},{d1,d2,d3},{},''

end
]]--

if (sim_call_type==sim_childscriptcall_initialization) then 
    -- Check if the required plugin is there (libv_repExtRos.so or libv_repExtRos.dylib):
    local moduleName=0
    local moduleVersion=0
    local index=0
    local pluginNotFound=true
    while moduleName do
        moduleName,moduleVersion=simGetModuleName(index)
        if (moduleName=='Ros') then
            pluginNotFound=false
        end
        index=index+1
    end

    if (pluginNotFound) then

        -- Display an error message if the plugin was not found:
        simDisplayDialog('Error','ROS plugin was not found.&&nSimulation will not run properly',sim_dlgstyle_ok,false,nil,{0.8,0,0,0,0,0},{0.5,0,0,1,1,1})
    else

        topicName=simExtROS_enablePublisher('JointAngles',1,simros_strmcmd_get_joint_state,sim_handle_all,0,'')

--http://www.coppeliarobotics.com/helpFiles/en/rosServices.htm#simRosSetJointState
--rosservice call /vrep/simRosGetObjectHandle "LBR4p_joint1"
        local subscriberID=simExtROS_enableSubscriber('command',1,simros_strmcmd_set_joint_state,-1,-1,'')

        Laser1handle=simGetObjectHandle('Laser1')
        Laser2handle=simGetObjectHandle('Laser2')
        Laser3handle=simGetObjectHandle('Laser3')
        
        -- proximity sensor message
        --topicName=simExtROS_enablePublisher('Laser1',1,simros_strmcmd_read_proximity_sensor,Laser1handle,0,'')
        
        -- single double message
        topicName=simExtROS_enablePublisher('Laser1',1,simros_strmcmd_get_float_signal,-1,-1,'rl1')
        topicName=simExtROS_enablePublisher('Laser2',1,simros_strmcmd_get_float_signal,-1,-1,'rl2')
        topicName=simExtROS_enablePublisher('Laser3',1,simros_strmcmd_get_float_signal,-1,-1,'rl3')
        

        --topicName=simExtROS_enablePublisher('LaserValues',1,simros_strmcmd_receive_data_from_script_function,1,-1,'readLs@LBR4p')
    
    end
end 

if (sim_call_type==sim_childscriptcall_cleanup) then 
 
end 

if (sim_call_type==sim_childscriptcall_sensing) then 
--this is for the double message
r1,d1=simReadProximitySensor(Laser1handle)
r2,d2=simReadProximitySensor(Laser2handle)
r3,d3=simReadProximitySensor(Laser3handle)
if r1<0.5 then d1=-1 end
if r2<0.5 then d2=-1 end
if r3<0.5 then d3=-1 end
simSetFloatSignal('rl1',d1)
simSetFloatSignal('rl2',d2)
simSetFloatSignal('rl3',d3)

end 

if (sim_call_type==sim_childscriptcall_actuation) then 

end 

```

