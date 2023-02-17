import os
import stat
import glob
import pathlib
import subprocess
import gi
from .imageOptions import *
from ..creator import error
gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk, Pango, Gdk

class getImages(list):
    def __init__(self, list, loc): 

        i = 0
        self.appimages = 0
        self.executable = []
        self.names = []

        for x in list:
            file = pathlib.Path(list[i-1])
            i += 1
            self.file_extension = file.suffix
            if(self.file_extension == ".AppImage"):
                self.appimages += 1
                name = str(loc) + '/' + str(file).encode('utf-8').decode()
                self.names.append(name)
                names.append(self.names)

    def createElements(appImage, refresh, mainWindow):
            
            imageName = os.path.splitext(appImage)[0]

            fullName = os.path.basename(imageName)
            baseName = fullName.replace("-x86_64", "")

            st = os.stat(appImage)
            executable = bool(st.st_mode & stat.S_IEXEC)

            rightBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            rightBox.append(createElementButton('media-playback-start-symbolic','success',manageImages.startImage, appImage, refresh, baseName, mainWindow))
            rightBox.append(createElementButton('org.gnome.Settings-symbolic',None, manageImages.imageOptions, appImage, refresh, baseName, mainWindow))
            rightBox.append(createElementButton('user-trash-symbolic','error',manageImages.deleteImage, appImage, refresh, baseName, mainWindow))

            leftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            leftBox.set_hexpand(True)
            leftBox.append(createElementLabel("Name:  ", fullName + ".AppImage"))
            leftBox.append(createElementLabel("Path:  ", appImage))

            expandableLayout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            expandableLayout.append(leftBox)
            expandableLayout.append(rightBox)

            box = Adw.PreferencesGroup.new()

            adw_expander_row = Adw.ExpanderRow.new()
            adw_expander_row.set_title(title=baseName)
            adw_expander_row.add_row(child=expandableLayout)

            if not executable:
                adw_expander_row.get_style_context().add_class(class_name='error')
                adw_expander_row.set_subtitle(subtitle='AppImage file not executable')


            box.add(adw_expander_row)

            return box

    def restart_count():
        global desktopCount
        global nameNum
        desktopCount = 0
        nameNum = 0

def createElementButton(iconName, style, action, actionArg1, refresh, name, mainWindow):

            b = Gtk.Button()
            b.set_size_request(30,30)
            b.set_halign(Gtk.Align.END)
            b.set_valign(Gtk.Align.CENTER)
            b.set_icon_name(icon_name=iconName)
            if style is not None:
                b.get_style_context().add_class(class_name=style)
            b.set_margin_start(3)
            b.set_margin_top(12)
            b.set_margin_end(6)
            b.set_margin_bottom(12)
            b.connect('clicked', action, actionArg1, refresh, name, mainWindow)

            return b

def createElementLabel(text, name):

            l = Gtk.Label()
            l.set_margin_start(12)
            l.set_margin_top(6)
            l.set_margin_end(12)
            l.set_margin_bottom(12)
            l.set_text(text + name)
            l.set_halign(Gtk.Align.START)

            return l

desktopCount=0
names = []
nameNum = 0

def getFileNum(list, loc):
    return getImages(list, loc)

def executeImage(executable, imagePath):
        if not executable:
            error.throwError(None, "The app has no executable permissions", "Permission denied")
        else:
            subprocess.run(imagePath)