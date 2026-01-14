import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.adapters.registry import get_adapter
from spoofers.profile import build_default_profile_config, BaseConfig
from app.features.launch import resolve_effective_profile_id

def test_chromium_adapter_schema():
    adapter = get_adapter('chromium')
    schema = adapter.get_extra_config_schema()
    assert any(field.key == 'user_agent' for field in schema)
    assert any(field.key == 'timezone' for field in schema)

def test_profile_config_roundtrip():
    profile = build_default_profile_config('test@example.com', adapter_id='chromium')
    data = profile.to_dict()
    assert data['adapter_id'] == 'chromium'
    assert 'base_config' in data
    assert 'extra_config' in data

    base = BaseConfig.from_dict(data.get('base_config') or {}, 'test@example.com')
    assert base.adapter_id == 'chromium'

def test_resolve_effective_profile_id():
    assert resolve_effective_profile_id(None, None) is None
    assert resolve_effective_profile_id('p1', None) == 'p1'
    assert resolve_effective_profile_id(None, 'p2') == 'p2'
    assert resolve_effective_profile_id('p1', 'p2') == 'p1'

if __name__ == '__main__':
    test_chromium_adapter_schema()
    test_profile_config_roundtrip()
    test_resolve_effective_profile_id()
