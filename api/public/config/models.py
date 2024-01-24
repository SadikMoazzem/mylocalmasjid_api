import uuid
import enum

from sqlmodel import Field, SQLModel

class ConfigOption(str, enum.Enum):
    hijri_adjustment = "hijri_adjustment"

class ConfigBase(SQLModel):
    __tablename__ = 'config'

    config_option: ConfigOption = Field()

    value: str

    class Config:
        json_schema_extra = {
            "example": {
                "config_option": "hijri_adjustment",
                "value": "0"
            }
        }


class Config(ConfigBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class ConfigCreate(ConfigBase):
    pass
