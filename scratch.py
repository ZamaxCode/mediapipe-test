import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

save = 1
while cap.isOpened():
    ret, frame = cap.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

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
            print("Avanza -", pulgar_d)

        #Avanza Derecha
        elif pulgar_d < 0.29 and indice_d > 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d < 0.35:
            print("Avanza Derecha -", pulgar_d)

        #Avanza Izquierda
        elif pulgar_d < 0.29 and indice_d < 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d > 0.35:
            print("Avanza Izquierda -", pulgar_d)

        #Reversa
        elif pulgar_d > 0.29 and indice_d < 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d < 0.35:
            print("Reversa -", pulgar_d)

        #Reversa Derecha
        elif pulgar_d > 0.29 and indice_d > 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d < 0.35:
            print("Reversa Derecha -", pulgar_d)

        #Reversa Izquierda
        elif pulgar_d > 0.29 and indice_d < 0.35 and medio_d < 0.35 and anular_d < 0.35 and menique_d > 0.35:
            print("Reversa Izquierda-", pulgar_d)
            
    cv2.imshow('Hand Tracking', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
