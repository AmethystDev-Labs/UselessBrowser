from pathlib import Path
from typing import Optional

from app.adapters.base import BrowserAdapter, FieldSchema, LaunchResult, ValidationError
from app.spoofers.profile import get_profiles_dir
from app.spoofers.profile import BaseConfig, SpoofProfile


class _CamoufoxHandle:
    def __init__(self, session, context, page):
        self._session = session
        self._context = context
        self._page = page

    def quit(self) -> None:
        try:
            try:
                self._context.close()
            except Exception:
                pass
        finally:
            try:
                self._session.__exit__(None, None, None)
            except Exception:
                pass

    @property
    def page(self):
        return self._page


class CamoufoxAdapter(BrowserAdapter):
    @property
    def id(self) -> str:
        return 'camoufox'

    @property
    def label(self) -> str:
        return 'Camoufox'

    def get_extra_config_schema(self) -> list[FieldSchema]:
        return [
            FieldSchema(key='headless', label='Headless', type='switch', default=False),
            FieldSchema(key='geoip', label='GeoIP', type='switch', default=True),
            FieldSchema(key='geoip_ip', label='GeoIP IP', type='text', default=''),
            FieldSchema(key='locale', label='Locale', type='text', default=''),
            FieldSchema(key='timezone', label='Timezone', type='text', default=''),
            FieldSchema(key='proxy', label='Proxy', type='text', default=''),
            FieldSchema(key='lock_window_size', label='Lock Window Size', type='switch', default=True),
            FieldSchema(
                key='screen_width',
                label='Screen Width',
                type='spin',
                default=SpoofProfile.screen_width,
                min=1,
                max=10000,
                step=1,
            ),
            FieldSchema(
                key='screen_height',
                label='Screen Height',
                type='spin',
                default=SpoofProfile.screen_height,
                min=1,
                max=10000,
                step=1,
            ),
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

        return errors

    def launch(self, base_config: BaseConfig, extra_config: dict) -> LaunchResult:
        try:
            from camoufox.sync_api import Camoufox
        except Exception as exc:
            raise RuntimeError('Camoufox is not available in this environment') from exc

        url = base_config.target_url or 'https://example.com'
        headless = bool((extra_config or {}).get('headless', False))
        geoip_enabled = bool((extra_config or {}).get('geoip', True))
        geoip_ip = str((extra_config or {}).get('geoip_ip') or '').strip()
        geoip = None if not geoip_enabled else (geoip_ip or True)

        locale_raw = str((extra_config or {}).get('locale') or '').strip()
        timezone_id_raw = str((extra_config or {}).get('timezone') or '').strip()
        if geoip is not None:
            locale = None if not locale_raw or locale_raw == 'en-US' else locale_raw
            timezone_id = None if not timezone_id_raw or timezone_id_raw == 'America/New_York' else timezone_id_raw
        else:
            locale = locale_raw or 'en-US'
            timezone_id = timezone_id_raw or 'America/New_York'
        lock_window_size = bool((extra_config or {}).get('lock_window_size', False))
        screen_width = int((extra_config or {}).get('screen_width') or SpoofProfile.screen_width)
        screen_height = int((extra_config or {}).get('screen_height') or SpoofProfile.screen_height)

        proxy_raw = (extra_config or {}).get('proxy') or base_config.proxy or ''
        proxy: Optional[dict] = None
        if isinstance(proxy_raw, str) and proxy_raw.strip():
            proxy = {'server': proxy_raw.strip()}

        profiles_dir = get_profiles_dir()
        if base_config.user_data_dir:
            user_data_dir = Path(base_config.user_data_dir)
        else:
            user_data_dir = profiles_dir / 'camoufox' / base_config.profile_id
        user_data_dir.mkdir(parents=True, exist_ok=True)

        executable_path: Optional[str] = base_config.browser_path or None
        args: list[str] = []
        if not lock_window_size:
            args.extend([f'--width={screen_width}', f'--height={screen_height}'])
        session = Camoufox(
            persistent_context=True,
            user_data_dir=str(user_data_dir),
            headless=headless,
            proxy=proxy,
            geoip=geoip,
            locale=locale,
            timezone_id=timezone_id,
            args=args or None,
            no_viewport=not lock_window_size,
            window=(screen_width, screen_height) if lock_window_size else None,
            executable_path=executable_path,
        )
        try:
            context = session.__enter__()
        except Exception as exc:
            raise RuntimeError('Camoufox launch failed. Ensure Camoufox is installed: camoufox fetch') from exc

        try:
            page = context.pages[0] if getattr(context, 'pages', None) else None
        except Exception:
            page = None
        if page is None:
            page = context.new_page()
        page.goto(url)
        return LaunchResult(page=_CamoufoxHandle(session, context, page))
