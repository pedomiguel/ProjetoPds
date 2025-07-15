import face_recognition
from app.extractors.media_extraction_strategy import MediaExtractionStrategy


class ImageFaceExtractor(MediaExtractionStrategy):
    def extract(self, file_path: str) -> dict:
        try:
            image_array = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(image_array)

            return {"face_count": len(face_locations)}
        except Exception:
            return {"face_count": None}
