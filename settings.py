from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QGridLayout, \
    QFileDialog,  QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import os
import configparser

config = configparser.ConfigParser()


# noinspection PyArgumentList
class Settings(QWidget):
    """
    Settings popup window. This window is set modal.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("resources\\main_icon.ico"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Set window modal
        self.setGeometry(300, 300, 350, 150)

        self.default_dirpath_in = None
        self.default_dirpath_out = None
        self.testing_mode_status = False
        self.check_current_settings()
        self.make_interface()
        self.add_widget_actions()

    def make_interface(self):
        self.default_dirpath_in_field = QLineEdit()
        self.default_dirpath_in_browse = QPushButton("Browse")
        default_dirpath_in_label = QLabel("Default input directory")
        self.default_dirpath_in_field.setText(self.default_dirpath_in)

        self.default_dirpath_out_field = QLineEdit()
        self.default_dirpath_out_browse = QPushButton("Browse")
        default_dirpath_out_label = QLabel("Default output directory")
        self.default_dirpath_out_field.setText(self.default_dirpath_out)

        self.testing_mode_checkbox = QCheckBox()
        testing_mode_checkbox_label = QLabel("Testing mode")
        self.testing_mode_checkbox.setChecked(self.testing_mode_status)

        self.apply_btn = QPushButton("Apply")
        self.cancel_btn = QPushButton("Cancel")

        top_grid = QGridLayout()
        bottom_grid = QGridLayout()
        bottom_grid.setColumnStretch(2, 1)

        top_grid.addWidget(default_dirpath_in_label, 0, 0)
        top_grid.addWidget(self.default_dirpath_in_field, 1, 0)
        top_grid.addWidget(self.default_dirpath_in_browse, 1, 1)
        top_grid.addWidget(default_dirpath_out_label, 2, 0)
        top_grid.addWidget(self.default_dirpath_out_field, 3, 0)
        top_grid.addWidget(self.default_dirpath_out_browse, 3, 1)

        bottom_grid.addWidget(testing_mode_checkbox_label, 0, 0)
        bottom_grid.addWidget(self.testing_mode_checkbox, 0, 1)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.apply_btn)
        hbox.addWidget(self.cancel_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(top_grid)
        vbox.addLayout(bottom_grid)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def add_widget_actions(self):
        self.apply_btn.clicked.connect(self.set_settings)
        self.cancel_btn.clicked.connect(self.close_window)
        self.default_dirpath_in_browse.clicked.connect(self.set_default_dir_in)
        self.default_dirpath_out_browse.clicked.connect(self.set_default_dir_out)

    def check_current_settings(self):
        default_dirpath_in = get_setting("path_in")
        default_dirpath_out = get_setting("path_out")
        testing_mode = get_setting("testing", boolean=True)

        if default_dirpath_in == "__file__":
            default_dirpath_in = os.path.dirname(__file__)
        if default_dirpath_out == "__file__":
            default_dirpath_out = os.path.dirname(__file__)
        if testing_mode:
            self.testing_mode_status = True

        self.default_dirpath_in = default_dirpath_in
        self.default_dirpath_out = default_dirpath_out

    def set_default_dir_in(self):
        new_directory = QFileDialog.getExistingDirectory(self, "Choose a default input directory")
        self.default_dirpath_in_field.setText(new_directory)

    def set_default_dir_out(self):
        new_directory = QFileDialog.getExistingDirectory(self, "Choose a default output directory")
        self.default_dirpath_out_field.setText(new_directory)

    def set_settings(self):
        config_path = "resources\\settings.ini"
        section = "CURRENT"
        new_default_in_dir = self.default_dirpath_in_field.text()
        new_default_out_dir = self.default_dirpath_out_field.text()
        testing_mode_status = str(self.testing_mode_checkbox.isChecked())

        config.read(config_path)

        config.set(section, "path_in", new_default_in_dir)
        config.set(section, "path_out", new_default_out_dir)
        config.set(section, "testing", testing_mode_status)

        with open(config_path, "w") as config_file:
            config.write(config_file)

        self.close()

    def close_window(self):
        self.close()


def get_setting(value: str, section: str = "CURRENT", boolean: bool = False):
    config.read("resources\\settings.ini")
    if not boolean:
        current_value = config.get(section, value)
    else:
        current_value = config.getboolean(section, value)
    return current_value


def check_resources():
    """
    Checks if settings.ini file exists. If it doesn't, make it with a premade fields and comments.
    """
    config_exists = os.path.isfile("resources\\settings.ini")

    if not config_exists:
        a = "; Default values can safely be modified as long as paths lead to existing directories and testing value " \
            "is boolean.\n" \
            "; Accepted booleans: yes/no, on/off, true/false, 1/0.\n" \
            "; if default paths are marked as __file__ the program's working directory will be used for them.\n\n" \
            "; Settings can be reset by deleting this .ini file and rebooting the program or by removing every value " \
            "under section\n" \
            "; [CURRENT]. However, by using latter way dont remove the section title itself.\n\n" \
            "[DEFAULT]\n" \
            "path_in = __file__\n" \
            "path_out = __file__\n" \
            "testing = False\n\n" \
            "[CURRENT]\n"
        with open("resources\\settings.ini", "w") as file:
            file.write(a)
