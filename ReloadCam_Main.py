#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Arguments, ReloadCam_Helper

def GetVersion():
    return 4

class Server(object):
    def GetUrl():
        pass
    def GetClines(self):
        pass

def WriteCccamFile(clines, append, check, path):
    """Crea el archivo CCCam.cfg"""
    import os, os.path

    existingClines = []
    clinesToWrite = []

    if append and os.path.exists(path):
        with open(path) as f:
            existingClines = f.readlines()

    for cline in existingClines:
        if check == False or (check == True and TestCline(cline) == True):
            clinesToWrite.append(cline)

    clinesToWrite += clines
    clinesToWrite = filter(None, clinesToWrite)
    clinesToWrite = list(set(clinesToWrite)) #Remove duplicated lines
    clinesToWrite = ReloadCam_Helper.SortClinesByPing(clinesToWrite)

    file = open(path, 'w')
    for cline in clinesToWrite:
        file.write(cline + '\n')
    file.close()

def GetClinesByArgument(arguments, customClines):
    """Lee los arguments y carga las clines pertinentes"""
    import importlib

    clines = []
    clines += customClines #Primero agregamos las clines custom

    if arguments is None:
        print "No parameters supplied!"
        return clines

    if len(arguments) > 1 and ('ALL' in arguments or 'ALLT' in arguments):
        print "Cannot use parameter ALL/ALLT with other parameters"
        return clines
    else:
        if 'ALL' in arguments:
            arguments = ReloadCam_Arguments.Arguments
            arguments.remove('ALL')
            arguments.remove('ALLT')
            arguments.remove('Testious')
        if 'ALLT' in arguments:
            arguments = ReloadCam_Arguments.Arguments
            arguments.remove('ALL')
            arguments.remove('ALLT')

    if len(arguments) == 0:
        print "No parameters available!"
        return clines

    for argument in arguments:
        moduleName = 'ReloadCam_Server_' + argument #creamos el nombre del modulo que tenemos que importar ej:ReloadCam_Myccam
        try:
            my_module = importlib.import_module(moduleName) #Esta linea importa el modulo como si hicieramos un import <nombremodulo>
            classInstance = getattr(my_module, argument)() #Creamos una instancia de ese modulo importado
            clines += classInstance.GetClines() #Este metodo lo deben implementar todas las clases derivadas de "Server"
        except Exception,e:
            print "Error loading module: " + moduleName
    return clines

def RestartCccam(path):
    """Resetea el proceso de CCCam para que las nuevas clines se carguen"""
    import time, os

    if os.path.exists(path):
        os.system('killall ' + os.path.basename(path))
        time.sleep(0.5)
        os.system('rm -rf /tmp/*.info* /tmp/*.tmp*')
        os.system(path + ' &')
    else:
        print "ERROR! Cannot restart cccam! Restart manually or fix variable path cccamBin! Current value: " + path

def Main(customClines, cccamPath, cccamBin):
    import sys, os, optparse, ReloadCam_Arguments
    clines = []

    parser = optparse.OptionParser(description="Refrescador automatico de clines. Creado por Dagger")

    possibleArguments = '%s' % ','.join(map(str, ReloadCam_Arguments.Arguments))

    parser.add_option('-s', '--server', dest='web', action='append', choices=ReloadCam_Arguments.Arguments,
        help='Especifica la web de la que quieres descargar las clines. Puedes repetir este parametro varias veces. \
        Valores posibles: ' + possibleArguments)
    
    parser.add_option('-a', '--append', dest='append', default=False, action='store_true',
        help='Mete las nuevas lineas al final sin sobreescribir el CCcam.cfg')

    parser.add_option('-c', '--check', dest='check', default=False, action='store_true', 
        help='Checkea las lineas antiguas del CCcam.cfg y las borra si no funcionan')

    parser.add_option('-r', '--norestart', dest='norestart', default=False, action='store_true', 
        help='NO reinicia la cccam despues del refresco de clines')

    (opts, args) = parser.parse_args()

    if opts.check and not opts.append:
        print "Option check requires option append\n"
        parser.print_help()
        exit(-1)

    clines = GetClinesByArgument(opts.web, customClines)

    if len(clines) > 0:
        print "Writing to the cccam.cfg!"
        WriteCccamFile(clines, opts.append, opts.check, cccamPath)
        if opts.norestart is False:
            print "Restarting cam!"
            #RestartCccam(cccamBin)
        print "Finished!!!"
    else :
        print "ERROR!!!! NO CCCAMS LOADED!"
    return;

def CleanFiles(currentPath, platform):
    import os

    if  platform.lower() == "windows":
        os.system('del /q "' + currentPath + '*.pyc"')
        os.system('del /q "' + currentPath + '*.pyo"')
    else:
        os.system("rm -rf " + currentPath + "*.pyo")
        os.system("rm -rf " + currentPath + "*.pyc")

#endregion
