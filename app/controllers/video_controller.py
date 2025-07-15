from uuid import UUID
from fastapi import Depends, File, UploadFile, Form

from app.dependencies.auth_guard import AuthGuard
from app.models import User
from app.services import PipelineRunService
# from app.schemas import MediaUpdate, MediaSingleRespose, MediaParentResponse # TODO: Create them
from .controller import BaseController

class MediaController(BaseController):
    def __init__(self,) -> None:
        super().__init__(tags=["Video"], prefix="/video")
        self._media_service = None

    def add_routes(self) -> None:
        @self.router.post("/upload", response_model=None) # Define response model
        def upload(
            file: UploadFile = File(...),
            user: User = Depends(AuthGuard.get_authenticated_user),
            pipeline: str = Form(...),
        ):
            pipeline_list = [p.strip() for p in pipeline.split(",") if p.strip()]
            media = self._media_service.run(file, pipeline_list)
            return [
                MediaSingleRespose.model_validate(children)
                for children in media.children
            ]

        @self.router.get("/download/{id}")
        def download(
            id: UUID,
            user: User = Depends(AuthGuard.get_authenticated_user)
        ):
            raise NotImplemented
