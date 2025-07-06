from uuid import UUID
from app.models.pipeline_run_model import PipelineRun
from app.schemas.pipeline_run_schema import PipelineRunCreate
from app.repositories.repository import Repository


class PipelineRunRepository(Repository[PipelineRun, PipelineRunCreate, None]):
    @property
    def model(self) -> type[PipelineRun]:
        return PipelineRun
