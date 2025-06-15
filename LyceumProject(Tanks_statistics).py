import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import datetime

import json

app_id = "6c7e76f5e9c95e02c28d3179472da7b2"


def timestamp_to_a_date(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return str(dt_object).split()


def id_by_nickname(nick, type_of_game=None):
    """
        :param nick:
        :param type_of_game: True - TanksBlitz, False - MirTankov
    """

    if type_of_game is True:
        url = f"""https://papi.tanksblitz.ru/wotb/account/list/?application_id={app_id}&language=ru&type=startswith&search={nick}"""
        data_dict = (requests.get(url)).json()
        id_account = data_dict['data'][0]
        return id_account["account_id"]

    elif type_of_game is False:
        url = f"""https://api.tanki.su/wot/account/list/?application_id={app_id}&language=ru&type=startswith&search={nick}"""
        data_dict = (requests.get(url)).json()
        id_account = data_dict['data'][0]
        return id_account["account_id"]
    else:
        raise AttributeError('(type_of_game) None не поддерживается')


def getting_all_info_by_id_TB(id_account, main_info=False):
    """
        :param main_info: True - main info , False - all info
    """
    url = f"""https://papi.tanksblitz.ru/wotb/account/info/?application_id={app_id}&extra=statistics.rating&account_id={id_account}&fields=private.credits%2C+last_battle_time&language=ru"""
    data_dict = (requests.get(url)).json()
    if main_info is True:
        return data_dict


# noinspection PyArgumentList
class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.MT = None
        self.BlitzTree = None
        uic.loadUi("MainWindow.ui", self)
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("Cyberpunk(RUS BY LYAJKA)", 10))
        self.setFixedSize(1080, 720)
        self.TanksBlitz.setToolTip('Tanks Blitz')
        self.setStyleSheet(""" background-image: url(data/images/background_hell.png);""")

        self.MirTankov.clicked.connect(self.MTClick)

        self.TanksBlitz.clicked.connect(self.BlitzClick)
        self.SettingsButton.clicked.connect(self.open_settings)
        self.ExitButton.clicked.connect(sys.exit)

    def open_settings(self):
        pass

    def MTClick(self):
        self.hide()
        self.MT = MTTree()
        self.MT.show()

    def BlitzClick(self):
        self.hide()
        print(1)
        self.BlitzTree = TanksBlitzTree()
        print(2)
        self.BlitzTree.show()


class TanksBlitzTree(QMainWindow):

    # noinspection PyArgumentList
    def __init__(self):
        super().__init__()
        self.mainW = MainMenu()
        uic.loadUi("TanksBlitzWindow.ui", self)
        self.setWindowTitle("BlitzStatistic")
        self.initUI()
        self.full_info = {}
        self.nick = ""

    def initUI(self):
        self.setStyleSheet(""" background-image: url(data/images/background_hell.png);""")
        self.goBackButton.clicked.connect(self.go_back)
        self.SearchButton.clicked.connect(self.search)

    def go_back(self):
        self.close()
        self.mainW.show()

    def search(self):
        self.nick = self.InputNick.text()
        self.full_info = getting_all_info_by_id_TB(id_by_nickname(self.nick, type_of_game=True), main_info=True)
        print(self.full_info)


class MTTree(QMainWindow):
    # noinspection PyArgumentList
    def __init__(self):
        super().__init__()
        self.mainW = MainMenu()
        uic.loadUi("MTSearchWindow.ui", self)
        self.setWindowTitle("MTStatistic")
        self.initUI()

    def initUI(self):
        self.setStyleSheet(""" background-image: url(data/images/background_hell.png);""")
        self.goBackMT.clicked.connect(self.go_back_MT)
        # self.SearchButton.clicked.connect(self.search)

    def go_back_MT(self):
        self.close()
        self.mainW.show()

    def search(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())
    # g = id_by_nickname("EdgarBeckNewwer", type_of_game=False)
    # print(id_by_nickname("EdgarBeckNewwer", type_of_game=False))
    # print(g)
    # print(getting_all_info_by_id_TB(g, main_info=True))
