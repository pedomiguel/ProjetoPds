from typing import List, Dict

import torch
from PIL import Image
from torchvision import models, transforms

from app.extractors.media_extraction_strategy import MediaExtractionStrategy


class ImageObjectExtractor(MediaExtractionStrategy):
    COCO_LABELS: List[str] = [
        "__background__",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "dining table",
        "toilet",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]

    def __init__(self):
        self.model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model.eval()
        self.transform = transforms.Compose([transforms.ToTensor()])

    def extract(self, file_path: str) -> Dict[str, List[str]]:
        try:
            image = Image.open(file_path).convert("RGB")

            input_tensor = self.transform(image).unsqueeze(0)
            with torch.no_grad():
                outputs = self.model(input_tensor)[0]

            detected_objects = {
                self.COCO_LABELS[label]
                for label, score in zip(outputs["labels"], outputs["scores"])
                if score > 0.7
            }

            return {"objects_detected": sorted(detected_objects)}
        except Exception:
            return {"objects_detected": []}
