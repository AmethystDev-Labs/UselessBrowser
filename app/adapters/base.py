from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from spoofers.profile import BaseConfig


@dataclass
class FieldSchema:
    key: str
    label: str
    type: str  # text/date/time/spin/checkbox/combo/switch/slider
    default: Any = None
    options: Optional[list[tuple[str, Any]]] = None
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    required: bool = False


@dataclass
class ValidationError:
    key: str
    message: str


@dataclass
class LaunchResult:
    page: Any


class BrowserAdapter(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def label(self) -> str:
        raise NotImplementedError

    def get_base_config_schema(self) -> list[FieldSchema]:
        return [
            FieldSchema(key='profile_id', label='Profile ID', type='text', required=True),
            FieldSchema(key='adapter_id', label='Adapter', type='text', required=True),
            FieldSchema(key='browser_path', label='Browser Path', type='text', required=False),
            FieldSchema(key='target_url', label='Target URL', type='text', required=False),
            FieldSchema(key='user_data_dir', label='User Data Dir', type='text', required=False),
            FieldSchema(key='proxy', label='Proxy', type='text', required=False),
        ]

    @abstractmethod
    def get_extra_config_schema(self) -> list[FieldSchema]:
        raise NotImplementedError

    @abstractmethod
    def validate(self, base_config: BaseConfig, extra_config: dict) -> list[ValidationError]:
        raise NotImplementedError

    @abstractmethod
    def launch(self, base_config: BaseConfig, extra_config: dict) -> LaunchResult:
        raise NotImplementedError
