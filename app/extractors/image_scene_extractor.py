import os
import urllib.request

import torch
from PIL import Image
from torchvision import models, transforms

from app.extractors.media_extraction_strategy import MediaExtractionStrategy


class ImageSceneExtractor(MediaExtractionStrategy):
    PLACES365_URL = (
        "http://places2.csail.mit.edu/models_places365/resnet18_places365.pth.tar"
    )
    LABELS_URL = "https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt"
    LABELS_FILE = "scene_categories.txt"

    def __init__(self):
        self.scene_model = self._load_model()
        self.scene_model.eval()
        self.transform = self._build_transform()
        self.labels = self._load_labels()

    def extract(self, file_path: str) -> dict:
        if not self.labels:
            return {"scene_type": None}

        try:
            image = Image.open(file_path).convert("RGB")
            input_tensor = self.transform(image).unsqueeze(0)

            with torch.no_grad():
                output = self.scene_model(input_tensor)
                probs = torch.nn.functional.softmax(output, dim=1)
                idx = torch.argmax(probs, dim=1).item()

            return {"scene_type": self.labels[idx]}
        except Exception:
            return {"scene_type": None}

    def _build_transform(self):
        return transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

    def _load_model(self):
        try:
            model = models.resnet18(num_classes=365)
            state_dict = torch.hub.load_state_dict_from_url(
                self.PLACES365_URL, map_location="cpu"
            )
            cleaned_state = {
                k.replace("module.", ""): v for k, v in state_dict["state_dict"].items()
            }
            model.load_state_dict(cleaned_state)

            return model
        except Exception:
            raise

    def _load_labels(self):
        try:
            dir_path = os.path.dirname(__file__)
            label_path = os.path.join(dir_path, self.LABELS_FILE)

            if not os.path.exists(label_path):
                urllib.request.urlretrieve(self.LABELS_URL, label_path)

            with open(label_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            return [line.strip().split(" ")[0][3:] for line in lines]

        except Exception:
            return []
