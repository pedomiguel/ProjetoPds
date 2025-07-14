from PIL import Image
from colorthief import ColorThief
import torch
import os
from torchvision import models, transforms

import face_recognition

from .media_metadata_extractor import MediaMetadataExtractor


class ImageMetadataExtractor(MediaMetadataExtractor):
    def __init__(self):
        self.scene_model = self.load_places365_model()
        self.scene_model.eval()

        self.scene_transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        self.scene_labels = self._load_places365_labels()

        self.object_model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.object_model.eval()
        self.object_transform = transforms.Compose([transforms.ToTensor()])

        self.COCO_INSTANCE_CATEGORY_NAMES = [
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

    def extract(self, file_path: str) -> dict:
        metadata = self._extract_basic_metadata(file_path)

        metadata["dominant_color"] = self._extract_dominant_color(file_path)
        metadata["face_count"] = self._extract_faces(file_path)
        metadata["scene_type"] = self._extract_scene_type(file_path)
        metadata["objects_detected"] = self._extract_objects(file_path)

        return metadata

    def _extract_dominant_color(self, file_path: str):
        try:
            color_thief = ColorThief(file_path)
            return color_thief.get_color(quality=1)
        except Exception as e:
            print(f"Error extracting dominant color: {e}")
            return None

    def _extract_faces(self, file_path: str):
        try:
            image_array = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(image_array)
            return len(face_locations)
        except Exception as e:
            print(f"Error extracting faces: {e}")
            return None

    def _extract_scene_type(self, file_path: str):
        try:
            if not self.scene_labels:
                print("Scene labels not loaded.")
                return None

            img = Image.open(file_path).convert("RGB")
            input_tensor = self.scene_transform(img).unsqueeze(0)

            with torch.no_grad():
                logits = self.scene_model(input_tensor)
                probs = torch.nn.functional.softmax(logits, dim=1)
                top_idx = torch.argmax(probs, dim=1).item()

            return self.scene_labels[top_idx]
        except Exception as e:
            print(f"Error extracting scene type: {e}")
            return None

    def load_places365_model(self):

        model = models.resnet18(num_classes=365)

        state_dict = torch.hub.load_state_dict_from_url(
            "http://places2.csail.mit.edu/models_places365/resnet18_places365.pth.tar",
            map_location="cpu",
        )

        corrected_state_dict = {
            k.replace("module.", ""): v for k, v in state_dict["state_dict"].items()
        }

        model.load_state_dict(corrected_state_dict)

        model.eval()
        return model

    def _load_places365_labels(self):
        try:
            import urllib.request

            local_dir = os.path.join(os.path.dirname(__file__), "places365")
            os.makedirs(local_dir, exist_ok=True)

            label_path = os.path.join(local_dir, "categories_places365.txt")
            label_url = "https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt"

            if not os.path.exists(label_path):
                urllib.request.urlretrieve(label_url, label_path)

            with open(label_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            return [line.strip().split(" ")[0][3:] for line in lines]
        except Exception as e:
            print(f"Error loading Places365 labels: {e}")
            return []

    def _extract_objects(self, file_path: str):
        try:
            image = Image.open(file_path).convert("RGB")
            input_tensor = self.object_transform(image).unsqueeze(0)
            with torch.no_grad():
                outputs = self.object_model(input_tensor)[0]

            detected = [
                self.COCO_INSTANCE_CATEGORY_NAMES[label]
                for label, score in zip(outputs["labels"], outputs["scores"])
                if score > 0.7
            ]
            return list(set(detected))
        except Exception:
            return []

    def _extract_basic_metadata(self, file_path: str) -> dict:
        with Image.open(file_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": {"width": img.width, "height": img.height},
            }
