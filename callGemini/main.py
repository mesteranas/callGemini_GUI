import sys
from custome_errors import *
sys.excepthook = my_excepthook
import time
import update
import gui
import guiTools
from settings import *
import speech_recognition as sr
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
import google.generativeai as genai
import winsound
import gtts
import langdetect
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
genai.configure(api_key="")
TextModel=genai.GenerativeModel('gemini-pro')
class Thread(qt2.QThread):
    def __init__(self,player):
        super().__init__()
        self.player=player
        self.player.mediaStatusChanged.connect(self.on_state)
        self.is_playing=False
    def on_state(self,state):
        if state==QMediaPlayer.MediaStatus.EndOfMedia:
            self.is_playing=False

    def run(self):
        SR=sr.Recognizer()
        chat=TextModel.start_chat()
        while True:
            self.player.stop()
            time.sleep(1)
            self.player.setSource(qt2.QUrl.fromLocalFile(None))
            with sr.Microphone() as src:
                winsound.PlaySound("data/sounds/1.wav",1)
                audio=SR.listen(src)
            try:
                winsound.PlaySound("data/sounds/2.wav",1)
                text=SR.recognize_google(audio,language=settings_handler.get("g","speekLanguage"))
            except:
                text="sorry"
            winsound.PlaySound("data/sounds/3.wav",1)
            try:
                res=chat.send_message(text).text
            except:
                res="error"
            try:
                Language=langdetect.detect(res)
            except:
                Language="en"
            tts=gtts.gTTS(res,lang=Language)
            tts.save("data/speek.mp3")
            winsound.PlaySound("data/sounds/4.wav",1)
            self.player.setSource(qt2.QUrl.fromLocalFile("data/speek.mp3"))
            self.is_playing=True
            self.player.play()
            time.sleep(self.player.duration()/1000)


class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.player=QMediaPlayer()
        self.audio=QAudioOutput()
        self.player.setAudioOutput(self.audio)

        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        self.thread=Thread(self.player)
        self.thread.start()
        layout=qt.QVBoxLayout()
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        self.thread.terminate()
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()

App=qt.QApplication(sys.argv)
w=main()
w.show()
App.setStyle('fusion')
App.exec()