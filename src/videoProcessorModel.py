import os, cv2, copy, numpy as np, transforms3d, mediapipe as mp
from src.Blendshapes import blendshapes
from src.pylivelinkface import PyLiveLinkFace,FaceBlendShape
from mediapipe.framework.formats import landmark_pb2 
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils.blendshape_calculator import BlendshapeCalculator
from utils.face_geometry import (PCF, get_metric_landmarks, procrustes_landmark_basis)
from utils.collectionLists import MediapipeBlendShape, filter_landmarks, blendshape_names, blendshape_indices
from utils.debugger import debugger as dbg

d = dbg()
FaceLandmarkerResult = vision.FaceLandmarkerResult

base_options = python.BaseOptions(model_asset_path='models/face_landmarker_v2_with_blendshapes.task')

options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)

detector = vision.FaceLandmarker.create_from_options(options)

# points of the face model that will be used for SolvePnP later
points_idx = [33, 263, 61, 291, 199]
points_idx = points_idx + [key for (key, val) in procrustes_landmark_basis]
points_idx = list(set(points_idx))
points_idx.sort()

# Calculates the 3d rotation and 3d landmarks from the 2d landmarks
def calculate_rotation(face_landmarks, pcf: PCF, image_shape):
    frame_width, frame_height, channels = image_shape
    focal_length = frame_width
    center = (frame_width / 2, frame_height / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
        dtype="double",
    )

    dist_coeff = np.zeros((4, 1))

    landmarks = np.array(
        [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark[:468]]

    )
    landmarks = landmarks.T

    metric_landmarks, pose_transform_mat = get_metric_landmarks(
        landmarks.copy(), pcf
    )

    model_points = metric_landmarks[0:3, points_idx].T
    image_points = (
        landmarks[0:2, points_idx].T
        * np.array([frame_width, frame_height])[None, :]
    )

    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeff,
        flags=cv2.SOLVEPNP_ITERATIVE,
    )

    return pose_transform_mat, metric_landmarks, rotation_vector, translation_vector


class videoProcessor():
    def __init__(self, model, source = "video.mp4") -> None:
        self.source = source
        self.frame = 0
        self.model = model
        
        self.blendshape_calculator = BlendshapeCalculator()
        
        self.image_height, self.image_width, channels = (720, 1280, 3) # 720x1280 for normal webcam
        focal_length = self.image_width
        center = (self.image_width/2, self.image_height/2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]],
            dtype = "double",
        )

        self.live_link_face = PyLiveLinkFace(fps=30, filter_size = 4)
        self.pcf = PCF(
            near=1,
            far=10000,
            frame_height=self.image_height,
            frame_width=self.image_width,
            fy=camera_matrix[1, 1],
        )

        self.output = []

    def process(self):
        cap = cv2.VideoCapture(self.source)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)
        
        while cap is not None and cap.isOpened():
            success, image = cap.read()
            if not success:
                break
        
            print('Processing frame: ' + str(self.frame))
            img = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=image
            )

            detection_result = detector.detect(img)
            # self.f_l
            # self.m_l 
            frame = []
            if len(detection_result.face_landmarks) > 0:
                for i in detection_result.face_landmarks[0]:
                    frame.append(dict(x=i.x, y=i.y, z=i.z))
        
                landmark_subset = landmark_pb2.NormalizedLandmarkList(
                    landmark=frame)
                frames_landmarks = []
                frames_landmarks.append(landmark_subset)

                for face_landmarks in frames_landmarks:
                    pose_transform_mat, metric_landmarks, rotation_vector, translation_vector = calculate_rotation(face_landmarks, self.pcf, (self.image_width, self.image_height, 3))  

                    #=====comment these 2 lines to remove cheek fix
                    # self.blendshape_calculator.calculate_blendshapes(
                    #     self.live_link_face, metric_landmarks[0:3].T, face_landmarks.landmark)

                    # calculate the head rotation out of the pose matrix
                    eulerAngles = transforms3d.euler.mat2euler(pose_transform_mat)
                    pitch = -eulerAngles[0]
                    yaw = eulerAngles[1]
                    roll = eulerAngles[2]
                    self.live_link_face.set_blendshape(
                        FaceBlendShape.HeadPitch, pitch)
                    self.live_link_face.set_blendshape(
                        FaceBlendShape.HeadRoll, roll)
                    self.live_link_face.set_blendshape(FaceBlendShape.HeadYaw, yaw)

            frame_input = []
            for i in filter_landmarks:
                frame_input.append([frame[i]['x'], frame[i]['y']])
            self.frame+=1
            if len(frame_input) > 0:
                output_data = blendshapes(self.model, frame_input)
                self.setBlendShapeValues(output_data[0])
                self.output.append(copy.deepcopy(self.live_link_face))
        return self.output
    
    def setBlendShapeValues(self, blendshape_values):
        # 'eyeBlinkLeft', 'eyeBlinkRight'
        to_ignore = ['_neutral',
                     'eyeLookDownLeft',
                     'eyeLookDownRight',
                     'eyeLookInLeft',
                     'eyeLookInRight',
                     'eyeLookOutLeft',
                     'eyeLookOutRight',
                     'eyeLookUpLeft',
                     'eyeLookUpRight']
        for index, name in blendshape_indices.items():
            if name in to_ignore:
                continue
            self.live_link_face.set_blendshape(FaceBlendShape(MediapipeBlendShape[name].value), blendshape_values[index])
            # self.live_link_face.set_blendshape(FaceBlendShape.JawOpen, 1 - blendshape_values[27])
        return