from typing import Optional

from PyQt6 import QtCore, QtWidgets
from qfluentwidgets import ComboBox
from qfluentwidgets.common import Theme, setTheme
from qfluentwidgets.common.config import isDarkTheme
from qfluentwidgets.common.translator import FluentTranslator

from app.app_config import resolve_language_code, resolve_theme_mode, save_app_settings
from app.ui_strings import UI_STRINGS


class SettingsMixin:
    def _apply_fluent_translator(self) -> None:
        locale = QtCore.QLocale(self._language_code.replace('-', '_'))
        app = QtWidgets.QApplication.instance()
        if self._fluent_translator:
            app.removeTranslator(self._fluent_translator)
        self._fluent_translator = FluentTranslator(locale)
        app.installTranslator(self._fluent_translator)

    def _apply_theme(self, theme_mode: str, save: bool) -> None:
        theme = resolve_theme_mode(theme_mode)
        setTheme(theme, save=save)
        self._apply_palette_overrides()
        if theme_mode == 'auto':
            if not self._theme_listener.isRunning():
                self._theme_listener.start()
        else:
            if self._theme_listener.isRunning():
                self._theme_listener.requestInterruption()
                self._theme_listener.wait(1500)

    def _apply_language(self) -> None:
        def set_text(attr: str, text: str) -> None:
            widget = getattr(self, attr, None)
            if widget is not None:
                widget.setText(text)

        self.setWindowTitle(self._t('window_title'))
        set_text('home_greeting_body', self._format_greeting())
        set_text('home_title', self._t('home_title'))
        set_text('home_subtitle', self._t('home_subtitle'))
        set_text('home_quick_label', self._t('home_quick_actions'))
        set_text('home_profile_label', self._t('home_profile_title'))
        set_text('home_launch_btn', self._t('home_go_launch'))
        set_text('home_profiles_btn', self._t('home_manage_profiles'))
        set_text('home_tips_label', self._t('home_tips_title'))
        set_text('home_tips_body', self._t('home_tips_body'))
        if getattr(self, 'home_edit_btn', None) is not None:
            self.home_edit_btn.setToolTip(
                self._t('home_edit_done') if self._home_edit_mode else self._t('home_edit')
            )
        if getattr(self, 'home_add_card_btn', None) is not None:
            self.home_add_card_btn.setToolTip(self._t('home_add_card'))

        set_text('launch_title', self._t('launch_title'))
        set_text('launch_subtitle', self._t('launch_subtitle'))
        set_text('launch_group_title', self._t('launch_settings'))
        set_text('launch_label_profile', self._t('launch_current_profile'))
        set_text('launch_label_url', self._t('launch_target_url'))
        set_text('open_btn', self._t('launch_open_browser'))
        set_text('launch_profiles_btn', self._t('launch_select_profile'))
        if getattr(self, 'launch_profile_combo', None) is not None:
            if self.launch_profile_combo.currentIndex() < 0:
                self.launch_profile_combo.setPlaceholderText(self._t('launch_profile_placeholder'))

        set_text('profiles_title', self._t('profiles_title'))
        set_text('actions_label', self._t('profiles_actions'))
        set_text('new_random_btn', self._t('profiles_new_random'))
        set_text('new_ip_btn', self._t('profiles_new_from_ip'))
        set_text('delete_btn', self._t('profiles_delete'))
        set_text('refresh_btn', self._t('profiles_refresh'))
        set_text('details_header', self._t('profiles_details'))
        set_text('protection_header', self._t('profiles_protection'))
        set_text('fingerprint_header', self._t('profiles_fingerprint_title'))

        set_text('label_profile_id', self._t('field_profile_id'))
        set_text('label_user_agent', self._t('field_user_agent'))
        set_text('label_profile_browser', self._t('field_profile_browser'))
        set_text('label_timezone', self._t('field_timezone'))
        set_text('label_locale', self._t('field_locale'))
        set_text('label_screen', self._t('field_screen'))
        set_text('label_pixel_ratio', self._t('field_pixel_ratio'))
        set_text('label_hardware', self._t('field_hardware'))
        set_text('label_webgl', self._t('field_webgl'))
        set_text('label_geo', self._t('field_geo'))
        set_text('label_webrtc_mode', self._t('field_webrtc_mode'))
        set_text('label_webrtc', self._t('protect_webrtc'))
        set_text('label_canvas', self._t('protect_canvas'))
        set_text('label_webgl_protect', self._t('protect_webgl'))
        set_text('label_audio', self._t('protect_audio'))
        set_text('label_fonts', self._t('protect_fonts'))
        set_text('label_geolocation', self._t('protect_geolocation'))
        set_text('label_timezone_protect', self._t('protect_timezone'))
        set_text('label_client_hints', self._t('protect_client_hints'))

        set_text('settings_title', self._t('settings_title'))
        set_text('settings_subtitle', self._t('settings_subtitle'))
        set_text('settings_group_title', self._t('settings_title'))
        set_text('settings_label_language', self._t('settings_language'))
        set_text('settings_label_theme', self._t('settings_theme'))
        set_text('settings_onboarding_btn', self._t('settings_onboarding'))

        set_text('onboarding_welcome_title', self._t('onboarding_title'))
        set_text('onboarding_welcome_body', self._t('onboarding_body'))
        set_text('onboarding_install_title', self._t('onboarding_install_title'))
        set_text('onboarding_install_desc', self._t('onboarding_install_body'))
        set_text('onboarding_install_version_label', self._t('install_browser_version'))
        set_text('onboarding_install_btn', self._t('install_browser_action'))
        set_text('onboarding_init_title', self._t('onboarding_init_title'))
        set_text('onboarding_init_desc', self._t('onboarding_init_body'))
        set_text('onboarding_init_btn', self._t('onboarding_init_action'))
        set_text('onboarding_back_btn', self._t('onboarding_back'))
        set_text('onboarding_next_btn', self._t('onboarding_next'))
        set_text('onboarding_exit_btn', self._t('onboarding_exit'))

        set_text('nav_home', self._t('nav_home'))
        set_text('nav_launch', self._t('nav_launch'))
        set_text('nav_profiles', self._t('nav_profiles'))
        set_text('nav_browser_library', self._t('nav_browser_library'))
        set_text('nav_install_browser', self._t('nav_install_browser'))
        set_text('nav_settings', self._t('nav_settings'))

        set_text('browser_library_title', self._t('browser_library_title'))
        set_text('browser_library_subtitle', self._t('browser_library_subtitle'))
        set_text('browser_library_group_title', self._t('browser_library_group_title'))
        set_text('browser_library_refresh_btn', self._t('browser_library_refresh'))
        set_text('browser_library_install_btn', self._t('browser_library_install_button'))

        set_text('install_browser_title', self._t('install_browser_title'))
        set_text('install_browser_subtitle', self._t('install_browser_subtitle'))
        set_text('install_browser_group_title', self._t('install_browser_group_title'))
        set_text('install_label_version', self._t('install_browser_version'))
        set_text('install_browser_btn', self._t('install_browser_action'))

        self._refresh_settings_options()
        if getattr(self, '_refresh_fingerprint_controls_options', None) is not None and getattr(self, 'fingerprint_header', None) is not None:
            self._refresh_fingerprint_controls_options()

        selected_path = None
        if self._current_profile:
            try:
                selected_path = self._current_profile.base_config.browser_path
            except Exception:
                selected_path = getattr(self._current_profile, 'browser_id', None)
        if getattr(self, '_populate_profile_browser_combo', None) is not None:
            self._populate_profile_browser_combo(selected_path)
        self._update_home_profile_hint()
        self._register_palette_targets()
        self._apply_palette_overrides()

    def _register_palette_targets(self) -> None:
        names = [
            'home_greeting_body',
            'home_title',
            'home_subtitle',
            'home_quick_label',
            'home_profile_label',
            'home_profile_hint',
            'home_tips_label',
            'home_tips_body',
            'launch_group_title',
            'launch_label_profile',
            'launch_label_url',
            'label_profile_id',
            'label_user_agent',
            'label_timezone',
            'label_locale',
            'label_screen',
            'label_pixel_ratio',
            'label_hardware',
            'label_webgl',
            'label_geo',
            'label_webrtc',
            'label_canvas',
            'label_webgl_protect',
            'label_audio',
            'label_fonts',
            'label_geolocation',
            'label_timezone_protect',
            'label_client_hints',
            'protection_header',
            'fingerprint_header',
            'label_webrtc_mode',
            'settings_group_title',
            'settings_label_language',
            'settings_label_theme',
            'browser_library_title',
            'browser_library_subtitle',
            'browser_library_group_title',
            'install_browser_title',
            'install_browser_subtitle',
            'install_browser_group_title',
            'install_label_version',
            'label_profile_browser',
            'label_adapter_id',
            'label_target_url',
            'label_proxy',
            'extra_header',
        ]
        labels = []
        for name in names:
            widget = getattr(self, name, None)
            if widget is not None:
                labels.append(widget)
        self._palette_labels = labels
        self._palette_group_boxes = []

    def _apply_palette_overrides(self) -> None:
        label_style = 'color: palette(windowText);'
        input_style = 'color: palette(text);'
        if self._is_dark_theme_active():
            label_style = 'color: #f2f2f2;'
            input_style = 'color: #f2f2f2;'
        for label in self._palette_labels:
            label.setStyleSheet(label_style)

        roots = [
            getattr(self, 'profiles_content', None),
            getattr(self, 'profiles_page', None),
            getattr(self, 'launch_page', None),
            getattr(self, 'home_page', None),
            getattr(self, 'browser_library_page', None),
            getattr(self, 'install_browser_page', None),
            getattr(self, 'settings_page', None),
            getattr(self, 'onboarding_page', None),
        ]
        for root in roots:
            if root is None:
                continue
            for label in root.findChildren(QtWidgets.QLabel):
                label.setStyleSheet(label_style)
            for spin in root.findChildren(QtWidgets.QSpinBox):
                spin.setStyleSheet(input_style)
            for spin in root.findChildren(QtWidgets.QDoubleSpinBox):
                spin.setStyleSheet(input_style)
            for edit in root.findChildren(QtWidgets.QDateEdit):
                edit.setStyleSheet(input_style)
            for edit in root.findChildren(QtWidgets.QTimeEdit):
                edit.setStyleSheet(input_style)

        group_style = (
            'QGroupBox { border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; }'
            if self._is_dark_theme_active()
            else 'QGroupBox { border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 8px; }'
        )
        for group in self._palette_group_boxes:
            group.setStyleSheet(group_style)

    def _is_dark_theme_active(self) -> bool:
        return isDarkTheme()

    def _resolve_language_mode(self, index: int) -> Optional[str]:
        text = self.language_combo.itemText(index)
        if text == self._t('language_system'):
            return 'system'
        if text == self._t('language_english'):
            return 'en-US'
        if text == self._t('language_chinese'):
            return 'zh-CN'
        return None

    def _resolve_theme_mode(self, index: int) -> Optional[str]:
        text = self.theme_combo.itemText(index)
        if text == self._t('theme_auto'):
            return 'auto'
        if text == self._t('theme_light'):
            return 'light'
        if text == self._t('theme_dark'):
            return 'dark'
        return None

    def _refresh_settings_options(self) -> None:
        current_language = self.language_combo.currentData()
        current_theme = self.theme_combo.currentData()

        self.language_combo.blockSignals(True)
        self.language_combo.clear()
        self.language_combo.addItem(self._t('language_system'), 'system')
        self.language_combo.addItem(self._t('language_english'), 'en-US')
        self.language_combo.addItem(self._t('language_chinese'), 'zh-CN')
        self._set_combo_value(self.language_combo, current_language)
        self.language_combo.blockSignals(False)

        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()
        self.theme_combo.addItem(self._t('theme_auto'), 'auto')
        self.theme_combo.addItem(self._t('theme_light'), 'light')
        self.theme_combo.addItem(self._t('theme_dark'), 'dark')
        self._set_combo_value(self.theme_combo, current_theme)
        self.theme_combo.blockSignals(False)

    def _set_combo_value(self, combo: ComboBox, value: Optional[str], label: Optional[str] = None) -> bool:
        if not value:
            return False
        for idx in range(combo.count()):
            data = combo.itemData(idx)
            if data == value:
                combo.setCurrentIndex(idx)
                return True
            if label and combo.itemText(idx) == label:
                combo.setCurrentIndex(idx)
                return True
        return False

    def _sync_settings_controls(self) -> None:
        self._refresh_settings_options()
        selection = {
            'system': self._t('language_system'),
            'en-US': self._t('language_english'),
            'zh-CN': self._t('language_chinese'),
        }
        self._set_combo_value(
            self.language_combo,
            self._language_mode,
            selection.get(self._language_mode),
        )
        theme_selection = {
            'auto': self._t('theme_auto'),
            'light': self._t('theme_light'),
            'dark': self._t('theme_dark'),
        }
        self._set_combo_value(
            self.theme_combo,
            self._theme_mode,
            theme_selection.get(self._theme_mode),
        )

    def _on_language_changed(self, index: int) -> None:
        mode = self._resolve_language_mode(index)
        if not mode:
            return
        self._language_mode = mode
        self._language_code = resolve_language_code(mode)
        self._strings = UI_STRINGS[self._language_code]
        self._apply_fluent_translator()
        self._apply_language()
        self._refresh_settings_options()
        save_app_settings({'language': self._language_mode, 'theme': self._theme_mode})

    def _on_theme_changed(self, index: int) -> None:
        mode = self._resolve_theme_mode(index)
        if not mode:
            return
        self._theme_mode = mode
        self._apply_theme(self._theme_mode, save=True)
        save_app_settings({'language': self._language_mode, 'theme': self._theme_mode})

    def _on_system_theme_changed(self) -> None:
        if self._theme_mode == 'auto':
            self._apply_theme(self._theme_mode, save=False)
