import tkinter as tk
import cv2
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

class VideoCaptureApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.idx = 0
        
        self.vid = cv2.VideoCapture(1)
        
        self.canvas_video = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas_video.pack(side=tk.LEFT)
        
        self.canvas_image = tk.Canvas(window, width=300, height=300)
        self.canvas_image.pack(side=tk.RIGHT)
        
        self.btn_start_stop = tk.Button(window, text="Start", width=10, command=self.toggle_start_stop)
        self.btn_start_stop.pack(anchor=tk.CENTER, expand=True)
        
        self.is_playing = False
        self.update()
        
        self.window.mainloop()
    
    def toggle_start_stop(self):
        if self.is_playing:
            self.btn_start_stop.config(text="Start")
        else:
            self.btn_start_stop.config(text="Stop")
        self.is_playing = not self.is_playing
        
    def update(self):
        ret, frame = self.vid.read()
        if ret:
            if self.is_playing:
                image_paths = ["f.png", "b.png", "l.png", "r.png"]
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame)
                if results.multi_hand_landmarks:
                    draw.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
                    hand_landmarks = results.multi_hand_landmarks[0]
        
                    base = hand_landmarks.landmark[0]
                    centro = hand_landmarks.landmark[13]

                    pulgar = hand_landmarks.landmark[4]
                    indice = hand_landmarks.landmark[8]
                    medio = hand_landmarks.landmark[12]
                    anular = hand_landmarks.landmark[16]
                    menique = hand_landmarks.landmark[20]

                    
                    pulgar_d = math.sqrt((base.x - pulgar.x)**2 + (base.y - pulgar.y)**2 + (base.z - pulgar.z)**2)
                    indice_d = math.sqrt((base.x - indice.x)**2 + (base.y - indice.y)**2 + (base.z - indice.z)**2)
                    medio_d = math.sqrt((base.x - medio.x)**2 + (base.y - medio.y)**2 + (base.z - medio.z)**2)
                    anular_d = math.sqrt((base.x - anular.x)**2 + (base.y - anular.y)**2 + (base.z - anular.z)**2)
                    menique_d = math.sqrt((base.x - menique.x)**2 + (base.y - menique.y)**2 + (base.z - menique.z)**2)

                    #Avanza
                    if pulgar_d < 0.29 and indice_d > 0.35 and medio_d > 0.35 and anular_d > 0.35 and menique_d > 0.35:
                        self.idx = 0

                    #Avanza Derecha
                    elif pulgar_d < 0.29 and indice_d > 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d < 0.35:
                        self.idx = 3

                    #Avanza Izquierda
                    elif pulgar_d < 0.29 and indice_d < 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d > 0.35:
                        self.idx = 2

                    #Reversa
                    elif pulgar_d > 0.29 and indice_d < 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d < 0.35:
                        self.idx = 1

                image = Image.open(image_paths[self.idx])
                image = image.resize((300,300))
                image_tk = ImageTk.PhotoImage(image)
                self.canvas_image.create_image(0, 0, anchor=tk.NW, image=image_tk)
                self.canvas_image.img = image_tk 

                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.canvas_video.create_image(0, 0, anchor=tk.NW, image=img)
                self.canvas_video.img = img
                
        self.window.after(10, self.update)
        
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the VideoCaptureApp class
VideoCaptureApp(tk.Tk(), "Tkinter Video Capture")
