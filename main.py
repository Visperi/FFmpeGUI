"""
Copyright (C) 2019  Visperi
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLineEdit, \
    QGridLayout, QMainWindow, QFileDialog, QComboBox, QCheckBox
from PyQt5.QtGui import QIcon
import convert
import os


# noinspection PyArgumentList
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFmpeGUI")
        self.setGeometry(300, 300, 450, 170)
        self.icon = QIcon("resources\\main_icon.ico")
        self.make_main_layout()
        self.add_widget_actions()

    def make_main_layout(self):
        main_interface = Window()

        # Make all the labels, buttons and boxes in main interface
        self.input_path = QLineEdit()
        self.input_path_browse = QPushButton("Browse")
        input_label = QLabel("Input file")

        self.output_path = QLineEdit()
        self.output_path_browse = QPushButton("Browse")
        output_label = QLabel("Output directory")

        self.new_filename = QLineEdit()
        self.new_filename.setPlaceholderText("Leave this blank to use the original file name")
        new_filename_label = QLabel("New file name")

        self.bitrate_box = QComboBox()
        self.bitrate = "Default"
        bitrate_box_label = QLabel("Bitrate")
        bitrate_unit_label = QLabel("kbps")

        self.output_format_box = QComboBox()
        self.output_format = "MP3"
        output_format_label = QLabel("Format")

        self.make_mono_box = QCheckBox()
        self.make_mono_state = False
        make_mono_lbl = QLabel("Make mono")

        self.settings_btn = QPushButton("Settings")
        self.start_btn = QPushButton("Start")
        self.exit_btn = QPushButton("Exit")

        # Add labels, buttons and boxes into grids. The main interface is separated into two grids so it's easier to
        # control the size of the combo boxes and check boxes
        upper_grid = QGridLayout()
        lower_grid = QGridLayout()

        upper_grid.addWidget(input_label, 0, 0)
        upper_grid.addWidget(self.input_path, 0, 1)
        upper_grid.addWidget(self.input_path_browse, 0, 2)
        upper_grid.addWidget(output_label, 1, 0)
        upper_grid.addWidget(self.output_path, 1, 1)
        upper_grid.addWidget(self.output_path_browse, 1, 2)
        upper_grid.addWidget(new_filename_label, 2, 0)
        upper_grid.addWidget(self.new_filename, 2, 1)

        lower_grid.addWidget(output_format_label, 0, 0)
        lower_grid.addWidget(self.output_format_box, 0, 1)
        lower_grid.addWidget(bitrate_box_label, 0, 2)
        lower_grid.addWidget(self.bitrate_box, 0, 3)
        lower_grid.addWidget(bitrate_unit_label, 0, 4)
        lower_grid.addWidget(make_mono_lbl, 0, 5)
        lower_grid.addWidget(self.make_mono_box, 0, 6)

        # Adjust the placement of previous widgets by using horizontal and vertical box layouts.
        # addStretch() basically forces the widgets/layouts to bottom or right side of the window depending on which
        # box layout is used
        hbox = QHBoxLayout()
        hbox.addWidget(self.settings_btn)
        hbox.addStretch()
        hbox.addWidget(self.start_btn)
        hbox.addWidget(self.exit_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(upper_grid)
        vbox.addLayout(lower_grid)
        vbox.addStretch()
        vbox.addLayout(hbox)

        main_interface.setLayout(vbox)
        self.setCentralWidget(main_interface)
        self.setWindowIcon(self.icon)
        self.show()

    def add_widget_actions(self):
        output_bitrates = ["Default", "320", "256", "192", "128", "96"]
        output_formats = ["MP3", "MP4", "WAV", "WebM"]

        self.bitrate_box.addItems(output_bitrates)
        self.output_format_box.addItems(output_formats)

        self.input_path_browse.clicked.connect(self.set_input_path)
        self.output_path_browse.clicked.connect(self.set_output_path)
        self.settings_btn.clicked.connect(self.open_settings_window)
        self.start_btn.clicked.connect(self.start_ffmpeg_convert)
        self.exit_btn.clicked.connect(self.close_program)
        self.make_mono_box.stateChanged.connect(self.set_make_mono)
        self.bitrate_box.activated.connect(self.set_bitrate)
        self.output_format_box.activated.connect(self.set_output_format)

    def set_input_path(self):
        input_file_path = QFileDialog.getOpenFileName(self, "Choose an input file")[0]
        self.input_path.setText(input_file_path)

    def set_output_path(self):
        output_directory_path = QFileDialog.getExistingDirectory(self, "Choose an output directory")
        self.output_path.setText(output_directory_path)

    def open_settings_window(self):
        # TODO: Settings window with testing mode check box and default paths
        print("Opening settings window.")

    def set_make_mono(self):
        self.make_mono_state = self.make_mono_box.isChecked()

    def set_output_format(self):
        self.output_format = self.output_format_box.currentText()

    def set_bitrate(self):
        self.bitrate = self.bitrate_box.currentText()

    def start_ffmpeg_convert(self):
        input_path = self.input_path.text()
        output_dir_path = self.output_path.text()
        make_mono = self.make_mono_state
        output_format = self.output_format
        bitrate = self.bitrate
        new_output_filename = self.new_filename.text()
        custom_output_format = os.path.splitext(new_output_filename)[1]

        if not new_output_filename:
            input_file_name = os.path.split(input_path)[1]
            input_file_ext = os.path.splitext(input_path)[1]
            input_file_name = input_file_name.strip(input_file_ext)
            output_path = os.path.join(output_dir_path, f"{input_file_name}.{output_format.lower()}")
        elif custom_output_format and custom_output_format != ".":
            output_path = os.path.join(output_dir_path, f"{new_output_filename}")
        else:
            output_path = os.path.join(output_dir_path, f"{new_output_filename}.{output_format.lower()}")

        convert.convert_file(input_path, output_path, make_mono, bitrate, testing_mode=False)

    def close_program(self):
        self.close()


# noinspection PyArgumentList
class Window(QWidget):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
