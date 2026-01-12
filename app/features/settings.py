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
        self.setWindowTitle(self._t('window_title'))
        self.home_greeting_body.setText(self._format_greeting())
        self.home_title.setText(self._t('home_title'))
        self.home_subtitle.setText(self._t('home_subtitle'))
        self.home_quick_label.setText(self._t('home_quick_actions'))
        self.home_profile_label.setText(self._t('home_profile_title'))
        self.home_launch_btn.setText(self._t('home_go_launch'))
        self.home_profiles_btn.setText(self._t('home_manage_profiles'))
        self.home_tips_label.setText(self._t('home_tips_title'))
        self.home_tips_body.setText(self._t('home_tips_body'))
        self.home_edit_btn.setToolTip(
            self._t('home_edit_done') if self._home_edit_mode else self._t('home_edit')
        )
        self.home_add_card_btn.setToolTip(self._t('home_add_card'))

        self.launch_title.setText(self._t('launch_title'))
        self.launch_subtitle.setText(self._t('launch_subtitle'))
        self.launch_group_title.setText(self._t('launch_settings'))
        self.launch_label_profile.setText(self._t('launch_current_profile'))
        self.launch_label_url.setText(self._t('launch_target_url'))
        self.open_btn.setText(self._t('launch_open_browser'))
        self.launch_profiles_btn.setText(self._t('launch_select_profile'))
        if self.launch_profile_combo.currentIndex() < 0:
            self.launch_profile_combo.setPlaceholderText(self._t('launch_profile_placeholder'))

        self.profiles_title.setText(self._t('profiles_title'))
        self.actions_label.setText(self._t('profiles_actions'))
        self.new_random_btn.setText(self._t('profiles_new_random'))
        self.new_ip_btn.setText(self._t('profiles_new_from_ip'))
        self.delete_btn.setText(self._t('profiles_delete'))
        self.refresh_btn.setText(self._t('profiles_refresh'))
        self.details_header.setText(self._t('profiles_details'))
        self.protection_header.setText(self._t('profiles_protection'))

        self.label_profile_id.setText(self._t('field_profile_id'))
        self.label_user_agent.setText(self._t('field_user_agent'))
        self.label_profile_browser.setText(self._t('field_profile_browser'))
        self.label_timezone.setText(self._t('field_timezone'))
        self.label_locale.setText(self._t('field_locale'))
        self.label_screen.setText(self._t('field_screen'))
        self.label_pixel_ratio.setText(self._t('field_pixel_ratio'))
        self.label_hardware.setText(self._t('field_hardware'))
        self.label_webgl.setText(self._t('field_webgl'))
        self.label_geo.setText(self._t('field_geo'))
        self.label_webrtc.setText(self._t('protect_webrtc'))
        self.label_canvas.setText(self._t('protect_canvas'))
        self.label_webgl_protect.setText(self._t('protect_webgl'))
        self.label_audio.setText(self._t('protect_audio'))
        self.label_fonts.setText(self._t('protect_fonts'))
        self.label_geolocation.setText(self._t('protect_geolocation'))
        self.label_timezone_protect.setText(self._t('protect_timezone'))
        self.label_client_hints.setText(self._t('protect_client_hints'))

        self.settings_title.setText(self._t('settings_title'))
        self.settings_subtitle.setText(self._t('settings_subtitle'))
        self.settings_group_title.setText(self._t('settings_title'))
        self.settings_label_language.setText(self._t('settings_language'))
        self.settings_label_theme.setText(self._t('settings_theme'))
        self.settings_onboarding_btn.setText(self._t('settings_onboarding'))

        self.onboarding_welcome_title.setText(self._t('onboarding_title'))
        self.onboarding_welcome_body.setText(self._t('onboarding_body'))
        self.onboarding_install_title.setText(self._t('onboarding_install_title'))
        self.onboarding_install_desc.setText(self._t('onboarding_install_body'))
        self.onboarding_install_version_label.setText(self._t('install_browser_version'))
        self.onboarding_install_btn.setText(self._t('install_browser_action'))
        self.onboarding_init_title.setText(self._t('onboarding_init_title'))
        self.onboarding_init_desc.setText(self._t('onboarding_init_body'))
        self.onboarding_init_btn.setText(self._t('onboarding_init_action'))
        self.onboarding_back_btn.setText(self._t('onboarding_back'))
        self.onboarding_next_btn.setText(self._t('onboarding_next'))
        self.onboarding_exit_btn.setText(self._t('onboarding_exit'))

        self.nav_home.setText(self._t('nav_home'))
        self.nav_launch.setText(self._t('nav_launch'))
        self.nav_profiles.setText(self._t('nav_profiles'))
        self.nav_browser_library.setText(self._t('nav_browser_library'))
        self.nav_install_browser.setText(self._t('nav_install_browser'))
        self.nav_settings.setText(self._t('nav_settings'))

        self.browser_library_title.setText(self._t('browser_library_title'))
        self.browser_library_subtitle.setText(self._t('browser_library_subtitle'))
        self.browser_library_group_title.setText(self._t('browser_library_group_title'))
        self.browser_library_refresh_btn.setText(self._t('browser_library_refresh'))
        self.browser_library_install_btn.setText(self._t('browser_library_install_button'))

        self.install_browser_title.setText(self._t('install_browser_title'))
        self.install_browser_subtitle.setText(self._t('install_browser_subtitle'))
        self.install_browser_group_title.setText(self._t('install_browser_group_title'))
        self.install_label_version.setText(self._t('install_browser_version'))
        self.install_browser_btn.setText(self._t('install_browser_action'))

        self._refresh_settings_options()
        self._refresh_fingerprint_controls_options()
        self._populate_profile_browser_combo(
            self._current_profile.browser_id if self._current_profile else None
        )
        self._update_home_profile_hint()
        self._register_palette_targets()
        self._apply_palette_overrides()

    def _register_palette_targets(self) -> None:
        self._palette_labels = [
            self.home_greeting_body,
            self.home_title,
            self.home_subtitle,
            self.home_quick_label,
            self.home_profile_label,
            self.home_profile_hint,
            self.home_tips_label,
            self.home_tips_body,
            self.launch_group_title,
            self.launch_label_profile,
            self.launch_label_url,
            self.label_profile_id,
            self.label_user_agent,
            self.label_timezone,
            self.label_locale,
            self.label_screen,
            self.label_pixel_ratio,
            self.label_hardware,
            self.label_webgl,
            self.label_geo,
            self.label_webrtc,
            self.label_canvas,
            self.label_webgl_protect,
            self.label_audio,
            self.label_fonts,
            self.label_geolocation,
            self.label_timezone_protect,
            self.label_client_hints,
            self.protection_header,
            self.fingerprint_header,
            self.label_webrtc_mode,
            self.settings_group_title,
            self.settings_label_language,
            self.settings_label_theme,
            self.browser_library_title,
            self.browser_library_subtitle,
            self.browser_library_group_title,
            self.install_browser_title,
            self.install_browser_subtitle,
            self.install_browser_group_title,
            self.install_label_version,
            self.label_profile_browser,
        ]
        self._palette_group_boxes = []

    def _apply_palette_overrides(self) -> None:
        label_style = 'color: palette(windowText);'
        if self._is_dark_theme_active():
            label_style = 'color: #f2f2f2;'
        for label in self._palette_labels:
            label.setStyleSheet(label_style)
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
