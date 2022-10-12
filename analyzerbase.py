from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, \
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QGridLayout, \
    QCheckBox, QComboBox, QGroupBox, QDateTimeEdit, QAction, QFileDialog, \
    QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
import json
from wookutil import WookLog, WookUtil, WookMath
from wookdata import *

class AnalyzerBase(QMainWindow, WookLog, WookUtil, WookMath):
    def __init__(self, log):
        super().__init__()
        WookLog.custom_init(self, log)
        WookUtil.__init__(self)
        WookMath.__init__(self)
        with open('setting.json') as r_file:
            self.setting = json.load(r_file)
        self.initUI()

    def initUI(self):
        # Test Button
        self.btn_test = QPushButton('Test')
        self.btn_test.clicked.connect(self.test)

        ##### Account information
        self.cb_auto_login = QCheckBox('Auto')
        self.cb_auto_login.setChecked(True)
        self.btn_login = QPushButton('Login', self)
        self.btn_login.clicked.connect(self.connect_kiwoom)
        lb_account = QLabel('Account')
        self.cbb_account = QComboBox()
        self.cbb_account.currentTextChanged.connect(self.on_select_account)

        account_grid = QGridLayout()
        account_grid.addWidget(self.cb_auto_login, 0, 0)
        account_grid.addWidget(self.btn_login, 0, 1)
        account_grid.addWidget(lb_account, 1, 0)
        account_grid.addWidget(self.cbb_account, 1, 1, 1, 2)
        account_grid.setColumnMinimumWidth(2, 10)

        account_gbox = QGroupBox('Account Information')
        account_gbox.setLayout(account_grid)

        ##### Item infomation
        lb_item_code = QLabel('Code')
        lb_item_name = QLabel('Name')
        self.cbb_item_code = QComboBox()
        self.cbb_item_name = QComboBox()
        self.cbb_item_code.setEditable(True)
        self.cbb_item_name.setEditable(True)
        self.cbb_item_code.editTextChanged.connect(self.on_select_item_code)
        self.cbb_item_name.currentIndexChanged.connect(self.on_select_item_name)
        self.cbb_item_code.addItems(CODES)
        self.cbb_item_name.addItems(CODES.values())

        # Period
        current_date = QDateTime.currentDateTime()
        lb_period = QLabel('Period')
        self.dte_first_day = QDateTimeEdit()
        self.dte_first_day.setCalendarPopup(True)
        self.dte_first_day.setDisplayFormat('yyyy-MM-dd')
        self.dte_first_day.setDateTime(current_date)
        lb_wave = QLabel('~')
        self.le_last_day = QLineEdit()
        self.dte_last_day = QDateTimeEdit()
        self.dte_last_day.setCalendarPopup(True)
        self.dte_last_day.setDisplayFormat('yyyy-MM-dd')
        self.dte_last_day.setDateTime(current_date)
        self.cb_one_day = QCheckBox('1-day')
        self.cb_one_day.setChecked(self.setting['one_day'])
        self.cb_all_days = QCheckBox('All')
        self.cb_all_days.setChecked(True)
        self.dte_first_day.dateChanged.connect(self.on_change_first_day)
        self.dte_last_day.dateChanged.connect(self.on_change_last_day)

        # Save Folder
        lb_save_folder = QLabel('Save')
        self.le_save_folder = QLineEdit()
        self.le_save_folder.setText(self.setting['save_folder'])
        self.le_save_folder.editingFinished.connect(self.on_edit_save_folder)
        self.btn_change_save_folder = QPushButton('Change')
        self.btn_change_save_folder.clicked.connect(self.on_change_save_folder)

        # Item grid layout
        item_grid = QGridLayout()
        item_grid.addWidget(lb_item_code, 0, 0)
        item_grid.addWidget(self.cbb_item_code, 0, 1)
        item_grid.addWidget(lb_item_name, 0, 2, 1, 2)
        item_grid.addWidget(self.cbb_item_name, 0, 4, 1, 3)
        item_grid.addWidget(lb_period, 1, 0)
        item_grid.addWidget(self.dte_first_day, 1, 1, 1, 2)
        item_grid.addWidget(lb_wave, 1, 3, Qt.AlignCenter)
        item_grid.addWidget(self.dte_last_day, 1, 4, 1, 1)
        item_grid.addWidget(self.cb_one_day, 1, 5)
        item_grid.addWidget(self.cb_all_days, 1, 6)
        item_grid.addWidget(lb_save_folder, 2, 0)
        item_grid.addWidget(self.le_save_folder, 2, 1, 1, 4)
        item_grid.addWidget(self.btn_change_save_folder, 2, 5, 1, 2)
        item_gbox = QGroupBox('Item information')
        item_gbox.setLayout(item_grid)

        ##### Data type
        self.rb_tick = QRadioButton('Tick')
        self.rb_min = QRadioButton('Min')
        self.rb_day = QRadioButton('Day')
        self.cbb_tick = QComboBox()
        self.cbb_min = QComboBox()
        self.cbb_day = QComboBox()
        self.rb_min.setChecked(True)
        self.cbb_tick.addItems(TICK)
        self.cbb_min.addItems(MIN)
        self.cbb_day.addItem(DAY_DATA)
        self.cbb_day.addItem(WEEK_DATA)
        self.cbb_day.addItem(MONTH_DATA)
        self.cbb_day.addItem(YEAR_DATA)
        self.cbb_tick.activated.connect(self.on_change_tick)
        self.cbb_min.activated.connect(self.on_change_min)
        self.cbb_day.activated.connect(self.on_change_day)

        data_type_grid = QGridLayout()
        data_type_grid.addWidget(self.rb_tick, 0, 0)
        data_type_grid.addWidget(self.cbb_tick, 0, 1)
        data_type_grid.addWidget(self.rb_min, 1, 0)
        data_type_grid.addWidget(self.cbb_min, 1, 1)
        data_type_grid.addWidget(self.rb_day, 2, 0)
        data_type_grid.addWidget(self.cbb_day, 2, 1)
        data_type_gbox = QGroupBox('Data Type')
        data_type_gbox.setLayout(data_type_grid)

        ##### Go button
        self.btn_go = QPushButton('&Go')
        self.btn_go.clicked.connect(self.get_stock_price)
        # self.btn_go.setMaximumHeight(100)
        self.btn_go.setMinimumSize(80, 100)
        go_grid = QGridLayout()
        go_grid.addWidget(self.btn_go, 0, 0, 3, 1)

        ##### Analysis
        lb_analysis_folder = QLabel('Target')
        self.le_analysis_folder = QLineEdit()
        self.le_analysis_folder.setText(self.setting['analysis_folder'])
        self.btn_change_analysis_folder = QPushButton('Change')
        self.btn_change_analysis_folder.clicked.connect(self.on_change_analysis_folder)
        self.le_interval = QLineEdit()
        lb_interval = QLabel('Interval')
        self.le_interval.setMaximumWidth(30)
        self.le_interval.setText('50')
        lb_loss_cut = QLabel('Loss cut')
        self.le_loss_cut = QLineEdit()
        self.le_loss_cut.setMaximumWidth(30)
        self.le_loss_cut.setText('30')
        lb_fee = QLabel('Fee(%)')
        self.le_fee = QLineEdit()
        self.le_fee.setMaximumWidth(40)
        self.le_fee.setText('0.03')

        analysis_grid = QGridLayout()
        analysis_grid.addWidget(lb_analysis_folder, 0, 0)
        analysis_grid.addWidget(self.le_analysis_folder, 0, 1, 1, 5)
        analysis_grid.addWidget(self.btn_change_analysis_folder, 0, 6)
        analysis_grid.addWidget(lb_interval, 2, 0)
        analysis_grid.addWidget(self.le_interval, 2, 1)
        analysis_grid.addWidget(lb_loss_cut, 2, 2)
        analysis_grid.addWidget(self.le_loss_cut, 2, 3)
        analysis_grid.addWidget(lb_fee, 2, 4)
        analysis_grid.addWidget(self.le_fee, 2, 5)
        analysis_gbox = QGroupBox('Analysis')
        analysis_gbox.setLayout(analysis_grid)

        ##### Chart
        self.lb_analysis_item = QLabel('No item')
        self.lb_analysis_item.setStyleSheet('color:DarkGreen')
        self.lb_analysis_item.setMaximumWidth(110)
        self.lb_analysis_first_day = QLabel(self.dte_first_day.text())
        self.lb_analysis_first_day.setStyleSheet('color:Indigo')
        lb_chart_wave = QLabel('~')
        self.lb_analysis_last_day = QLabel(self.dte_last_day.text())
        self.lb_analysis_last_day.setStyleSheet('color:Indigo')
        self.rb_save_chart = QRadioButton('Save')
        self.rb_save_chart.clicked.connect(self.on_select_save_chart)
        self.rb_show_chart = QRadioButton('Show')
        self.rb_show_chart.clicked.connect(self.on_select_show_chart)
        self.rb_show_chart.setChecked(True)
        self.btn_candle_chart = QPushButton('Candle')
        self.btn_candle_chart.clicked.connect(self.save_as_candle_chart)
        self.btn_candle_chart.setEnabled(False)
        self.btn_simplified_chart = QPushButton('Simplified')
        self.btn_simplified_chart.clicked.connect(self.show_simplified_chart)
        self.btn_simplified_chart.setEnabled(False)

        chart_hbox = QHBoxLayout()
        chart_hbox.addWidget(self.lb_analysis_first_day)
        chart_hbox.addWidget(lb_chart_wave)
        chart_hbox.addWidget(self.lb_analysis_last_day)
        chart_hbox.addStretch()

        chart_grid = QGridLayout()
        chart_grid.addWidget(self.lb_analysis_item, 0, 0, 1, 2)
        chart_grid.addLayout(chart_hbox, 0, 2, 1, 2)
        chart_grid.addWidget(self.rb_show_chart, 1, 0)
        chart_grid.addWidget(self.rb_save_chart, 1, 1)
        chart_grid.addWidget(self.btn_candle_chart, 1, 2)
        chart_grid.addWidget(self.btn_simplified_chart, 1, 3)
        chart_gbox = QGroupBox('Chart')
        chart_gbox.setLayout(chart_grid)

        ##### Analyze Button
        self.btn_analyze = QPushButton('Analyze')
        self.btn_analyze.setMinimumSize(110, 75)
        self.btn_analyze.clicked.connect(self.analyze)
        analysis_btn_grid = QGridLayout()
        analysis_btn_grid.addWidget(self.btn_analyze, 0, 0)

        ##### Analysis Report
        report_header = ['Item', 'Time', 'Earning', 'Loss', 'Profit', 'Rate']
        report_header += ['Fee', 'Net Profit', 'Net Rate']
        self.table_report = QTableWidget(0, 9)
        self.table_report.cellClicked.connect(self.on_select_table_report)
        self.table_report.setHorizontalHeaderLabels(report_header)
        for column in range(1, self.table_report.columnCount()):
            self.table_report.setColumnWidth(column, 70)
        self.table_report.setColumnWidth(0, 145)
        self.table_report.setColumnWidth(1, 75)
        self.table_report.setColumnWidth(2, 50)
        self.table_report.setColumnWidth(3, 50)

        report_gbox = QGroupBox('Analysis Report')
        report_gbox.setMinimumHeight(400)
        report_grid = QGridLayout()
        report_grid.addWidget(self.table_report)
        report_gbox.setLayout(report_grid)

        # TextEdit
        self.te_info = QTextEdit()

        # Central Layout
        top_hbox = QHBoxLayout()
        top_hbox.addWidget(account_gbox)
        top_hbox.addWidget(item_gbox)
        top_hbox.addWidget(data_type_gbox)
        top_hbox.addLayout(go_grid)
        top_hbox.addStretch()

        middle_hbox = QHBoxLayout()
        middle_hbox.addWidget(analysis_gbox)
        middle_hbox.addWidget(chart_gbox)
        middle_hbox.addLayout(analysis_btn_grid)
        middle_hbox.addStretch()

        vbox = QVBoxLayout()
        vbox.addLayout(top_hbox)
        vbox.addLayout(middle_hbox)
        vbox.addWidget(report_gbox)
        vbox.addWidget(self.te_info)
        vbox.addWidget(self.btn_test)

        # Central widget
        cw = QWidget()
        cw.setLayout(vbox)

        # Menu bar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet('background:rgb(140,230,255)')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)

        setting_action = QAction('Setting', self)
        setting_action.triggered.connect(self.edit_setting)
        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(setting_action)

        # Window setting
        self.setCentralWidget(cw)
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('ready')
        self.setWindowTitle('wook\'s algorithm analyzer')
        self.resize(700, 800)
        self.move(100, 100)
        self.setWindowIcon(QIcon('nyang1.ico'))
        self.show()