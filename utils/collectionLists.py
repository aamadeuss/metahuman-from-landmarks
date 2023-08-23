from enum import Enum

class MediapipeBlendShape(Enum):
    browDownLeft = 41
    browDownRight = 42
    browInnerUp = 43
    browOuterUpLeft = 44
    browOuterUpRight = 45
    cheekPuff = 46
    cheekSquintLeft = 47
    cheekSquintRight = 48
    eyeBlinkLeft = 0
    eyeBlinkRight = 7
    eyeLookDownLeft = 1
    eyeLookDownRight = 8
    eyeLookInLeft = 2
    eyeLookInRight = 9
    eyeLookOutLeft = 3
    eyeLookOutRight = 10
    eyeLookUpLeft = 4
    eyeLookUpRight = 11
    eyeSquintLeft = 5
    eyeSquintRight = 12
    eyeWideLeft = 6
    eyeWideRight = 13
    jawForward = 14
    jawLeft = 15
    jawOpen = 17
    jawRight = 16
    mouthClose = 18
    mouthDimpleLeft = 27
    mouthDimpleRight = 28
    mouthFrownLeft = 25
    mouthFrownRight = 26
    mouthFunnel = 19
    mouthLeft = 21
    mouthLowerDownLeft = 37
    mouthLowerDownRight = 38
    mouthPressLeft = 35
    mouthPressRight = 36
    mouthPucker = 20
    mouthRight = 22
    mouthRollLower = 31
    mouthRollUpper = 32
    mouthShrugLower = 33
    mouthShrugUpper = 34
    mouthSmileLeft = 23
    mouthSmileRight = 24
    mouthStretchLeft = 29
    mouthStretchRight = 30
    mouthUpperUpLeft = 39
    mouthUpperUpRight = 40
    noseSneerLeft = 49
    noseSneerRight = 50

filter_landmarks = [0, 1, 4, 5, 6, 7, 8, 10, 13, 14, 17, 21, 33, 37, 39, 40, 46, 52, 53, 54, 55, 58, 61, 63, 65, 66, 67, 70, 78, 80,
81, 82, 84, 87, 88, 91, 93, 95, 103, 105, 107, 109, 127, 132, 133, 136, 144, 145, 146, 148, 149, 150, 152, 153, 154, 155, 157,
158, 159, 160, 161, 162, 163, 168, 172, 173, 176, 178, 181, 185, 191, 195, 197, 234, 246, 249, 251, 263, 267, 269, 270, 276, 282,
283, 284, 285, 288, 291, 293, 295, 296, 297, 300, 308, 310, 311, 312, 314, 317, 318, 321, 323, 324, 332, 334, 336, 338, 356,
361, 362, 365, 373, 374, 375, 377, 378, 379, 380, 381, 382, 384, 385, 386, 387, 388, 389, 390, 397, 398, 400, 402, 405,
409, 415, 454, 466, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477]

blendshape_indices = {
    0: '_neutral',
    1: 'browDownLeft',
    2: 'browDownRight',
    3: 'browInnerUp',
    4: 'browOuterUpLeft',
    5: 'browOuterUpRight',
    6: 'cheekPuff',
    7: 'cheekSquintLeft',
    8: 'cheekSquintRight',
    9: 'eyeBlinkLeft',
    10: 'eyeBlinkRight',
    11: 'eyeLookDownLeft',
    12: 'eyeLookDownRight',
    13: 'eyeLookInLeft',
    14: 'eyeLookInRight',
    15: 'eyeLookOutLeft',
    16: 'eyeLookOutRight',
    17: 'eyeLookUpLeft',
    18: 'eyeLookUpRight',
    19: 'eyeSquintLeft',
    20: 'eyeSquintRight',
    21: 'eyeWideLeft',
    22: 'eyeWideRight',
    23: 'jawForward',
    24: 'jawLeft',
    25: 'jawOpen',
    26: 'jawRight',
    27: 'mouthClose',
    28: 'mouthDimpleLeft',
    29: 'mouthDimpleRight',
    30: 'mouthFrownLeft',
    31: 'mouthFrownRight',
    32: 'mouthFunnel',
    33: 'mouthLeft',
    34: 'mouthLowerDownLeft',
    35: 'mouthLowerDownRight',
    36: 'mouthPressLeft',
    37: 'mouthPressRight',
    38: 'mouthPucker',
    39: 'mouthRight',
    40: 'mouthRollLower',
    41: 'mouthRollUpper',
    42: 'mouthShrugLower',
    43: 'mouthShrugUpper',
    44: 'mouthSmileLeft',
    45: 'mouthSmileRight',
    46: 'mouthStretchLeft',
    47: 'mouthStretchRight',
    48: 'mouthUpperUpLeft',
    49: 'mouthUpperUpRight',
    50: 'noseSneerLeft',
    51: 'noseSneerRight'}

blendshape_names = ['_neutral',
 'browDownLeft',
 'browDownRight',
 'browInnerUp',
 'browOuterUpLeft',
 'browOuterUpRight',
 'cheekPuff',
 'cheekSquintLeft',
 'cheekSquintRight',
 'eyeBlinkLeft',
 'eyeBlinkRight',
 'eyeLookDownLeft',
 'eyeLookDownRight',
 'eyeLookInLeft',
 'eyeLookInRight',
 'eyeLookOutLeft',
 'eyeLookOutRight',
 'eyeLookUpLeft',
 'eyeLookUpRight',
 'eyeSquintLeft',
 'eyeSquintRight',
 'eyeWideLeft',
 'eyeWideRight',
 'jawForward',
 'jawLeft',
 'jawOpen',
 'jawRight',
 'mouthClose',
 'mouthDimpleLeft',
 'mouthDimpleRight',
 'mouthFrownLeft',
 'mouthFrownRight',
 'mouthFunnel',
 'mouthLeft',
 'mouthLowerDownLeft',
 'mouthLowerDownRight',
 'mouthPressLeft',
 'mouthPressRight',
 'mouthPucker',
 'mouthRight',
 'mouthRollLower',
 'mouthRollUpper',
 'mouthShrugLower',
 'mouthShrugUpper',
 'mouthSmileLeft',
 'mouthSmileRight',
 'mouthStretchLeft',
 'mouthStretchRight',
 'mouthUpperUpLeft',
 'mouthUpperUpRight',
 'noseSneerLeft',
 'noseSneerRight']
