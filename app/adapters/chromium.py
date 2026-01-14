from pathlib import Path
from typing import Any, Optional

from DrissionPage import ChromiumOptions, ChromiumPage

from app.adapters.base import BrowserAdapter, FieldSchema, LaunchResult, ValidationError
from app.browser_library import BROWSER_ARGS, find_chrome_path
from spoofers.profile import get_profiles_dir
from spoofers.cdp_spoofer import apply_pre_navigation_spoofing
from spoofers.profile import BaseConfig, SpoofProfile


class ChromiumAdapter(BrowserAdapter):
    @property
    def id(self) -> str:
        return 'chromium'

    @property
    def label(self) -> str:
        return 'Chromium (DrissionPage)'

    def get_extra_config_schema(self) -> list[FieldSchema]:
        return [
            FieldSchema(
                key='user_agent',
                label='User Agent',
                type='text',
                default=SpoofProfile.user_agent,
                required=True,
            ),
            FieldSchema(
                key='timezone',
                label='Timezone',
                type='text',
                default=SpoofProfile.timezone,
                required=True,
            ),
            FieldSchema(
                key='locale',
                label='Locale',
                type='text',
                default=SpoofProfile.locale,
                required=True,
            ),
            FieldSchema(key='screen_width', label='Screen Width', type='spin', default=SpoofProfile.screen_width, min=1, max=10000, step=1),
            FieldSchema(key='screen_height', label='Screen Height', type='spin', default=SpoofProfile.screen_height, min=1, max=10000, step=1),
            FieldSchema(key='pixel_ratio', label='Pixel Ratio', type='spin', default=SpoofProfile.pixel_ratio, min=0.5, max=5.0, step=0.05),
            FieldSchema(key='hardware_concurrency', label='CPU Cores', type='spin', default=SpoofProfile.hardware_concurrency, min=1, max=128, step=1),
            FieldSchema(key='device_memory', label='Device Memory (GB)', type='spin', default=SpoofProfile.device_memory, min=1, max=512, step=1),
            FieldSchema(key='webgl_renderer', label='WebGL Renderer', type='text', default=SpoofProfile.webgl_renderer),
            FieldSchema(key='latitude', label='Latitude', type='spin', default=SpoofProfile.latitude, min=-90.0, max=90.0, step=0.0001),
            FieldSchema(key='longitude', label='Longitude', type='spin', default=SpoofProfile.longitude, min=-180.0, max=180.0, step=0.0001),
            FieldSchema(key='accuracy', label='Geo Accuracy (m)', type='spin', default=SpoofProfile.accuracy, min=0.0, max=10000.0, step=1.0),
            FieldSchema(key='protect_webrtc', label='Protect WebRTC', type='switch', default=SpoofProfile.protect_webrtc),
            FieldSchema(key='protect_canvas', label='Protect Canvas', type='switch', default=SpoofProfile.protect_canvas),
            FieldSchema(key='protect_webgl', label='Protect WebGL', type='switch', default=SpoofProfile.protect_webgl),
            FieldSchema(key='protect_audio', label='Protect Audio', type='switch', default=SpoofProfile.protect_audio),
            FieldSchema(key='protect_fonts', label='Protect Fonts', type='switch', default=SpoofProfile.protect_fonts),
            FieldSchema(key='protect_geolocation', label='Protect Geolocation', type='switch', default=SpoofProfile.protect_geolocation),
            FieldSchema(key='protect_timezone', label='Protect Timezone', type='switch', default=SpoofProfile.protect_timezone),
            FieldSchema(key='protect_client_hints', label='Protect Client Hints', type='switch', default=SpoofProfile.protect_client_hints),
        ]

    def validate(self, base_config: BaseConfig, extra_config: dict) -> list[ValidationError]:
        errors: list[ValidationError] = []

        if not base_config.profile_id:
            errors.append(ValidationError(key='profile_id', message='profile_id is required'))
        if base_config.browser_path:
            try:
                if not Path(base_config.browser_path).exists():
                    errors.append(ValidationError(key='browser_path', message='browser_path does not exist'))
            except Exception:
                errors.append(ValidationError(key='browser_path', message='browser_path is invalid'))

        user_agent = str(extra_config.get('user_agent') or '')
        if 'Mozilla/5.0' not in user_agent or 'Chrome/' not in user_agent:
            errors.append(ValidationError(key='user_agent', message='user_agent must look like a Chromium UA'))

        timezone = str(extra_config.get('timezone') or '')
        if '/' not in timezone:
            errors.append(ValidationError(key='timezone', message='timezone must be an IANA timezone like America/New_York'))

        locale = str(extra_config.get('locale') or '')
        if not locale:
            errors.append(ValidationError(key='locale', message='locale is required'))

        return errors

    def launch(self, base_config: BaseConfig, extra_config: dict) -> LaunchResult:
        url = base_config.target_url or 'https://example.com'
        co = self._build_options(base_config)
        page = ChromiumPage(co)
        spoof_profile = SpoofProfile.from_dict(extra_config or {})
        apply_pre_navigation_spoofing(page, spoof_profile)
        page.get(url)
        return LaunchResult(page=page)

    def _build_options(self, base_config: BaseConfig) -> ChromiumOptions:
        co = ChromiumOptions()

        profiles_dir = get_profiles_dir()
        if base_config.user_data_dir:
            user_data_dir = Path(base_config.user_data_dir)
        else:
            user_data_dir = profiles_dir / 'chrome' / base_config.profile_id
        user_data_dir.mkdir(parents=True, exist_ok=True)
        co.set_user_data_path(str(user_data_dir))
        co.auto_port()

        co.set_argument('--disable-infobars')
        co.set_argument('--no-first-run')
        co.set_argument('--no-default-browser-check')
        co.set_argument('--disable-dev-shm-usage')

        try:
            chrome_path = base_config.browser_path or find_chrome_path()
            if chrome_path:
                co.set_browser_path(chrome_path)
            for arg in BROWSER_ARGS:
                co.set_argument(arg)
        except Exception:
            if base_config.browser_path:
                co.set_browser_path(base_config.browser_path)

        return co
