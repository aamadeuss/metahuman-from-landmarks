from mediapipe.python.solutions import face_mesh, drawing_utils, drawing_styles
import threading
import socket
import random
import time
from src.pylivelinkface import PyLiveLinkFace, FaceBlendShape

class sender():
    def __init__(self, live_link_faces, fps, ip = '127.0.0.1', port = 11111) -> None:
        
        self.live_link_faces = live_link_faces
        self.index = 0
        
        self.ip = ip
        self.upd_port = port

        self.timestep = 1./fps

        self.lock = threading.Lock()
        self.got_new_data = False
        self.network_data = b''
        self.network_thread = threading.Thread(target=self._network_loop, daemon=True)

    def start(self):
        self.network_thread.start()
        while True:
            if not self.push_data():
                break

    def _network_loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect((self.ip, self.upd_port))
            while True:
                # print (time.time())
                with self.lock:
                    if self.got_new_data:
                        sock.sendall(self.network_data)
                        with open('blendshapes.txt', 'a') as f:
                            for i in FaceBlendShape:
                                f.write(str(i)[15:] + ': ' + str(PyLiveLinkFace.decode(self.network_data)[1].get_blendshape(i)) + '\n')
                        self.got_new_data = False
                # print (time.time())
                time.sleep(0.001)

    def push_data(self):
        target_time = time.time()
        if self.index >= len(self.live_link_faces):
            return False
        live_link_face_data = self.live_link_faces[self.index]
        with self.lock:
            self.got_new_data = True
            self.network_data = live_link_face_data.encode()
            time.sleep(random.uniform(0, self.timestep/2.))
        self.index += 1
        target_time += self.timestep
        time.sleep(max(0, target_time - time.time()))
        return True
    
    def disconnect(self):
        self.network_thread.join()
        