import cv2
import mediapipe as mp
import numpy as np

# Инициализация MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh()
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Константы
W_NAME = "Eye Tracking - УВЕРСИЯ"
CAM_WIDTH = 640
CAM_HEIGHT = 480

# Инициализация видеозахвата
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

# Создание окна
cv2.namedWindow(W_NAME, cv2.WINDOW_NORMAL)

# Константы для индексов landmarks
LEFT_EYE_INDICES = [33, 133, 157, 158, 159, 160, 161, 173]  # Примерные индексы для левого глаза
RIGHT_EYE_INDICES = [362, 263, 387, 388, 389, 390, 391, 373]  # Примерные индексы для правого глаза
LEFT_IRIS_INDICES = [468, 469, 470, 471, 472]  # Индексы для левого зрачка
RIGHT_IRIS_INDICES = [473, 474, 475, 476, 477]  # Индексы для правого зрачка

# Состояние программы
video_playing = False

def get_eye_region(landmarks, eye_indices):
    """Получить координаты области глаза"""
    points = []
    for idx in eye_indices:
        landmark = landmarks.landmark[idx]
        x = int(landmark.x * CAM_WIDTH)
        y = int(landmark.y * CAM_HEIGHT)
        points.append((x, y))
    return points

def get_iris_center(landmarks, iris_indices):
    """Получить центр зрачка"""
    points = []
    for idx in iris_indices:
        landmark = landmarks.landmark[idx]
        x = int(landmark.x * CAM_WIDTH)
        y = int(landmark.y * CAM_HEIGHT)
        points.append((x, y))
    
    # Вычисляем центр зрачка как среднее арифметическое всех точек
    center_x = int(np.mean([p[0] for p in points]))
    center_y = int(np.mean([p[1] for p in points]))
    return (center_x, center_y)

def get_iris_ratio_h(landmarks, side="left"):
    """Получить горизонтальное положение зрачка относительно глаза (0-1)"""
    if side == "left":
        eye_indices = LEFT_EYE_INDICES
        iris_indices = LEFT_IRIS_INDICES
    else:
        eye_indices = RIGHT_EYE_INDICES
        iris_indices = RIGHT_IRIS_INDICES
    
    # Получаем область глаза
    eye_points = get_eye_region(landmarks, eye_indices)
    iris_center = get_iris_center(landmarks, iris_indices)
    
    # Находим крайние точки глаза по X
    eye_x_coords = [p[0] for p in eye_points]
    eye_left = min(eye_x_coords)
    eye_right = max(eye_x_coords)
    
    # Вычисляем отношение положения зрачка
    eye_width = eye_right - eye_left
    if eye_width == 0:
        return 0.5
    
    ratio = (iris_center[0] - eye_left) / eye_width
    return ratio

def get_iris_ratio_v(landmarks, side="left"):
    """Получить вертикальное положение зрачка относительно глаза (0-1)"""
    if side == "left":
        eye_indices = LEFT_EYE_INDICES
        iris_indices = LEFT_IRIS_INDICES
    else:
        eye_indices = RIGHT_EYE_INDICES
        iris_indices = RIGHT_IRIS_INDICES
    
    # Получаем область глаза
    eye_points = get_eye_region(landmarks, eye_indices)
    iris_center = get_iris_center(landmarks, iris_indices)
    
    # Находим крайние точки глаза по Y
    eye_y_coords = [p[1] for p in eye_points]
    eye_top = min(eye_y_coords)
    eye_bottom = max(eye_y_coords)
    
    # Вычисляем отношение положения зрачка
    eye_height = eye_bottom - eye_top
    if eye_height == 0:
        return 0.5
    
    ratio = (iris_center[1] - eye_top) / eye_height
    return ratio

def draw_eyes(frame, landmarks):
    """Нарисовать глаза и зрачки на кадре"""
    # Рисуем левый глаз
    left_eye_points = get_eye_region(landmarks, LEFT_EYE_INDICES)
    left_iris_center = get_iris_center(landmarks, LEFT_IRIS_INDICES)
    
    # Рисуем контур глаза
    for i in range(len(left_eye_points)):
        cv2.line(frame, left_eye_points[i], left_eye_points[(i+1)%len(left_eye_points)], (0, 255, 0), 1)# Рисуем зрачок
    cv2.circle(frame, left_iris_center, 5, (0, 0, 255), -1)
    
    # Рисуем правый глаз
    right_eye_points = get_eye_region(landmarks, RIGHT_EYE_INDICES)
    right_iris_center = get_iris_center(landmarks, RIGHT_IRIS_INDICES)
    
    # Рисуем контур глаза
    for i in range(len(right_eye_points)):
        cv2.line(frame, right_eye_points[i], right_eye_points[(i+1)%len(right_eye_points)], (0, 255, 0), 1)
    
    # Рисуем зрачок
    cv2.circle(frame, right_iris_center, 5, (0, 0, 255), -1)

def start_video():
    """Начать воспроизведение видео (заглушка)"""
    global video_playing
    print("Воспроизведение видео начато")
    video_playing = True

def stop_video():
    """Остановить воспроизведение видео (заглушка)"""
    global video_playing
    print("Воспроизведение видео остановлено")
    video_playing = False

# Основной цикл программы
try:
    while True:
        # Захват кадра
        ret, frame = cap.read()
        if not ret:
            break
        
        # Зеркальное отражение кадра
        frame = cv2.flip(frame, 1)
        
        # Изменение размера кадра
        frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))
        
        # Конвертация цвета
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Обработка кадра с помощью MediaPipe
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            
            # Получаем положение зрачков
            left_h = get_iris_ratio_h(landmarks, "left")
            right_h = get_iris_ratio_h(landmarks, "right")
            avg_h = (left_h + right_h) / 2
            
            left_v = get_iris_ratio_v(landmarks, "left")
            right_v = get_iris_ratio_v(landmarks, "right")
            avg_v = (left_v + right_v) / 2
            
            # Определяем, смотрит ли человек прямо
            horizontal_ok = 0.35 < avg_h < 0.65
            vertical_ok = 0.3 < avg_v < 0.8
            looking = horizontal_ok and vertical_ok
            
            # Рисуем глаза
            draw_eyes(frame, landmarks)
            
            # Управление воспроизведением видео
            if not looking and not video_playing:
                start_video()
            elif looking and video_playing:
                stop_video()
            
            # Отображаем предупреждение, если не смотрит прямо
            if not looking:
                cv2.putText(frame, "УВЕРСИЯ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Отображаем информацию о положении зрачков
            cv2.putText(frame, f"H: {avg_h:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(frame, f"V: {avg_v:.2f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(frame, f"Looking: {'YES' if looking else 'NO'}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if looking else (0, 0, 255), 1)
        
        # Отображаем кадр
        cv2.imshow(W_NAME, frame)
        
        # Выход по нажатию 'q' или ESC
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

except KeyboardInterrupt:
    print("Программа прервана пользователем")

finally:
    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()
    if video_playing:
        stop_video()