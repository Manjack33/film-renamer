import cv2
file_path = "Watchmen - Strážci.avi"  # change to your own video path
vid = cv2.VideoCapture(file_path)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
bitrate = vid.get(cv2.CAP_PROP_BITRATE)


print(f'{int(width)}x{int(height)} - {bitrate}')
