from abc import ABC
from html.parser import HTMLParser

import shows


class MyHTMLParser(HTMLParser, ABC):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        return

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        return

    def handle_data(self, data):
        print(data)


class Menu:
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

    # Vypise moznosti Hlavniho menu
    def main_menu(self):
        print('1 - Filmy\n2 - Serialy')
        self.SwitchValuation('Main', input('Vyber moznost: '))
        return

    # Zavola danou moznost
    def SwitchValuation(self, type, option):
        method_name = type + str(option)
        method = getattr(self, method_name, lambda: self.main_menu())
        return method()

    # Vypise moznosti Filmoveho menu
    def Main1(self):
        print('1 - seznam filmu\n2 - prejmenovat film\n3 - prejmenovat vice filmu')
        self.SwitchValuation('Movie', input('Vyber moznost: '))
        return

    # Vypise moznosti Serialoveho menu
    def Main2(self):
        print(
            '1 - seznam serialu\n2 - seznam serialu vcetne dilu\n3 - prejmenovat dily serialu\n4 - prejmenovat serii serialu\n5 - prejmenovat Serie')
        self.SwitchValuation('Show', input('Vyber moznost: '))
        return

    def Movie1(self):
        print('Seznam neni')
        return

    def Show1(self):
        print('Seznam neni')
        return

    def Show3(self):
        s = shows.Show()
        path = input('Zadejte adresu k serialu ve formatu: "Y:\\Cizí\\Dexter": ')
        s.rename_episodes(path)
        return

    def Show4(self):
        s = shows.Show()
        path = input('Zadejte adresu k serii serialu ve formatu: "Y:\\Cizí\\Dexter\\Serie 01": ')

        parser = MyHTMLParser()
        parser.feed(s.rename_serie_episodes(path))
        return

    def Show5(self):
        s = shows.Show()
        path = input('Zadejte adresu k serialu ve formatu: "Y:\\Cizí\\Dexter": ')
        s.renameTheSerieFolder(path)
        return


f = Menu()
f.main_menu()
