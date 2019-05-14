import pyrealsense2 as rs

from pprint import pprint
import numpy as np
import cv2

# Get realsense pipeline
pipe = rs.pipeline()

# Configure the pipeline
cfg = rs.config()
cfg.enable_stream(rs.stream.pose) # Positional data (translation, rotation, velocity etc)
cfg.enable_stream(rs.stream.fisheye, 1) # Left camera
cfg.enable_stream(rs.stream.fisheye, 2) # Right camera

# Prints a list of available streams, not all are supported by each device
print('Available streams:')
pprint(dir(rs.stream))

# Start the configured pipeline
pipe.start(cfg)

try:
    for _ in range(10000):
        frames = pipe.wait_for_frames()

        left = frames.get_fisheye_frame(1)
        left_data = np.asanyarray(left.get_data())

        right = frames.get_fisheye_frame(2)
        right_data = np.asanyarray(right.get_data())
        h,  w = left_data.shape[:2]
        mtx=np.array([[285.629349, 0.000000, 421.755510],[0.000000, 287.216162, 387.112779],[0.000000, 0.000000, 1.000000]])
        dist=np.array([-0.232094, 0.036002, 0.003086, 0.003522, 0.000000])
        rec=np.array([[0.987407, 0.025541, 0.156124],[0.021770, 0.999430, 0.025817],[0.156694, 0.022093, 0.987400]])
        proj=np.array([[297.923209, 0.000000, 412.454276, 0.000000],[0.000000, 297.923209, 398.625719, 0.000000],[ 0.000000,0.000000, 1.000000, 0.000000]])
        mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,np.eye(3),proj,(w,h),cv2.CV_32FC1)
        dst_left = cv2.remap(left_data,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)

        mtx1=np.array([[265.879331, 0.000000, 421.388842],[ 0.000000, 267.722657, 404.000467],[0.000000, 0.000000, 1.000000]])
        dist1=np.array([-0.201737, 0.028530, -0.002716, 0.000891, 0.000000])
        rec1=np.array([[0.993738, 0.020699, 0.109798, -0.023336, 0.999468, 0.022783, -0.109268, -0.025203, 0.993693]])
        proj1=np.array([[297.923209, 0.000000, 412.454276, -196.472363],[0.000000, 297.923209, 398.625719, 0.000000],[ 0.000000,0.000000, 1.000000, 0.000000]])
        mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,np.eye(3),proj,(w,h),cv2.CV_32FC1)
        dst_right = cv2.remap(right_data,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)


        # show the calibrated image

        cv2.imshow('left', dst_left)
        cv2.imshow('left_ori', left_data)
        cv2.imshow('right', dst_right)
        cv2.imshow('right_ori', right_data)
        pose = frames.get_pose_frame()
        if pose:
            data = pose.get_pose_data()
            print('\nFrame number: ', pose.frame_number)
            print('Position: ', data.translation)
            print('Velocity: ', data.velocity)
            print('Acceleration: ', data.acceleration)
            print('Rotation: ', data.rotation)


        cv2.waitKey(50)

finally:
    pipe.stop()
