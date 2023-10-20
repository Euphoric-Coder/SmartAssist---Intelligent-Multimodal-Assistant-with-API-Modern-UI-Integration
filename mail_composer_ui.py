from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import os
import sys

sizes_of_font = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
HTML_EXTENSIONS = [".htm", ".html"]

def splitext(p):
    return os.path.splitext(p)[1].lower()

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(900, 800)
        layout = QVBoxLayout()
        self.mail_composer = QTextEdit()
        self.path = "./email.html"

        layout.addWidget(self.mail_composer)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.menuBar().setNativeMenuBar(False)

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.mail_composer.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in sizes_of_font])
        self.fontsize.currentIndexChanged.connect(
    lambda index: self.mail_composer.setFontPointSize(float(self.fontsize.currentText()))
)

        format_toolbar.addWidget(self.fontsize)

        self.bold_action = QAction(
            QIcon(os.path.join("images", "edit-bold.png")), "Bold", self
        )
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.fromString("Ctrl+B"))
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(
            lambda x: self.mail_composer.setFontWeight(
                QFont.Weight.Bold if x else QFont.Weight.Normal
            )
        )
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        self.italic_action = QAction(
            QIcon(os.path.join("images", "edit-italic.png")), "Italic", self
        )
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.fromString("Ctrl+I"))
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.mail_composer.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)

        self.underline_action = QAction(
            QIcon(os.path.join("images", "edit-underline.png")), "Underline", self
        )
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.fromString("Ctrl+U"))
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.mail_composer.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        format_menu.addSeparator()

        self.alignl_action = QAction(
            QIcon(os.path.join("images", "edit-alignment.png")), "Align left", self
        )
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(
            lambda: self.mail_composer.setAlignment(Qt.AlignmentFlag.AlignLeft)
        )
        format_toolbar.addAction(self.alignl_action)
        format_menu.addAction(self.alignl_action)

        self.alignc_action = QAction(
            QIcon(os.path.join("images", "edit-alignment-center.png")),
            "Align center",
            self,
        )
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(
            lambda: self.mail_composer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        )
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)

        self.alignr_action = QAction(
            QIcon(os.path.join("images", "edit-alignment-right.png")),
            "Align right",
            self,
        )
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(
            lambda: self.mail_composer.setAlignment(Qt.AlignmentFlag.AlignRight)
        )
        format_toolbar.addAction(self.alignr_action)
        format_menu.addAction(self.alignr_action)

        self.alignj_action = QAction(
            QIcon(os.path.join("images", "edit-alignment-justify.png")), "Justify", self
        )
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(
            lambda: self.mail_composer.setAlignment(Qt.AlignmentFlag.AlignJustify)
        )
        format_toolbar.addAction(self.alignj_action)
        format_menu.addAction(self.alignj_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)

        format_menu.addSeparator()

        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
        ]

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        edit_menu = self.menuBar().addMenu("&Edit")

        edit_actions = [
            (
                os.path.join("images", "scissors.png"),
                "Cut",
                "Cut selected text",
                QKeySequence.StandardKey.Cut,
                self.mail_composer.cut,
            ),
            (
                os.path.join("images", "document-copy.png"),
                "Copy",
                "Copy selected text",
                QKeySequence.StandardKey.Copy,
                self.mail_composer.copy,
            ),
            (
                os.path.join("images", "clipboard-paste-document-text.png"),
                "Paste",
                "Paste from clipboard",
                QKeySequence.StandardKey.Paste,
                self.mail_composer.paste,
            ),
            (
                os.path.join("images", "selection-input.png"),
                "Select all",
                "Select all text",
                QKeySequence.StandardKey.SelectAll,
                self.mail_composer.selectAll,
            ),
        ]

        self.removeToolBar(edit_toolbar)

        for icon_path, text, status_tip, shortcut, connect_func in edit_actions:
            action = QAction(QIcon(icon_path), text, self)
            action.setStatusTip(status_tip)
            action.setShortcut(shortcut)
            action.triggered.connect(connect_func)
            edit_toolbar.addAction(action)
            edit_menu.addAction(action)

        edit_menu.addSeparator()

        file_toolbar = QToolBar("Send Email !!!")
        file_toolbar.setIconSize(QSize(25, 25))
        self.removeToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&Send Email")

        saveas_file_action = QAction(
            QIcon(os.path.join("images", "disk--pencil.png")), "Send the email...", self
        )
        saveas_file_action.setStatusTip("Save current page to specified file")
        QKeySequence.StandardKey.Save
        saveas_file_action.triggered.connect(self.send_mail)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        self.mode_updater()
        self.update_title()
        self.show()

    def mode_stopper(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def mode_updater(self):
        self.mode_stopper(self._format_actions, True)

        self.fonts.setCurrentFont(self.mail_composer.currentFont())
        # self.fontsize.setCurrentText(str(int(self.mail_composer.fontPointSize())))
        self.fontsize.currentIndexChanged.connect(
    lambda index: self.mail_composer.setFontPointSize(float(self.fontsize.itemText(index)))
)

        self.italic_action.setChecked(self.mail_composer.fontItalic())
        self.underline_action.setChecked(self.mail_composer.fontUnderline())
        self.bold_action.setChecked(
            self.mail_composer.fontWeight() == QFont.Weight.Bold
        )

        self.alignl_action.setChecked(
            self.mail_composer.alignment() == Qt.AlignmentFlag.AlignLeft
        )
        self.alignc_action.setChecked(
            self.mail_composer.alignment() == Qt.AlignmentFlag.AlignCenter
        )
        self.alignr_action.setChecked(
            self.mail_composer.alignment() == Qt.AlignmentFlag.AlignRight
        )
        self.alignj_action.setChecked(
            self.mail_composer.alignment() == Qt.AlignmentFlag.AlignJustify
        )

        self.mode_stopper(self._format_actions, False)

    def send_mail(self):
        text = self.mail_composer.toHtml()

        try:
            with open(self.path, "w") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def update_title(self):
        self.setWindowTitle("%s" % (self.path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Mail Composer")

    window = MainWindow()
    sys.exit(app.exec())
