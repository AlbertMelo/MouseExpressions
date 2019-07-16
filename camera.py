import cv2 as cv

class Camera(object):

    
    def __init__(self):
        #Camera padrao do computador
        try:
            self.cap = cv.VideoCapture(0)
        except:
            print ('Nao foi possivel iniciar camera Verifique se a camera esta conectada no computador')
            exit

    def pararCaptura(self):
        self.cap.release()

    def lerImagem(self):
        return self.cap.read()