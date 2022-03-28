import os
import urllib.request
from abc import ABC
from html.parser import HTMLParser
from bs4 import BeautifulSoup


class Show:
    # @staticmethod
    # def get_episodes_from_web(name):
    #     li = []
    #
    #     with urllib.request.urlopen('https://www.serialzone.cz/serial/' + name + '/epizody/') as response:
    #         html = response.read().decode("utf-8")
    #         season_list = html[int(html.find('season-head')):int(html.find('mto20'))]
    #         season_counter = 1
    #
    #         while season_list:
    #             season_part = str(season_counter) + '\n' + season_list[0:int(season_list[2:].find('season-head')):]
    #             season_list = season_list[len(season_part):]
    #             season_counter += 1
    #             counter = 1
    #
    #             while season_part.find('sunr') != -1:
    #                 start = season_part.find('sunr')
    #                 end = season_part.find('</h2>')
    #                 ep = season_part[start:end]
    #                 season_part = season_part[end + 1:]
    #                 counter += 1
    #                 episode_name = ep[6:8] + 'x' + ep[15:17] + ' - ' + ep[25:-1 + ep.find('<span')]
    #                 li.append(episode_name)
    #     return li

    """Returns list of the episodes of the TV Show formated as '01x01 - Episode name'"""

    @staticmethod
    def get_episodes_from_web(name):
        with urllib.request.urlopen('https://www.serialzone.cz/serial/' + name + '/epizody/') as html:
            parsed_html = BeautifulSoup(html, features="lxml")
            episodes = parsed_html.body.find_all('', attrs={'class': 'suname'})
            return [f'{episode.text[:5]} - {episode.text[6:episode.text.find("(") - 1]}' for episode in episodes]

    """Returns file list of all file form folder and their subfolders, except thumb and .srt files"""

    @staticmethod
    def get_file_list_from_folder_and_subfolders(start_path) -> list:
        episodes = []
        for path, dirs, files in os.walk(start_path):
            for filename in files:
                if ("Thumb" not in filename) and (".srt" not in filename) and ("Potitulk" not in filename):
                    episodes.append(os.path.join(path, filename))
        return episodes

    """Vrati seznam slozek v adresari"""

    @staticmethod
    def get_subfolders_list(start_path):
        return next(os.walk(start_path))[1]

    """Přejmenuje díly seriálu"""

    def rename_episodes(self, path):
        name = path[path.rfind('\\') + 1:].translate(str.maketrans("ěščřžýáíéúůňťĚŠČŘŽÝÁÍÉÚŮŇŤ ", "escrzyaieuuntESCRZYAIEUUNT-"))
        files = self.get_file_list_from_folder_and_subfolders(path)
        episode_names = self.get_episodes_from_web(name)

        counter = 0
        updated_files = []
        for file in files:
            updated_files.append(file[0:file.rfind('\\') + 1] + episode_names[counter] + file[file.rfind('.'):])
            print(file + '  -->  ' + updated_files[counter])
            counter += 1
        # self.renameList(path_li, li)

    # Prejmenuje danou serii
    @staticmethod
    def rename_serie_episodes(path):
        print(path)  # "Y:\\Cizí\\Dexter\\Serie 01"

        # serie = path[path.rfind('\\') + 1:]
        # serie = serie[serie.len] if serie[len(serie) - 1] == '0' else serie = serie[len(serie) - 1:]
        # print(serie)
        midName = path[:path.rfind('\\')]

        name = midName[midName.rfind('\\') + 1:]
        name = name.translate(str.maketrans("ěščřžýáíéúůňťĚŠČŘŽÝÁÍÉÚŮŇŤ ", "escrzyaieuuntESCRZYAIEUUNT-"))

        url = f'https://www.serialzone.cz/serial/{name}/epizody/'
        with urllib.request.urlopen(url) as response:
            html = response.read().decode("utf-8")
            movieList = html[int(html.find('season-head')):int(html.find('mto20'))]

        return movieList

    # Přejmenuje složky sérií
    def renameTheSerieFolder(self, path):
        series = self.get_subfolders_list(path)
        curList = []
        newList = []
        counter = 0
        for serie in series:
            if "S0" in serie.upper():
                start_pos = serie.upper().find("S0")
                curList.append(os.path.join(path, serie))
                newList.append(os.path.join(path, 'Serie 0' + str(serie[start_pos + 2:start_pos + 3])))
                print(curList[counter] + '  -->  ' + newList[counter])
                counter += 1

        self.renameList(curList, newList)
        return

    # Zahájí přejmenování složek a souborů
    def renameList(self, current, updated):
        if input('Přejmenovat dle výše uvedeného? [y/n]:') == ('y' or 'Y'):
            counter = 0

            for cur in current:
                os.rename(cur, updated[counter])
                print('Hotovo')

                counter += 1
        return


f = Show()
f.rename_episodes('Y:\Cizí\Humans\Serie 2')
