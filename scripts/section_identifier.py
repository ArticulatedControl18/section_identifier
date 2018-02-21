#!/usr/bin/env python
import rospy
from custom_msgs.msg import *
from custom_msgs.srv import *
from std_msgs.msg import String


class SectionIdentifier:

    def __init__(self):
        # In ROS, nodes are uniquely named. If two nodes with the same
        # node are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('section_identifier', anonymous=True)
        self.isInSection = False

        self.pub = rospy.Publisher('section_identifier', String, queue_size=0)

        rospy.Subscriber("truck_state", TruckState, self.callback)
        rospy.Subscriber("section_lock", String, self.release_callback)

    def callback(self, data):
        # x > 600 || x 1500
        # y > 5900 || y < 7000
        x = data.p.x
        y = data.p.y
        rospy.loginfo("x = %s, y = %s)", String(data.p.x), String(data.p.y))
        if 600 < x < 1500 and 5900 < y < 7000 and not self.isInSection:
            self.isInSection = True
            self.pub.publish("STAPH THE TRUCK")


    def release_callback(self, data):
        if data.data == "release":
            self.isInSection = False


if __name__ == '__main__':
    s = SectionIdentifier()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
