import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# -------- SETTINGS --------
SMOOTHENING = 5
CLICK_THRESHOLD = 40
DRAG_THRESHOLD = 30
RIGHT_CLICK_THRESHOLD = 40
BOX_MARGIN = 100

# -------- FLAGS --------
click_flag = False
right_click_flag = False
dragging = False

# -------- MEDIAPIPE --------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# -------- CAMERA --------
cap = cv2.VideoCapture(0)

# -------- SCREEN SIZE --------
screen_w, screen_h = pyautogui.size()

# -------- SMOOTHING --------
prev_x, prev_y = 0, 0

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    # DRAW CONTROL BOX
    cv2.rectangle(frame, (BOX_MARGIN, BOX_MARGIN),
                  (w - BOX_MARGIN, h - BOX_MARGIN),
                  (255, 0, 255), 2)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            # -------- INDEX FINGER --------
            index_finger = hand_landmarks.landmark[8]
            x = int(index_finger.x * w)
            y = int(index_finger.y * h)

            # Draw pointer
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # -------- CURSOR MOVEMENT --------
            if BOX_MARGIN < x < w - BOX_MARGIN and BOX_MARGIN < y < h - BOX_MARGIN:

                screen_x = np.interp(x, (BOX_MARGIN, w - BOX_MARGIN), (0, screen_w))
                screen_y = np.interp(y, (BOX_MARGIN, h - BOX_MARGIN), (0, screen_h))

                curr_x = prev_x + (screen_x - prev_x) / SMOOTHENING
                curr_y = prev_y + (screen_y - prev_y) / SMOOTHENING

                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

            # -------- THUMB (for click/drag) --------
            thumb = hand_landmarks.landmark[4]
            tx = int(thumb.x * w)
            ty = int(thumb.y * h)

            distance = np.hypot(tx - x, ty - y)

            # -------- LEFT CLICK --------
            if distance < CLICK_THRESHOLD:
                if not click_flag:
                    pyautogui.click()
                    click_flag = True
                    cv2.putText(frame, "LEFT CLICK", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                click_flag = False

            # -------- DRAG --------
            if distance < DRAG_THRESHOLD:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # -------- RIGHT CLICK (INDEX + MIDDLE) --------
            middle = hand_landmarks.landmark[12]
            mx = int(middle.x * w)
            my = int(middle.y * h)

            dist2 = np.hypot(mx - x, my - y)

            if dist2 < RIGHT_CLICK_THRESHOLD:
                if not right_click_flag:
                    pyautogui.rightClick()
                    right_click_flag = True
                    cv2.putText(frame, "RIGHT CLICK", (x, y + 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                right_click_flag = False

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # -------- UI TEXT --------
    cv2.putText(frame, "Mode: Virtual Mouse", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Virtual Mouse", frame)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()