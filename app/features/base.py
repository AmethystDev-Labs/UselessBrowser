class AppLogMixin:
    def _log(self, message: str) -> None:
        print(f'[APP] {message}')

    def _log_settings(self, message: str) -> None:
        print(f'[SETTINGS] {message}')
