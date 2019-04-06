#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 3

#Filename must start with Server, classname and argument must be the same!
class Kacsat(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://kac-sat.noip.me/index.php
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfN3Gz5zUxaVgoaOssXvfypvYz8iWqmGkq7E=")
        return realUrl

    def GetClines(self):
        print "Now getting Kacsat clines!"
        kacsatClines = []
        kacsatClines.append(self.__GetKacsatCline())
        kacsatClines = filter(None, kacsatClines)
        if len(kacsatClines) == 0: print "No Kacsat lines retrieved"
        return kacsatClines

    def __GetKacsatCline(self):

        values= {
            'user': ReloadCam_Helper.GetMyIP(),
            'pass': 'hack-sat.net',
            'submit':'Active+User%21'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
