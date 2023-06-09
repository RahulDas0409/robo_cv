import pyrealsense2 as rs2
import numpy as np

class RealsenseCamera:
    def __init__(self):
        self.pipeline = rs2.pipeline()
        config = rs2.config()
        
        pipeline_wrapper = rs2.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs2.camera_info.product_line))
        
        config.enable_stream(rs2.stream.depth, 640, 480, rs2.format.z16, 30)
        config.enable_stream(rs2.stream.color, 640, 480, rs2.format.bgr8, 30)
        
        decimation = rs2.decimation_filter()
        spatial = rs2.spatial_filter()
        temporal = rs2.temporal_filter()
        hole_filling = rs2.hole_filling_filter()
        depth_to_disparity = rs2.disparity_transform(True)
        disparity_to_depth = rs2.disparity_transform(False)
        
        self.profile = self.pipeline.start(config)
        
        self.align_to = rs2.stream.color
        self.align = rs2.align(self.align_to)
        
    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image
    
    def get_intrinsic(self):
        self.intr = self.profile.get_stream(rs2.stream.color).as_video_stream_profile().get_intrinsics()
        return (self.intr.ppx, self.intr.ppy, self.intr.fx, self.intr.fy)
    
    def get_extrinsic(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        
        depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)
        color_to_depth_extrin = color_frame.profile.get_extrinsics_to(depth_frame.profile)
        return depth_to_color_extrin
    
    def release(self):
        self.pipeline.stop()

if __name__ == "__main__":
    obj = RealsenseCamera()
    print(obj.get_extrinsic())