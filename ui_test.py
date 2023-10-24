from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import os
import sys

sizes_of_font = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class CustomTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursorPositionChanged.connect(self.update_formatting_actions)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            cursor = self.textCursor()
            current_block_format = cursor.blockFormat()
            new_block = QTextBlockFormat()

            # Copy the alignment from the current block to the new block
            new_block.setAlignment(current_block_format.alignment())

            # Set any other formatting properties here if needed

            cursor.setBlockFormat(new_block)
            cursor.insertBlock()
            self.ensureCursorVisible()
        else:
            super().keyPressEvent(event)
    
    def update_formatting_actions(self):
        cursor = self.textCursor()
        char_format = cursor.charFormat()
        block_format = cursor.blockFormat()

        # Access formatting actions and combo boxes directly
        window.fonts.setCurrentFont(QFont(char_format.font().family()))
        window.fontsize.setCurrentText(str(int(char_format.font().pointSize())))

        window.bold_action.setChecked(char_format.font().bold())
        window.italic_action.setChecked(char_format.font().italic())
        window.underline_action.setChecked(char_format.font().underline())

        window.uncheck_align_actions()
        if block_format.alignment() == Qt.AlignmentFlag.AlignLeft:
            window.align_left_action.setChecked(True)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignCenter:
            window.align_center_action.setChecked(True)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignRight:
            window.align_right_action.setChecked(True)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignJustify:
            window.align_justify_action.setChecked(True)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(900, 800)
        layout = QVBoxLayout()
        self.mail_composer = CustomTextEdit()
        self.path = "./email.html"
        self.cursor_position = None

        layout.addWidget(self.mail_composer)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.menuBar().setNativeMenuBar(False)

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.font_changed)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in sizes_of_font])
        self.fontsize.currentIndexChanged.connect(self.font_size_changed)
        format_toolbar.addWidget(self.fontsize)

        bold_icon = QIcon(resource_path("UI-IMAGES/bold.png"))
        italic_icon = QIcon(resource_path("UI-IMAGES/italic.png"))
        underline_icon = QIcon(resource_path("UI-IMAGES/underline.png"))

        self.bold_action = QAction(bold_icon, "Bold", self, checkable=True)
        self.italic_action = QAction(italic_icon, "Italic", self, checkable=True)
        self.underline_action = QAction(underline_icon, "Underline", self, checkable=True)

        # Add shortcuts to actions
        self.bold_action.setShortcut(QKeySequence.fromString("Ctrl+B"))
        self.italic_action.setShortcut(QKeySequence.fromString("Ctrl+I"))
        self.underline_action.setShortcut(QKeySequence.fromString("Ctrl+U"))

        self.bold_action.toggled.connect(self.set_bold)
        self.italic_action.toggled.connect(self.set_italic)
        self.underline_action.toggled.connect(self.set_underline)

        format_toolbar.addActions([self.bold_action, self.italic_action, self.underline_action])
        format_menu.addActions([self.bold_action, self.italic_action, self.underline_action])

        format_menu.addSeparator()

        self.align_group = QActionGroup(self)

        self.align_left_action = QAction("Align Left", self, checkable=True)
        self.align_left_action.setIcon(QIcon(resource_path("UI-IMAGES/align-left.png")))
        self.align_left_action.triggered.connect(self.set_alignment_left)
        self.align_group.addAction(self.align_left_action)
        self.align_left_action.setShortcut(QKeySequence.fromString("Ctrl+L"))

        self.align_center_action = QAction("Align Center", self, checkable=True)
        self.align_center_action.setIcon(QIcon(resource_path("UI-IMAGES/align-center.png")))
        self.align_center_action.triggered.connect(self.set_alignment_center)
        self.align_group.addAction(self.align_center_action)
        self.align_center_action.setShortcut(QKeySequence.fromString("Ctrl+E"))

        self.align_right_action = QAction("Align Right", self, checkable=True)
        self.align_right_action.setIcon(QIcon(resource_path("UI-IMAGES/align-right.png")))
        self.align_right_action.triggered.connect(self.set_alignment_right)
        self.align_group.addAction(self.align_right_action)
        self.align_right_action.setShortcut(QKeySequence.fromString("Ctrl+R"))

        self.align_justify_action = QAction("Align Justify", self, checkable=True)
        self.align_justify_action.setIcon(QIcon(resource_path("UI-IMAGES/align-justify.png")))
        self.align_justify_action.triggered.connect(self.set_alignment_justify)
        self.align_group.addAction(self.align_justify_action)
        self.align_justify_action.setShortcut(QKeySequence.fromString("Ctrl+J"))

        format_toolbar.addActions([self.align_left_action, self.align_center_action, self.align_right_action, self.align_justify_action])
        format_menu.addActions([self.align_left_action, self.align_center_action, self.align_right_action, self.align_justify_action])

        self.fonts.setCurrentFont(QFont("Arial"))
        self.fontsize.setCurrentIndex(5)

        self.mail_composer.cursorPositionChanged.connect(self.update_formatting_actions)

        self.mode_updater()
        self.update_title()
        self.show()

    def mode_stopper(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def mode_updater(self):
        self.mode_stopper([self.bold_action, self.italic_action, self.underline_action], True)

        cursor = self.mail_composer.textCursor()
        char_format = cursor.charFormat()

        self.bold_action.setChecked(char_format.font().bold())
        self.italic_action.setChecked(char_format.font().italic())
        self.underline_action.setChecked(char_format.font().underline())

        self.mode_stopper([self.bold_action, self.italic_action, self.underline_action], False)

        self.mode_stopper([self.align_left_action, self.align_center_action, self.align_right_action, self.align_justify_action], True)
        alignment = cursor.blockFormat().alignment()

        self.align_left_action.setChecked(alignment == Qt.AlignmentFlag.AlignLeft)
        self.align_center_action.setChecked(alignment == Qt.AlignmentFlag.AlignCenter)
        self.align_right_action.setChecked(alignment == Qt.AlignmentFlag.AlignRight)
        self.align_justify_action.setChecked(alignment == Qt.AlignmentFlag.AlignJustify)

        self.mode_stopper([self.align_left_action, self.align_center_action, self.align_right_action, self.align_justify_action], False)

    def font_size_changed(self, index):
        size = float(self.fontsize.itemText(index))
        cursor = self.mail_composer.textCursor()

        # Preserve existing formatting and only change font size
        char_format = QTextCharFormat()
        char_format.setFontPointSize(size)

        # Apply the modified character format to the selected text
        cursor.mergeCharFormat(char_format)
        self.mail_composer.setTextCursor(cursor)

        self.mail_composer.setFocus()
        self.mode_updater()

    def update_formatting_actions(self):
        cursor = self.mail_composer.textCursor()
        char_format = cursor.charFormat()
        block_format = cursor.blockFormat()

        # Update font style and size actions
        self.fonts.setCurrentFont(QFont(char_format.font().family()))
        self.fontsize.setCurrentText(str(int(char_format.font().pointSize())))

        self.bold_action.setChecked(char_format.font().bold())
        self.italic_action.setChecked(char_format.font().italic())
        self.underline_action.setChecked(char_format.font().underline())

        self.uncheck_align_actions()
        if block_format.alignment() == Qt.AlignmentFlag.AlignLeft:
            self.align_left_action.setChecked(True)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignCenter:
            self.align_center_action.setChecked(True)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignRight:
            self.align_right_action.setChecked(True)
        elif block_format.alignment() == Qt.AlignmentFlag.AlignJustify:
            self.align_justify_action.setChecked(True)

    def font_changed(self, font):
        cursor = self.mail_composer.textCursor()
        char_format = cursor.charFormat()

        # Preserve existing formatting properties and only change font family
        char_format.setFontFamily(font.family())

        cursor.mergeCharFormat(char_format)
        self.mail_composer.setTextCursor(cursor)
        self.mail_composer.setFocus()
        self.mode_updater()

    def font_size_changed(self, index):
        size = float(self.fontsize.itemText(index))
        cursor = self.mail_composer.textCursor()

        # Preserve existing formatting and only change font size
        char_format = QTextCharFormat()
        char_format.setFontPointSize(size)

        # Apply the modified character format to the selected text
        cursor.mergeCharFormat(char_format)
        self.mail_composer.setTextCursor(cursor)

        self.mail_composer.setFocus()
        self.mode_updater()

    def set_bold(self, bold):
        font = self.mail_composer.currentFont()
        font.setBold(bold)
        self.mail_composer.setCurrentFont(font)
        self.mail_composer.setFocus()
        self.mode_updater()

    def set_italic(self, italic):
        font = self.mail_composer.currentFont()
        font.setItalic(italic)
        self.mail_composer.setCurrentFont(font)
        self.mail_composer.setFocus()
        self.mode_updater()

    def set_underline(self, underline):
        font = self.mail_composer.currentFont()
        font.setUnderline(underline)
        self.mail_composer.setCurrentFont(font)
        self.mail_composer.setFocus()
        self.mode_updater()

    def uncheck_align_actions(self):
        for action in self.align_group.actions():
            action.setChecked(False)

    def set_alignment_left(self):
        self.uncheck_align_actions()
        self.set_alignment(Qt.AlignmentFlag.AlignLeft)

    def set_alignment_center(self):
        self.uncheck_align_actions()
        self.set_alignment(Qt.AlignmentFlag.AlignCenter)

    def set_alignment_right(self):
        self.uncheck_align_actions()
        self.set_alignment(Qt.AlignmentFlag.AlignRight)

    def set_alignment_justify(self):
        self.uncheck_align_actions()
        self.set_alignment(Qt.AlignmentFlag.AlignJustify)

    def set_alignment(self, alignment):
        cursor = self.mail_composer.textCursor()
        block_format = cursor.blockFormat()

        # Check if the provided alignment is the same as the current alignment
        if block_format.alignment() == alignment:
            # Set alignment to default left alignment if it's the same as current alignment
            alignment = Qt.AlignmentFlag.AlignLeft

        block_format.setAlignment(alignment)
        cursor.mergeBlockFormat(block_format)
        self.mail_composer.setTextCursor(cursor)
        self.mail_composer.setFocus()
        self.mode_updater()
        self.update_title()


    def update_title(self):
        self.setWindowTitle(self.path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Mail Composer")

    window = MainWindow()
    sys.exit(app.exec())
