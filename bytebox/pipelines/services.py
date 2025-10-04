
from typing import Any
from bytebox.pipelines.models import PipelineModel, PipelineStepModel

def execute_pipeline(pipeline: PipelineModel):
    pipeline_steps = pipeline.pipeline_steps
    for step in pipeline_steps:
        # TODO:L 
        # Create a task and insert into tasks.
        # The worker will then pick up the next task as it has finished the current step. 
        pass