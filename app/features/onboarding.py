from PyQt6 import QtCore, QtWidgets

from app.profile_utils import list_profile_entries


class OnboardingMixin:
    def _maybe_start_onboarding(self) -> None:
        if self._onboarding_checked:
            return
        self._onboarding_checked = True
        if list_profile_entries():
            return
        self._start_onboarding()

    def _start_onboarding(self) -> None:
        self._show_onboarding(reset=True)

    def _show_onboarding(self, reset: bool = False) -> None:
        self.switchTo(self.onboarding_page)
        if reset:
            self.onboarding_stack.setCurrentIndex(0)
            self._update_onboarding_nav()

    def _update_onboarding_nav(self) -> None:
        index = self.onboarding_stack.currentIndex()
        total = self.onboarding_stack.count()
        self.onboarding_back_btn.setEnabled(index > 0)
        self.onboarding_next_btn.setEnabled(index < total - 1)
        self.onboarding_next_btn.setVisible(index < total - 1)

    def _slide_to_onboarding(self, index: int, direction: int) -> None:
        current = self.onboarding_stack.currentWidget()
        next_widget = self.onboarding_stack.widget(index)
        if current is next_widget:
            return
        width = self.onboarding_stack.width()
        height = self.onboarding_stack.height()
        current.setGeometry(0, 0, width, height)
        next_widget.setGeometry(direction * width, 0, width, height)
        next_widget.show()

        anim_current = QtCore.QPropertyAnimation(current, b'pos', self)
        anim_current.setDuration(260)
        anim_current.setStartValue(QtCore.QPoint(0, 0))
        anim_current.setEndValue(QtCore.QPoint(-direction * width, 0))
        anim_next = QtCore.QPropertyAnimation(next_widget, b'pos', self)
        anim_next.setDuration(260)
        anim_next.setStartValue(QtCore.QPoint(direction * width, 0))
        anim_next.setEndValue(QtCore.QPoint(0, 0))
        group = QtCore.QParallelAnimationGroup(self)
        group.addAnimation(anim_current)
        group.addAnimation(anim_next)

        def _finish() -> None:
            self.onboarding_stack.setCurrentIndex(index)
            current.move(0, 0)
            next_widget.move(0, 0)
            self._update_onboarding_nav()

        group.finished.connect(_finish)
        self._onboarding_anim = group
        group.start()

    def _onboarding_next_step(self) -> None:
        index = self.onboarding_stack.currentIndex()
        if index >= self.onboarding_stack.count() - 1:
            return
        self._slide_to_onboarding(index + 1, direction=1)

    def _onboarding_prev_step(self) -> None:
        index = self.onboarding_stack.currentIndex()
        if index <= 0:
            return
        self._slide_to_onboarding(index - 1, direction=-1)

    def _onboarding_exit(self) -> None:
        self.switchTo(self.home_page)

    def _onboarding_init_profile(self) -> None:
        self._create_random_profile()
