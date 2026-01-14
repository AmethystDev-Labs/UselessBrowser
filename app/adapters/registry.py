from typing import Dict, Type

from app.adapters.base import BrowserAdapter
from app.adapters.chromium import ChromiumAdapter
from app.adapters.camoufox import CamoufoxAdapter

REGISTRY: Dict[str, Type[BrowserAdapter]] = {
    'chromium': ChromiumAdapter,
    'camoufox': CamoufoxAdapter,
}

def get_adapter(adapter_id: str) -> BrowserAdapter:
    adapter_cls = REGISTRY.get(adapter_id)
    if not adapter_cls:
        return ChromiumAdapter()
    return adapter_cls()


def list_adapters() -> list[tuple[str, str]]:
    return [(adapter_id, get_adapter(adapter_id).label) for adapter_id in REGISTRY]
