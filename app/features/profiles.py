import re
from typing import Optional

from PyQt6 import QtCore, QtWidgets
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBox

from app.profile_utils import list_profile_entries
from app.features.dialogs import ProfileIdDialog
from spoofers.profile import (
    SpoofProfile,
    generate_random_profile,
    generate_profile_from_ip,
    get_profile_path,
    load_profile,
    save_profile,
)


class ProfilesMixin:
    def _format_screen_label(self, profile: SpoofProfile) -> str:
        return f'{profile.screen_width} x {profile.screen_height}'

    def _format_pixel_ratio_label(self, profile: SpoofProfile) -> str:
        return f'{profile.pixel_ratio:.2f}'

    def _format_hardware_label(self, profile: SpoofProfile) -> str:
        return f'{profile.hardware_concurrency} / {profile.device_memory} GB'

    def _format_geo_label(self, profile: SpoofProfile) -> str:
        return f'{profile.latitude:.4f}, {profile.longitude:.4f} ({profile.accuracy:.0f}m)'

    def _parse_two_ints(self, text: str) -> Optional[tuple[int, int]]:
        values = re.findall(r'\d+', text)
        if len(values) < 2:
            return None
        return int(values[0]), int(values[1])

    def _parse_floats(self, text: str) -> list[float]:
        values = re.findall(r'[-+]?\d*\.?\d+', text)
        return [float(value) for value in values if value not in ('', '.', '-', '+')]

    def _persist_profile(self) -> None:
        if self._current_profile_id and not save_profile(self._current_profile_id, self._current_profile):
            InfoBar.error(
                title=self._t('info_save_failed_title'),
                content=self._t('info_save_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )

    def _refresh_fingerprint_controls_options(self) -> None:
        self.fingerprint_header.setText(self._t('profiles_fingerprint_title'))
        self.label_webrtc_mode.setText(self._t('field_webrtc_mode'))

        self._set_combo_items(
            self.combo_webrtc_mode,
            [
                (self._t('option_disable'), 'disable'),
                (self._t('option_random'), 'random'),
                (self._t('option_enable'), 'enable'),
            ],
            self._current_profile.webrtc_mode if self._current_profile else 'disable',
        )
    def _set_combo_items(self, combo, options, current_value: str) -> None:
        combo.blockSignals(True)
        combo.clear()
        for label, value in options:
            combo.addItem(label, value)
        self._set_combo_value(combo, current_value)
        combo.blockSignals(False)

    def _on_profile_combo_changed(self, key: str, combo) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        value = combo.currentData()
        if key == 'os_mode':
            self._apply_os_mode_profile(value)
            return
        self._update_profile_field(key, value)

    def _on_profile_text_changed(self, key: str, edit) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        value = edit.text().strip()
        self._update_profile_field(key, value)

    def _on_profile_int_changed(self, key: str, edit) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        text = edit.text().strip()
        if not text:
            return
        try:
            value = int(text)
        except ValueError:
            return
        self._update_profile_field(key, value)
        if key in ('hardware_concurrency', 'device_memory'):
            hardware_label = f'{self._current_profile.hardware_concurrency} / {self._current_profile.device_memory} GB'
            self.field_hardware.setText(hardware_label)

    def _apply_os_mode_profile(self, os_mode: str) -> None:
        if not self._current_profile:
            return
        self._updating_profile_controls = True
        chrome_version = self._extract_chrome_version(self._current_profile.user_agent)
        user_agent, platform, vendor = self._make_user_agent_for_os(os_mode, chrome_version)
        self._current_profile.os_mode = os_mode
        self._current_profile.user_agent = user_agent
        self._current_profile.platform = platform
        self._current_profile.vendor = vendor
        self.field_user_agent.setText(user_agent)
        self._updating_profile_controls = False
        self._update_profile_field('os_mode', os_mode)

    def _extract_chrome_version(self, user_agent: str) -> str:
        match = re.search(r'Chrome/(\d+\.\d+\.\d+\.\d+)', user_agent or '')
        if match:
            return match.group(1)
        return '131.0.0.0'

    def _make_user_agent_for_os(self, os_mode: str, chrome_version: str) -> tuple[str, str, str]:
        vendor = 'Google Inc.'
        if os_mode == 'macos':
            user_agent = (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                f'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'
            )
            platform = 'MacIntel'
        elif os_mode == 'linux':
            user_agent = (
                'Mozilla/5.0 (X11; Linux x86_64) '
                f'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'
            )
            platform = 'Linux x86_64'
        else:
            user_agent = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                f'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'
            )
            platform = 'Win32'
        return user_agent, platform, vendor

    def _update_profile_field(self, key: str, value) -> None:
        if not self._current_profile:
            return
        setattr(self._current_profile, key, value)
        self._persist_profile()

    def _on_profile_screen_changed(self) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        values = self._parse_two_ints(self.field_screen.text())
        if not values:
            self._updating_profile_controls = True
            self.field_screen.setText(self._format_screen_label(self._current_profile))
            self._updating_profile_controls = False
            return
        width, height = values
        if width <= 0 or height <= 0:
            self._updating_profile_controls = True
            self.field_screen.setText(self._format_screen_label(self._current_profile))
            self._updating_profile_controls = False
            return
        delta_width = self._current_profile.screen_width - self._current_profile.avail_width
        delta_height = self._current_profile.screen_height - self._current_profile.avail_height
        self._current_profile.screen_width = width
        self._current_profile.screen_height = height
        self._current_profile.avail_width = max(width - delta_width, 0)
        self._current_profile.avail_height = max(height - delta_height, 0)
        self._persist_profile()
        self._updating_profile_controls = True
        self.field_screen.setText(self._format_screen_label(self._current_profile))
        self._updating_profile_controls = False

    def _on_profile_pixel_ratio_changed(self) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        values = self._parse_floats(self.field_pixel_ratio.text())
        if not values:
            self._updating_profile_controls = True
            self.field_pixel_ratio.setText(self._format_pixel_ratio_label(self._current_profile))
            self._updating_profile_controls = False
            return
        ratio = values[0]
        if ratio <= 0:
            self._updating_profile_controls = True
            self.field_pixel_ratio.setText(self._format_pixel_ratio_label(self._current_profile))
            self._updating_profile_controls = False
            return
        self._current_profile.pixel_ratio = ratio
        self._persist_profile()
        self._updating_profile_controls = True
        self.field_pixel_ratio.setText(self._format_pixel_ratio_label(self._current_profile))
        self._updating_profile_controls = False

    def _on_profile_hardware_changed(self) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        values = self._parse_two_ints(self.field_hardware.text())
        if not values:
            self._updating_profile_controls = True
            self.field_hardware.setText(self._format_hardware_label(self._current_profile))
            self._updating_profile_controls = False
            return
        hardware, memory = values
        if hardware <= 0 or memory <= 0:
            self._updating_profile_controls = True
            self.field_hardware.setText(self._format_hardware_label(self._current_profile))
            self._updating_profile_controls = False
            return
        self._current_profile.hardware_concurrency = hardware
        self._current_profile.device_memory = memory
        self._persist_profile()
        self._updating_profile_controls = True
        self.field_hardware.setText(self._format_hardware_label(self._current_profile))
        self._updating_profile_controls = False

    def _on_profile_geo_changed(self) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        values = self._parse_floats(self.field_geo.text())
        if len(values) < 2:
            self._updating_profile_controls = True
            self.field_geo.setText(self._format_geo_label(self._current_profile))
            self._updating_profile_controls = False
            return
        latitude, longitude = values[0], values[1]
        accuracy = self._current_profile.accuracy
        if len(values) >= 3:
            accuracy = values[2]
        self._current_profile.latitude = latitude
        self._current_profile.longitude = longitude
        self._current_profile.accuracy = accuracy
        self._persist_profile()
        self._updating_profile_controls = True
        self.field_geo.setText(self._format_geo_label(self._current_profile))
        self._updating_profile_controls = False

    def refresh_profiles(self) -> None:
        entries = list_profile_entries()
        self.profile_list.clear()
        for entry in entries:
            item = QtWidgets.QListWidgetItem(entry['display'])
            item.setData(QtCore.Qt.ItemDataRole.UserRole, entry['id'])
            self.profile_list.addItem(item)
        self._populate_launch_profile_combo(entries, self._current_profile_id)

    def _on_profile_selected(
        self,
        current: Optional[QtWidgets.QListWidgetItem],
        previous: Optional[QtWidgets.QListWidgetItem],
    ) -> None:
        if not current:
            return
        profile_id = current.data(QtCore.Qt.ItemDataRole.UserRole)
        profile = load_profile(profile_id)
        if profile:
            self._set_profile_details(profile_id, profile)

    def _set_profile_details(self, profile_id: Optional[str], profile: Optional[SpoofProfile]) -> None:
        self._current_profile_id = profile_id
        self._current_profile = profile
        self._updating_profile_controls = True
        self.field_profile_id.setText(profile_id or '')
        self.field_user_agent.setText(profile.user_agent if profile else '')
        self.field_timezone.setText(profile.timezone if profile else '')
        self.field_locale.setText(profile.locale if profile else '')
        if profile:
            self.field_screen.setText(self._format_screen_label(profile))
            self.field_pixel_ratio.setText(self._format_pixel_ratio_label(profile))
            self.field_hardware.setText(self._format_hardware_label(profile))
            self.field_webgl.setText(profile.webgl_renderer)
            self.field_geo.setText(self._format_geo_label(profile))
        else:
            self.field_screen.setText('')
            self.field_pixel_ratio.setText('')
            self.field_hardware.setText('')
            self.field_webgl.setText('')
            self.field_geo.setText('')
        self._refresh_fingerprint_controls_options()
        self._updating_profile_controls = False

        self._update_home_profile_hint()
        if profile:
            self._populate_profile_browser_combo(profile.browser_id)
            self._set_protection_toggles(profile)
        else:
            self._populate_profile_browser_combo(None)
            self._clear_protection_toggles()

    def _populate_launch_profile_combo(self, entries: list[dict], current_id: Optional[str]) -> None:
        if self._updating_launch_combo:
            return
        self._updating_launch_combo = True
        self.launch_profile_combo.blockSignals(True)
        self.launch_profile_combo.clear()
        self.launch_profile_combo.addItem(self._t('launch_profile_placeholder'), None)
        selected_index = 0
        for idx, entry in enumerate(entries, start=1):
            self.launch_profile_combo.addItem(entry['display'], entry['id'])
            if current_id and entry['id'] == current_id:
                selected_index = idx
        self.launch_profile_combo.setCurrentIndex(selected_index)
        self.launch_profile_combo.blockSignals(False)
        self._updating_launch_combo = False

    def _on_launch_profile_changed(self, index: int) -> None:
        if self._updating_launch_combo:
            return
        profile_id = self._resolve_launch_profile_id()
        if profile_id:
            self._select_profile_by_id(profile_id)

    def _on_profile_browser_changed(self, index: int) -> None:
        if self._updating_browser_combo or not self._current_profile:
            return
        browser_id = None
        if index > 0:
            browser_id = self._browser_combo_ids[index - 1]
        self._current_profile.browser_id = browser_id
        self._log_settings(f'Profile browser set: {browser_id}')
        if self._current_profile_id:
            save_profile(self._current_profile_id, self._current_profile)

    def _populate_profile_browser_combo(self, selected_id: Optional[str]) -> None:
        if self._updating_browser_combo:
            return
        self._updating_browser_combo = True
        self.profile_browser_combo.blockSignals(True)
        self.profile_browser_combo.clear()
        self._browser_combo_ids = []
        self.profile_browser_combo.addItem(self._t('browser_auto'), None)
        selected_index = 0
        for entry in self._browser_entries:
            label = f'{entry.name} {entry.version} ({entry.source})'
            self.profile_browser_combo.addItem(label, entry.id)
            self._browser_combo_ids.append(entry.id)
            if selected_id and entry.id == selected_id:
                selected_index = len(self._browser_combo_ids)
        self.profile_browser_combo.setCurrentIndex(selected_index)
        self.profile_browser_combo.blockSignals(False)
        self._updating_browser_combo = False

    def _select_profile_by_id(self, profile_id: str) -> None:
        for i in range(self.profile_list.count()):
            item = self.profile_list.item(i)
            if item.data(QtCore.Qt.ItemDataRole.UserRole) == profile_id:
                self.profile_list.setCurrentItem(item)
                break

    def _on_protection_changed(self, checked: bool) -> None:
        if self._updating_protection or not self._current_profile:
            return
        self._current_profile.protect_webrtc = self.switch_webrtc.isChecked()
        self._current_profile.protect_canvas = self.switch_canvas.isChecked()
        self._current_profile.protect_webgl = self.switch_webgl.isChecked()
        self._current_profile.protect_audio = self.switch_audio.isChecked()
        self._current_profile.protect_fonts = self.switch_fonts.isChecked()
        self._current_profile.protect_geolocation = self.switch_geolocation.isChecked()
        self._current_profile.protect_timezone = self.switch_timezone.isChecked()
        self._current_profile.protect_client_hints = self.switch_client_hints.isChecked()
        if self._current_profile_id and not save_profile(self._current_profile_id, self._current_profile):
            InfoBar.error(
                title=self._t('info_protection_save_failed_title'),
                content=self._t('info_protection_save_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )

    def _set_protection_toggles(self, profile: SpoofProfile) -> None:
        self._updating_protection = True
        self.switch_webrtc.setChecked(profile.protect_webrtc)
        self.switch_canvas.setChecked(profile.protect_canvas)
        self.switch_webgl.setChecked(profile.protect_webgl)
        self.switch_audio.setChecked(profile.protect_audio)
        self.switch_fonts.setChecked(profile.protect_fonts)
        self.switch_geolocation.setChecked(profile.protect_geolocation)
        self.switch_timezone.setChecked(profile.protect_timezone)
        self.switch_client_hints.setChecked(profile.protect_client_hints)
        self._updating_protection = False

    def _clear_protection_toggles(self) -> None:
        self._updating_protection = True
        for toggle in (
            self.switch_webrtc,
            self.switch_canvas,
            self.switch_webgl,
            self.switch_audio,
            self.switch_fonts,
            self.switch_geolocation,
            self.switch_timezone,
            self.switch_client_hints,
        ):
            toggle.setChecked(False)
        self._updating_protection = False

    def _prompt_profile_id(self, title: str, default: str = '') -> Optional[str]:
        dialog = ProfileIdDialog(
            title=title,
            label=self._t('dialog_profile_id_label'),
            placeholder=self._t('dialog_profile_id_placeholder'),
            ok_text=self._t('dialog_profile_id_ok'),
            cancel_text=self._t('dialog_profile_id_cancel'),
            error_title=self._t('dialog_profile_id_error_title'),
            error_body=self._t('dialog_profile_id_error_body'),
            default=default,
            parent=self,
        )
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return None
        return dialog.inputEdit.text().strip()

    def _create_random_profile(self) -> None:
        profile_id = self._prompt_profile_id(self._t('profiles_new_random'))
        if not profile_id:
            return
        if get_profile_path(profile_id).exists():
            InfoBar.warning(
                title=self._t('info_profile_exists_title'),
                content=self._t('info_profile_exists_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        profile = generate_random_profile()
        if not save_profile(profile_id, profile):
            InfoBar.error(
                title=self._t('info_save_failed_title'),
                content=self._t('info_save_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return

        self.refresh_profiles()
        self._select_profile_id(profile_id)

    def _create_ip_profile(self) -> None:
        profile_id = self._prompt_profile_id(self._t('profiles_new_from_ip'))
        if not profile_id:
            return
        if get_profile_path(profile_id).exists():
            InfoBar.warning(
                title=self._t('info_profile_exists_title'),
                content=self._t('info_profile_exists_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        profile = generate_profile_from_ip()
        if not profile:
            InfoBar.error(
                title=self._t('info_ip_failed_title'),
                content=self._t('info_ip_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        if not save_profile(profile_id, profile):
            InfoBar.error(
                title=self._t('info_save_failed_title'),
                content=self._t('info_save_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return

        self.refresh_profiles()
        self._select_profile_id(profile_id)

    def _select_profile_id(self, profile_id: str) -> None:
        for i in range(self.profile_list.count()):
            item = self.profile_list.item(i)
            if item.data(QtCore.Qt.ItemDataRole.UserRole) == profile_id:
                self.profile_list.setCurrentItem(item)
                break

    def _delete_profile(self) -> None:
        if not self._current_profile_id:
            return
        dialog = MessageBox(
            self._t('confirm_delete_title'),
            self._t('confirm_delete_body').format(profile_id=self._current_profile_id),
            self,
        )
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        path = get_profile_path(self._current_profile_id)
        try:
            if path.exists():
                path.unlink()
        except Exception:
            InfoBar.error(
                title=self._t('info_delete_failed_title'),
                content=self._t('info_delete_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return

        self.refresh_profiles()
