import os

from PyQt6 import QtCore, QtWidgets


class HomeMixin:
    def _resolve_user_name(self) -> str:
        return os.environ.get('USERNAME') or os.environ.get('USER') or 'User'

    def _format_greeting(self) -> str:
        greeting = self._time_greeting()
        return f'{greeting}，{self._user_name}。<br>{self._t("home_greeting_message")}'

    def _time_greeting(self) -> str:
        hour = QtCore.QTime.currentTime().hour()
        if 0 <= hour < 6:
            return self._t('greeting_midnight')
        if 6 <= hour < 10:
            return self._t('greeting_morning')
        if 10 <= hour < 12:
            return self._t('greeting_forenoon')
        if 12 <= hour < 14:
            return self._t('greeting_noon')
        if 14 <= hour < 18:
            return self._t('greeting_afternoon')
        if 18 <= hour < 22:
            return self._t('greeting_evening')
        return self._t('greeting_midnight')

    def _toggle_home_edit_mode(self) -> None:
        self._set_home_edit_mode(not self._home_edit_mode)

    def _set_home_edit_mode(self, enabled: bool) -> None:
        self._home_edit_mode = enabled
        self.home_card_container.set_edit_mode(enabled)
        self.home_add_card_btn.setVisible(enabled)
        self.home_edit_btn.setToolTip(
            self._t('home_edit_done') if enabled else self._t('home_edit')
        )

    def _hide_home_card(self, card_id: str) -> None:
        self.home_card_container.set_card_visible(card_id, False)

    def _show_add_card_menu(self) -> None:
        menu = QtWidgets.QMenu(self)
        existing = set(self.home_card_container.card_ids())
        options = [
            ('greeting', self._t('home_card_greeting')),
            ('profile', self._t('home_card_profile')),
            ('tips', self._t('home_card_tips')),
        ]
        for card_id, label in options:
            if card_id in existing:
                continue
            action = menu.addAction(label)
            action.triggered.connect(lambda checked, cid=card_id: self._show_home_card(cid))

        if not menu.actions():
            action = menu.addAction(self._t('home_card_none'))
            action.setEnabled(False)

        menu.exec(self.home_add_card_btn.mapToGlobal(self.home_add_card_btn.rect().bottomLeft()))

    def _show_home_card(self, card_id: str) -> None:
        self.home_card_container.set_card_visible(card_id, True)

    def _update_home_profile_hint(self) -> None:
        if not self._current_profile_id:
            self.home_profile_hint.setText(self._t('home_profile_none'))
        else:
            self.home_profile_hint.setText(
                self._t('home_profile_current').format(profile_id=self._current_profile_id)
            )
