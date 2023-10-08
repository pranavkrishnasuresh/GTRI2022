    box_pose = geometry_msgs.msg.PoseStamped()
    box_pose.header.frame_id = "floor"
    box_pose.pose.orientation.w = 1.0
    box_pose.pose.position.z = -0.01
    box_name = "box"
    scene.add_box(box_name, box_pose, size=(0.1, 0.1, 0.1))