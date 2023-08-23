from src.jsonProcessor import jsonProcessor
from src.jsonProcessor_v2 import jsonProcessor as jP
from src.videoProcessor import videoProcessor as vp
from src.videoProcessorModel import videoProcessor as vpM
from src.sender import sender
import tensorflow as tf
import time

model = tf.keras.models.load_model('models/CNN_20_softplus.keras')
# jsonP = jsonProcessor(model=model, source_folder='./output_jsons')

vidProc = vp(source='videos/scrunch.mp4')
# vidProc = vpM(model=model, source='videos/scrunch.mp4')

# results = jsonP.process()
results = vidProc.process()

input('Press Enter to send data...')

while True:
    timestep = float(input('Enter output fps: '))
    time.sleep(1)
    unrealSender = sender(results, timestep)
    unrealSender.start()
    input('Press Enter to send again...')