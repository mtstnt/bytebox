from enum import Enum
from bytebox.config.database import Base, CommonMixin
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PipelineType(Enum):
    OneShot = 0  # For one-shot execution then destroy the container.
    Stream = 1  # For streaming output and stateful container.


class PipelineModel(CommonMixin, Base):
    __tablename__ = "pipelines"

    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(Integer, nullable=False)
    steps: Mapped[list["PipelineStepModel"]] = relationship(
        "PipelineStepModel", back_populates="pipeline"
    )


class PipelineStepModel(CommonMixin, Base):
    __tablename__ = "pipeline_steps"

    pipeline_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pipeline: Mapped["PipelineModel"] = relationship(
        "PipelineModel", back_populates="steps"
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    sequence_no: Mapped[int] = mapped_column(Integer, nullable=False)
    base_image: Mapped[str] = mapped_column(String, nullable=False)
    build_instruction: Mapped[str] = mapped_column(Text, nullable=False)
    command: Mapped[str] = mapped_column(Text, nullable=False)
    config: Mapped[str] = mapped_column(Text, nullable=False)
