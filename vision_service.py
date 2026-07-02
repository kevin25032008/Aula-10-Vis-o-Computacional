import cv2
import numpy as np
import json
from datetime import datetime

class VisionService:
    @staticmethod
    def analisar_imagem(image_bytes: bytes) -> dict:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Não foi possível decodificar a imagem.")

        h, w, _ = img.shape
        resolucao = f"{w}x{h}"

        # Calcula a luminosidade média usando o canal V do espaço de cores HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        luminosidade = float(np.mean(hsv[:, :, 2]))

        # Calcula a nitidez usando a variância do operador Laplaciano (OpenCV puro!)
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        nitidez = float(cv2.Laplacian(cinza, cv2.CV_64F).var())

        b_med, g_med, r_med = cv2.mean(img)[:3]
        cores_pred = f"R:{int(r_med)} G:{int(g_med)} B:{int(b_med)}"

        return {
            "descricao": "Captura em tempo real processada por OpenCV.",
            "objetos": "Pronto para integração com YOLO.",
            "quantidade_pessoas": 0,
            "rostos": 0,
            "idade": "N/A",
            "emocao": "N/A",
            "cores": cores_pred,
            "luminosidade": round(luminosidade, 2),
            "nitidez": round(nitidez, 2),
            "json_resultado": json.dumps({"resolucao": resolucao, "horario": datetime.now().strftime("%H:%M:%S")})
        }