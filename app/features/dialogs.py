from qfluentwidgets import LineEdit, MessageBox, MessageBoxBase, SubtitleLabel


class ProfileIdDialog(MessageBoxBase):
    def __init__(
        self,
        title: str,
        label: str,
        placeholder: str,
        ok_text: str,
        cancel_text: str,
        error_title: str,
        error_body: str,
        default: str = '',
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title, self)
        self._error_title = error_title
        self._error_body = error_body
        self.inputEdit = LineEdit(self)
        self.inputEdit.setPlaceholderText(placeholder)
        if default:
            self.inputEdit.setText(default)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(SubtitleLabel(label, self))
        self.viewLayout.addWidget(self.inputEdit)

        self.yesButton.setText(ok_text)
        self.cancelButton.setText(cancel_text)
        self.widget.setMinimumWidth(360)

    def validate(self) -> bool:
        if self.inputEdit.text().strip():
            return True
        MessageBox.error(
            title=self._error_title,
            content=self._error_body,
            parent=self
        ).exec()
        return False
