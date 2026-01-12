from PyQt6 import QtCore, QtGui, QtWidgets
from qfluentwidgets.components.layout.flow_layout import FlowLayout
from qfluentwidgets.components.widgets.card_widget import CardWidget


class DraggableCard(CardWidget):
    def __init__(self, card_id: str, parent=None) -> None:
        super().__init__(parent=parent)
        self.card_id = card_id
        self._drag_start: QtCore.QPoint | None = None
        self._edit_mode = False
        self._delete_button: QtWidgets.QToolButton | None = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))

    def mousePressEvent(self, event) -> None:
        if not self._edit_mode:
            return
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_start = event.position().toPoint()
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ClosedHandCursor))
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if not self._edit_mode:
            return
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if not self._edit_mode:
            return
        if self._drag_start is None:
            return
        if (
            event.position().toPoint() - self._drag_start
        ).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return

        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        mime.setData('application/x-card-id', self.card_id.encode('utf-8'))
        drag.setMimeData(mime)
        drag.setPixmap(self.grab())
        drag.setHotSpot(self._drag_start)
        drag.exec(QtCore.Qt.DropAction.MoveAction)

    def set_edit_mode(self, enabled: bool) -> None:
        self._edit_mode = enabled
        if self._delete_button:
            self._delete_button.setVisible(enabled)

    def set_delete_button(self, button: QtWidgets.QToolButton) -> None:
        self._delete_button = button
        button.setVisible(self._edit_mode)


class CardFlowContainer(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.flow_layout = FlowLayout(self, needAni=False, isTight=True)
        self.flow_layout.setHorizontalSpacing(16)
        self.flow_layout.setVerticalSpacing(16)
        self.flow_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.flow_layout)
        self._cards: dict[str, DraggableCard] = {}

    def add_card(self, card: DraggableCard) -> None:
        self._cards[card.card_id] = card
        self.flow_layout.addWidget(card)

    def set_edit_mode(self, enabled: bool) -> None:
        for card in self._cards.values():
            card.set_edit_mode(enabled)

    def set_card_visible(self, card_id: str, visible: bool) -> None:
        card = self._cards.get(card_id)
        if card:
            card.setVisible(visible)

    def card_ids(self) -> list[str]:
        return [card_id for card_id, card in self._cards.items() if card.isVisible()]

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasFormat('application/x-card-id'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event) -> None:
        if event.mimeData().hasFormat('application/x-card-id'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        if not event.mimeData().hasFormat('application/x-card-id'):
            event.ignore()
            return

        card_id = bytes(event.mimeData().data('application/x-card-id')).decode('utf-8')
        card = self._cards.get(card_id)
        if not card:
            event.ignore()
            return

        pos = event.position().toPoint()
        index = self._target_index(pos, card)
        self._reinsert_card(card, index)
        event.acceptProposedAction()

    def _reinsert_card(self, card: DraggableCard, index: int) -> None:
        current_index = self._index_of(card)
        if current_index is None:
            return
        if index > current_index:
            index -= 1
        self.flow_layout.removeWidget(card)
        max_index = self.flow_layout.count()
        index = max(0, min(index, max_index))
        self.flow_layout.insertWidget(index, card)
        card.show()

    def _index_of(self, card: DraggableCard) -> int | None:
        for i in range(self.flow_layout.count()):
            item = self.flow_layout.itemAt(i)
            if item and item.widget() is card:
                return i
        return None

    def _target_index(self, pos: QtCore.QPoint, dragged_card: DraggableCard) -> int:
        widgets: list[QtWidgets.QWidget] = []
        for i in range(self.flow_layout.count()):
            item = self.flow_layout.itemAt(i)
            if item and item.widget():
                widgets.append(item.widget())

        if not widgets:
            return 0

        best_index = len(widgets)
        best_distance = None
        for i, widget in enumerate(widgets):
            if widget is dragged_card:
                continue
            center = widget.geometry().center()
            distance = (center - pos).manhattanLength()
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_index = i

        if best_index == len(widgets):
            return len(widgets)

        center = widgets[best_index].geometry().center()
        if pos.x() > center.x() or pos.y() > center.y():
            return best_index + 1
        return best_index
