from typing import Optional

from PyQt6 import QtCore, QtWidgets
from qfluentwidgets import CheckBox, ComboBox, InfoBar, InfoBarPosition, LineEdit, MessageBox, SwitchButton

from app.adapters.base import FieldSchema
from app.adapters.registry import REGISTRY, get_adapter, list_adapters
from app.features.dialogs import ProfileIdDialog
from app.profile_utils import list_profile_entries
from app.spoofers.profile import (
    BaseConfig,
    ProfileConfig,
    build_default_profile_config,
    generate_profile_from_ip,
    get_profile_path,
    load_profile,
    save_profile,
)


class ProfilesMixin:
    def refresh_profiles(self) -> None:
        self._populate_adapter_combo()
        entries = list_profile_entries()
        self.profile_list.clear()
        for entry in entries:
            item = QtWidgets.QListWidgetItem(entry['display'])
            item.setData(QtCore.Qt.ItemDataRole.UserRole, entry['id'])
            self.profile_list.addItem(item)
        self._populate_launch_profile_combo(entries, self._current_profile_id)

    def _populate_launch_profile_combo(self, entries: list[dict], current_id: Optional[str]) -> None:
        if self._updating_launch_combo:
            return
        self._updating_launch_combo = True
        self.launch_profile_combo.blockSignals(True)
        self.launch_profile_combo.clear()
        self.launch_profile_combo.addItem(self._t('launch_profile_placeholder'), None)
        selected_index = 0
        for idx, entry in enumerate(entries, start=1):
            self.launch_profile_combo.addItem(entry['display'])
            self.launch_profile_combo.setItemData(idx, entry['id'])
            if current_id and entry['id'] == current_id:
                selected_index = idx
        self.launch_profile_combo.setCurrentIndex(selected_index)
        self.launch_profile_combo.blockSignals(False)
        self._updating_launch_combo = False

    def _resolve_launch_profile_id(self, index: Optional[int] = None) -> Optional[str]:
        idx = index if index is not None else self.launch_profile_combo.currentIndex()
        if idx <= 0:
            return None
        value = None
        try:
            value = self.launch_profile_combo.itemData(idx)
        except Exception:
            value = None
        if value:
            return value
        try:
            value = self.launch_profile_combo.currentData()
        except Exception:
            value = None
        if value:
            return value
        text = ''
        try:
            text = (self.launch_profile_combo.currentText() or '').strip()
        except Exception:
            text = ''
        if not text:
            return None
        for entry in list_profile_entries():
            if entry['id'] == text or entry['display'] == text:
                return entry['id']
        return None

    def _on_launch_profile_changed(self, index: int) -> None:
        if self._updating_launch_combo:
            return
        profile_id = self._resolve_launch_profile_id(index)
        if not profile_id:
            try:
                self.profile_list.setCurrentRow(-1)
                self.profile_list.clearSelection()
            except Exception:
                pass
            self._set_profile_details(None, None)
            return
        selected = self._select_profile_by_id(profile_id)
        if not selected:
            profile = load_profile(profile_id)
            self._set_profile_details(profile_id, profile)
            if not profile:
                InfoBar.error(
                    title=self._t('info_profile_load_failed_title'),
                    content=self._t('info_profile_load_failed_body').format(profile_id=profile_id),
                    parent=self,
                    position=InfoBarPosition.TOP,
                )

    def _on_profile_selected(
        self,
        current: Optional[QtWidgets.QListWidgetItem],
        previous: Optional[QtWidgets.QListWidgetItem],
    ) -> None:
        if not current:
            return
        profile_id = current.data(QtCore.Qt.ItemDataRole.UserRole)
        profile = load_profile(profile_id)
        self._set_profile_details(profile_id, profile)
        if not profile:
            InfoBar.error(
                title=self._t('info_profile_load_failed_title'),
                content=self._t('info_profile_load_failed_body').format(profile_id=profile_id),
                parent=self,
                position=InfoBarPosition.TOP,
            )

    def _set_profile_details(self, profile_id: Optional[str], profile: Optional[ProfileConfig]) -> None:
        self._current_profile_id = profile_id
        self._current_profile = profile
        self._updating_profile_controls = True

        self.field_profile_id.setText(profile_id or '')

        if profile:
            self.field_target_url.setText(profile.base_config.target_url or '')
            self.field_proxy.setText(str(profile.base_config.proxy or ''))
            self._set_adapter_combo_value(profile.base_config.adapter_id)
            self._populate_profile_browser_combo(profile.base_config.browser_path)
            self._build_extra_config_form(profile.base_config.adapter_id)
        else:
            self.field_target_url.setText('')
            self.field_proxy.setText('')
            self.adapter_id_combo.setCurrentIndex(-1)
            self._populate_profile_browser_combo(None)
            self._clear_extra_config_form()

        self._updating_profile_controls = False
        self._update_home_profile_hint()
        entries = list_profile_entries()
        self._populate_launch_profile_combo(entries, self._current_profile_id)
        if profile_id and not any(entry['id'] == profile_id for entry in entries):
            InfoBar.warning(
                title=self._t('info_profile_sync_conflict_title'),
                content=self._t('info_profile_sync_conflict_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )

    def _select_profile_by_id(self, profile_id: str) -> bool:
        for i in range(self.profile_list.count()):
            item = self.profile_list.item(i)
            if item.data(QtCore.Qt.ItemDataRole.UserRole) == profile_id:
                self.profile_list.setCurrentItem(item)
                return True
        return False

    def _select_profile_id(self, profile_id: str) -> None:
        self._select_profile_by_id(profile_id)

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

    def _populate_adapter_combo(self) -> None:
        if self.adapter_id_combo.count() > 0:
            try:
                if self.adapter_id_combo.itemData(0) is not None:
                    return
            except Exception:
                return
        self.adapter_id_combo.blockSignals(True)
        self.adapter_id_combo.clear()
        for adapter_id, label in list_adapters():
            self.adapter_id_combo.addItem(label)
            self.adapter_id_combo.setItemData(self.adapter_id_combo.count() - 1, adapter_id)
        self.adapter_id_combo.blockSignals(False)

    def _set_adapter_combo_value(self, adapter_id: str) -> None:
        if self.adapter_id_combo.count() == 0:
            self._populate_adapter_combo()
        index = -1
        for i in range(self.adapter_id_combo.count()):
            if self.adapter_id_combo.itemData(i) == adapter_id:
                index = i
                break
        if index >= 0:
            self.adapter_id_combo.setCurrentIndex(index)
        elif self.adapter_id_combo.count():
            self.adapter_id_combo.setCurrentIndex(0)

    def _persist_profile(self) -> None:
        if not self._current_profile_id or not self._current_profile:
            return
        if not isinstance(self._current_profile, ProfileConfig):
            return
        if not save_profile(self._current_profile_id, self._current_profile):
            InfoBar.error(
                title=self._t('info_save_failed_title'),
                content=self._t('info_save_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )

    def _show_validation_error_dialog(self, message: str) -> None:
        dialog = MessageBox(self._t('info_invalid_profile_title'), message, self)
        dialog.exec()

    def _validate_current_profile(self) -> tuple[bool, str]:
        if not self._current_profile or not isinstance(self._current_profile, ProfileConfig):
            return False, 'No profile'
        adapter_id = self._current_profile.base_config.adapter_id
        if adapter_id not in REGISTRY:
            return False, 'Unknown adapter'
        adapter = get_adapter(adapter_id)
        errors = adapter.validate(self._current_profile.base_config, self._current_profile.extra_config or {})
        if errors:
            return False, errors[0].message
        return True, ''

    def _on_base_adapter_changed(self, index: int) -> None:
        combo_text = ''
        try:
            combo_text = self.adapter_id_combo.currentText()
        except Exception:
            combo_text = ''
        combo_data = None
        try:
            combo_data = self.adapter_id_combo.itemData(index)
        except Exception:
            combo_data = None
        self._log_settings(
            f'Adapter combo changed: index={index} data={combo_data} text={combo_text} '
            f'updating={self._updating_profile_controls} profile={self._current_profile_id}'
        )

        if self._updating_profile_controls or not self._current_profile:
            return
        if not isinstance(self._current_profile, ProfileConfig):
            return

        adapter_id = combo_data or self.adapter_id_combo.currentData() or None
        if not adapter_id and combo_text:
            for adapter_id_candidate, label in list_adapters():
                if label == combo_text:
                    adapter_id = adapter_id_candidate
                    break
        if not adapter_id:
            self._log_settings(f'Adapter combo changed: no adapter_id resolved (profile={self._current_profile_id})')
            return
        if adapter_id == self._current_profile.base_config.adapter_id:
            return

        prev_adapter = self._current_profile.base_config.adapter_id
        prev_extra = (self._current_profile.extra_config or {}).copy()

        self._log_settings(f'Adapter change: {prev_adapter} -> {adapter_id} (profile={self._current_profile_id})')
        self._current_profile.base_config.adapter_id = adapter_id
        self._current_profile.extra_config = {}
        self._build_extra_config_form(adapter_id)

        ok, message = self._validate_current_profile()
        if not ok:
            self._log_settings(
                f'Adapter change rejected: {adapter_id} (profile={self._current_profile_id}) reason={message}'
            )
            self._current_profile.base_config.adapter_id = prev_adapter
            self._current_profile.extra_config = prev_extra
            self._show_validation_error_dialog(message)
            self._updating_profile_controls = True
            self._set_adapter_combo_value(prev_adapter)
            self._build_extra_config_form(prev_adapter)
            self._updating_profile_controls = False
            return

        self._persist_profile()
        self._log_settings(f'Adapter change saved: {adapter_id} (profile={self._current_profile_id})')

    def _on_base_browser_changed(self, index: int) -> None:
        if self._updating_browser_combo or not self._current_profile:
            return
        if not isinstance(self._current_profile, ProfileConfig):
            return

        browser_path: Optional[str] = None
        if index > 0 and index - 1 < len(self._browser_combo_ids):
            browser_path = self._browser_combo_ids[index - 1]

        prev = self._current_profile.base_config.browser_path
        self._current_profile.base_config.browser_path = browser_path
        ok, message = self._validate_current_profile()
        if not ok:
            self._current_profile.base_config.browser_path = prev
            self._show_validation_error_dialog(message)
            self._updating_profile_controls = True
            self._populate_profile_browser_combo(prev)
            self._updating_profile_controls = False
            return

        self._log_settings(f'Profile browser path set: {browser_path}')
        self._persist_profile()

    def _populate_profile_browser_combo(self, selected_path: Optional[str]) -> None:
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
            path_value = str(entry.path)
            self.profile_browser_combo.addItem(label, path_value)
            self._browser_combo_ids.append(path_value)
            if selected_path and path_value == selected_path:
                selected_index = len(self._browser_combo_ids)
        self.profile_browser_combo.setCurrentIndex(selected_index)
        self.profile_browser_combo.blockSignals(False)
        self._updating_browser_combo = False

    def _on_base_target_url_changed(self) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        if not isinstance(self._current_profile, ProfileConfig):
            return
        prev = self._current_profile.base_config.target_url
        self._current_profile.base_config.target_url = self.field_target_url.text().strip()
        ok, message = self._validate_current_profile()
        if not ok:
            self._current_profile.base_config.target_url = prev
            self._show_validation_error_dialog(message)
            self._updating_profile_controls = True
            self.field_target_url.setText(prev or '')
            self._updating_profile_controls = False
            return
        self._persist_profile()

    def _on_base_proxy_changed(self) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        if not isinstance(self._current_profile, ProfileConfig):
            return
        prev = self._current_profile.base_config.proxy
        value = self.field_proxy.text().strip()
        self._current_profile.base_config.proxy = value or None
        ok, message = self._validate_current_profile()
        if not ok:
            self._current_profile.base_config.proxy = prev
            self._show_validation_error_dialog(message)
            self._updating_profile_controls = True
            self.field_proxy.setText(str(prev or ''))
            self._updating_profile_controls = False
            return
        self._persist_profile()

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
        profile = build_default_profile_config(profile_id, adapter_id='chromium')
        if not save_profile(profile_id, profile):
            InfoBar.error(
                title=self._t('info_save_failed_title'),
                content=self._t('info_save_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        self.refresh_profiles()

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
        spoof_profile = generate_profile_from_ip()
        if not spoof_profile:
            InfoBar.error(
                title=self._t('info_ip_failed_title'),
                content=self._t('info_ip_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        profile = ProfileConfig(
            base_config=BaseConfig(profile_id=profile_id, adapter_id='chromium'),
            extra_config=spoof_profile.to_dict(),
        )
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

    def _clear_extra_config_form(self) -> None:
        if not hasattr(self, 'extra_form'):
            return
        while self.extra_form.rowCount():
            self.extra_form.removeRow(0)
        self._extra_widgets = {}

    def _ensure_extra_defaults(self, schema: list[FieldSchema]) -> None:
        if not self._current_profile or not isinstance(self._current_profile, ProfileConfig):
            return
        extra = self._current_profile.extra_config or {}
        for field in schema:
            if field.key not in extra and field.default is not None:
                extra[field.key] = field.default
        self._current_profile.extra_config = extra

    def _build_extra_config_form(self, adapter_id: str) -> None:
        self._clear_extra_config_form()
        if not self._current_profile or not isinstance(self._current_profile, ProfileConfig):
            return
        adapter = get_adapter(adapter_id)
        schema = adapter.get_extra_config_schema()
        self._ensure_extra_defaults(schema)
        self._extra_widgets = {}
        for field in schema:
            label = QtWidgets.QLabel(field.label)
            if field.help_text:
                label.setToolTip(field.help_text)
            widget = self._make_widget_for_field(field)
            if widget is None:
                continue
            self.extra_form.addRow(label, widget)
            self._extra_widgets[field.key] = (field, widget)
        if getattr(self, '_apply_palette_overrides', None) is not None:
            self._apply_palette_overrides()

    def _make_widget_for_field(self, field: FieldSchema):
        if not self._current_profile or not isinstance(self._current_profile, ProfileConfig):
            return None
        value = (self._current_profile.extra_config or {}).get(field.key, field.default)

        if field.type == 'text':
            w = LineEdit()
            w.setText('' if value is None else str(value))
            if field.placeholder:
                w.setPlaceholderText(field.placeholder)
            w.editingFinished.connect(lambda k=field.key, ww=w: self._on_extra_changed(k, ww.text()))
            return w

        if field.type == 'checkbox':
            w = CheckBox()
            w.setChecked(bool(value))
            w.stateChanged.connect(
                lambda state, k=field.key: self._on_extra_changed(
                    k, state == QtCore.Qt.CheckState.Checked.value
                )
            )
            return w

        if field.type == 'switch':
            w = SwitchButton()
            w.setOnText('On')
            w.setOffText('Off')
            w.setChecked(bool(value))
            w.checkedChanged.connect(lambda checked, k=field.key: self._on_extra_changed(k, bool(checked)))
            return w

        if field.type == 'combo':
            w = ComboBox()
            for label, opt_value in field.options or []:
                w.addItem(label, opt_value)
            idx = -1
            for i in range(w.count()):
                if w.itemData(i) == value:
                    idx = i
                    break
            if idx >= 0:
                w.setCurrentIndex(idx)
            w.currentIndexChanged.connect(
                lambda _idx, k=field.key, ww=w: self._on_extra_changed(k, ww.currentData())
            )
            return w

        if field.type == 'spin':
            if isinstance(value, int) and (field.step is None or float(field.step).is_integer()):
                w = QtWidgets.QSpinBox()
                w.setMinimum(int(field.min) if field.min is not None else -2147483648)
                w.setMaximum(int(field.max) if field.max is not None else 2147483647)
                w.setSingleStep(int(field.step) if field.step is not None else 1)
                w.setValue(int(value))
                w.valueChanged.connect(lambda v, k=field.key: self._on_extra_changed(k, int(v)))
                return w
            w = QtWidgets.QDoubleSpinBox()
            w.setMinimum(float(field.min) if field.min is not None else -1e12)
            w.setMaximum(float(field.max) if field.max is not None else 1e12)
            w.setSingleStep(float(field.step) if field.step is not None else 0.1)
            w.setDecimals(6)
            try:
                w.setValue(float(value))
            except Exception:
                w.setValue(float(field.default) if field.default is not None else 0.0)
            w.valueChanged.connect(lambda v, k=field.key: self._on_extra_changed(k, float(v)))
            return w

        if field.type == 'slider':
            w = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
            w.setMinimum(int(field.min) if field.min is not None else 0)
            w.setMaximum(int(field.max) if field.max is not None else 100)
            w.setSingleStep(int(field.step) if field.step is not None else 1)
            try:
                w.setValue(int(value))
            except Exception:
                w.setValue(int(field.default) if field.default is not None else 0)
            w.valueChanged.connect(lambda v, k=field.key: self._on_extra_changed(k, int(v)))
            return w

        if field.type == 'date':
            w = QtWidgets.QDateEdit()
            w.setCalendarPopup(True)
            if isinstance(value, str):
                date = QtCore.QDate.fromString(value, QtCore.Qt.DateFormat.ISODate)
                if date.isValid():
                    w.setDate(date)
            w.dateChanged.connect(
                lambda d, k=field.key: self._on_extra_changed(
                    k, d.toString(QtCore.Qt.DateFormat.ISODate)
                )
            )
            return w

        if field.type == 'time':
            w = QtWidgets.QTimeEdit()
            if isinstance(value, str):
                t = QtCore.QTime.fromString(value, 'HH:mm:ss')
                if t.isValid():
                    w.setTime(t)
            w.timeChanged.connect(lambda t, k=field.key: self._on_extra_changed(k, t.toString('HH:mm:ss')))
            return w

        return None

    def _on_extra_changed(self, key: str, value) -> None:
        if self._updating_profile_controls or not self._current_profile:
            return
        if not isinstance(self._current_profile, ProfileConfig):
            return
        extra = self._current_profile.extra_config or {}
        prev = extra.get(key, None)
        extra[key] = value
        self._current_profile.extra_config = extra
        ok, message = self._validate_current_profile()
        if not ok:
            if prev is None:
                extra.pop(key, None)
            else:
                extra[key] = prev
            self._current_profile.extra_config = extra
            self._show_validation_error_dialog(message)
            self._updating_profile_controls = True
            self._build_extra_config_form(self._current_profile.base_config.adapter_id)
            self._updating_profile_controls = False
            return
        self._persist_profile()
