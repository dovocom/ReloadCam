#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 3

#Filename must start with Server, classname and argument must be the same!
class Xhaka(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://myfree.cccam.bz/
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfN_e0uHGyV-VlpekrnvU35vdxttglZaXpK574s3c")
        return realUrl

    def GetClines(self):
        print "Now getting Xhaka clines!"
        xhakaClines = []
        xhakaClines.append(self.__GetXhakaCline())
        xhakaClines = filter(None, xhakaClines)
        if len(xhakaClines) == 0: print "No Xhaka lines retrieved"
        return xhakaClines

    def __GetXhakaCline(self):

        values= {
            'Username': ReloadCam_Helper.GetRandomString(5),
            'Password': ReloadCam_Helper.GetRandomString(5),
            'cline':'Order+New+CCCam'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
