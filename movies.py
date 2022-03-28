import os
import urllib.request

import ffmpeg

DIR_OF_FILMS = 'Z:\Filmy\Cizí\Sci-fi'


class MovieList:
    def __init__(self, **kwargs):
        super(MovieList, self).__init__(**kwargs)

    @staticmethod
    def get_filelist(start_path):
        full_name_list = []
        for path, dirs, files in os.walk(start_path):
            for filename in files:
                if ("Thumb" not in filename) and (".srt" not in filename) and ("Potitulk" not in filename):
                    full_name_list.append(os.path.join(path, filename))

        return full_name_list

    @staticmethod
    def get_filename(filepath):
        filename = os.path.basename(filepath)

        if ' - ' in filename[0:6]:
            filename = filename[filename.find(' - ') + 3:]
        filename = filename.replace('.avi', '')
        filename = filename.replace('.mkv', '')
        filename = filename.replace('.mp4', '')
        filename = filename.replace('.ts', '')
        return filename

    @staticmethod
    def print_list(li):
        for film in li:
            print(film)

    def print_verbose_film_list(self, dir_path, is_full=False):
        info_list = []

        for film in self.get_filelist(dir_path):
            info_list.append("{0} - {1}x{2}, {3}, {4}"
                             .format(film if is_full else self.get_filename(film), *self.get_mediainfo(film)))

        self.print_list(info_list)

    def print_low_res_films(self, dir_path, is_full=False):
        info_list = []

        for film in self.get_filelist(dir_path):
            print(self.get_mediainfo(film)[0])
            if self.get_mediainfo(film)[0] != '1920':
                info_list.append(film if is_full else self.get_filename(film) + ' - ' + str(self.get_mediainfo(film)).replace('[', '').replace(']', ''))

        self.print_list(info_list)

    @staticmethod
    def write_list(li, path, filename):
        file = open(os.path.join(path, filename), "w", encoding='utf-8')
        for i in li:
            file.write(i + '\n')
        file.close()

    def print_dictionary(self, d, indent=0):
        for key, value in d.items():
            line = '\t' * indent + str(key) + ': '
            if isinstance(value, dict):
                print(line)
                self.print_dictionary(value, indent + 1)
            else:
                line += '\t' * (indent + 1) + str(value)
                print(line)

    def mediainfo(self, file_path):
        probe = ffmpeg.probe(file_path)
        for stream in probe["streams"]:
            # print(stream)
            self.print_dictionary(stream)
            print('\n')

    def get_mediainfo(self, file_path):
        probe = ffmpeg.probe(file_path)
        video_streams = [stream for stream in probe["streams"]]
        result = []

        for stream in video_streams:
            if stream["codec_type"] == "video":
                width = self.retrieve_stream_info(stream, "width")
                height = self.retrieve_stream_info(stream, "height")
                codec = self.retrieve_stream_info(stream, 'codec_name')
                bitrate = f'{int(round(int(self.retrieve_stream_info(stream, "bit_rate")) / 1000))}kb/s'
                if bitrate == '0kb/s':
                    try:
                        bitrate = f'{int(round(int(stream["tags"]["BPS-eng"]) / 1000))}kb/s'
                    except Exception:
                        pass
                result.append(width)
                result.append(height)
                result.append(codec)
                result.append(bitrate)

            elif stream["codec_type"] == "audio":
                try:
                    language = f'{stream["tags"]["language"]}'
                except Exception:
                    try:
                        language = f'{stream["tags"]["Language"]}'
                    except Exception:
                        language = '?'
                result.append('Audio: ' + language)

            elif stream["codec_type"] == "subtitle":
                try:
                    language = f'{stream["tags"]["language"]}'
                except Exception:
                    try:
                        language = f'{stream["tags"]["Language"]}'
                    except Exception:
                        language = '?'
                result.append('Subtitle: ' + language)

        return result

    @staticmethod
    def retrieve_stream_info(stream, value):
        try:
            return stream[value]
        except Exception:
            return '0'


class MovieName:
    def getFixedName(self, filename):
        filename = filename.translate(str.maketrans("ěščřžýáíéúůňťĚŠČŘŽÝÁÍÉÚŮŇŤ", "escrzyaieuuntESCRZYAIEUUNT"))
        filename = filename.replace(' ', '%20')
        with urllib.request.urlopen('https://www.csfd.cz/hledat/?q=' + filename) as response:
            html = response.read().decode("utf-8")
            movieList = html[int(html.find('search-films')):]

            start = int(movieList.find("<h3"))
            end = int(movieList.find("</a></h3>"))
            ls = movieList[start:end]
            film = ls[ls.rfind('>') + 1:]
        print(filename + ' - ' + film)
        return film


class NameFixer:
    def fixNames(self, dir):
        fixedList = []
        movies = MovieList()

        movieList = movies.get_filelist(dir)
        movies.write_list(movieList, dir, 'testfile.txt')


#        for movie in movieList:
#           mov = MovieName()
#          fixedList.append(mov.getFixedName(movie))
#
#       movies.printList(fixedList, dir, 'fixed.txt')


# f = NameFixer()
# f.fixNames('Z:\\Filmy\\')

f = MovieList()
# print(f.get_mediainfo('Z:\Filmy\Cizí\Superhrdinové\Avengers\\01 - Iron-Man\I - Iron Man.mkv'))
f.print_low_res_films(DIR_OF_FILMS)
# f.print_verbose_film_list(DIR_OF_FILMS)
# f.mediainfo('Z:\Filmy\Cizí\Superhrdinové\Avengers\\01 - Iron-Man\I - Iron Man.mkv')
# print("{0}x{1}, {2}, {3}".format(*f.get_mediainfo('Z:\Filmy\Cizí\Superhrdinové\Avengers\\01 - Iron-Man\I - Iron Man.mkv')))
