# coding: utf-8

import rospy
from sensor_msgs.msg import Image
import cv2, cv_bridge
from raiv_libraries.srv import InitDirectory,InitDirectoryResponse

#
# Subscribe to the image topic (default : /usb_cam/image_raw) and display its images.
# You can save the current images with this service :
# rosservice call /record_image "data: '/home/philippe'"   (where /h
# home/philippe is the folder where the image is saved)
#

class ImageViewerOpenCV:
  def __init__(self, image_topic='/usb_cam/image_raw'):
    self.indImage = 0
    self.bridge = cv_bridge.CvBridge()
    self.image_sub = rospy.Subscriber(image_topic,
                                      Image, self.display_image)
    s = rospy.Service('record_image', InitDirectory, self.record_image)
    rospy.loginfo("Service record_image *******************************")


  def record_image(self,msg):
      repImage = msg.data
      cv2.imwrite(repImage+'/img{:04d}.png'.format(self.indImage),self.image)
      self.indImage+=1
      return InitDirectoryResponse()


  def display_image(self, msg):
    self.image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    cv2.namedWindow("window", 1)
    cv2.imshow("window", self.image)
    cv2.waitKey(5)
