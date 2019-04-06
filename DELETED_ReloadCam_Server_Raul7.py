#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 6

BestEuroCccamUsername = 'username'
BestEuroCccamPort = 170099

#Filename must start with Server, classname and argument must be the same!
class Raul7(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpLZ7fKHJ29LUkpihopuvpnvV1NmexdOUp6CZsbV81pSdssq9oYmpgIq6v-GS2MezrHJ0o3qGcrfZqaDHxqV0n4GcpLSDx7m_t5SlgmGYmKy1")
        return realUrl

    def GetClines(self):
        print "Now getting Raul7 clines!"
        raul7Clines = filter(None, self.__GetRaul7Cline())
        if len(raul7Clines) == 0: print "No Raul7 lines retrieved"
        return raul7Clines

    def GetBestEuroCccamCline(self, cline):
        import re

        regExpr = re.compile('[C]:\s*\S+\s+\S*\s+\S+\s+([\w.\-]+)')
        match = regExpr.search(cline)

        if match is None:
            return cline;

        password = match.group(1)
        return 'C: user.besteurocccam.com ' + str(BestEuroCccamPort) + ' ' + BestEuroCccamUsername + ' ' + password
        
    def __GetRaul7Cline(self):
        import re

        clines = []
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())

        regExpr = re.compile('([C]:\s*\S+\s+\S+\s+\S+\s+[\w.\-]+)')
        matches = regExpr.findall(htmlCode)
        
        for match in matches:
            if re.match('[C]:\s*user.besteurocccam.com\s*', match):
                match = self.GetBestEuroCccamCline(match)    
            if (ReloadCam_Helper.TestCline(match)):
                clines.append(match)
        
        return clines;
