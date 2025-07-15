from app.models.pipeline_step_model import PipelineStep
from app.schemas.pipeline_step_schema import PipelineStepCreate
from app.repositories.repository import Repository


class PipelineStepRepository(Repository[PipelineStep, PipelineStepCreate, None]):
    @property
    def model(self) -> type[PipelineStep]:
        return PipelineStep
