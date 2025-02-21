#Classes
from classes.login import user_login

#Utils
from utils.CompanyFormater import formatCompanyCode
from utils.csvReader import readCSV
from utils.xml_organizer import *

#Importando navegador
from config.browserConfig import Chorme

#Importanto função de autenticação
from auth.validateAcess import authorize_access

#INTERFACE GRÁFICA
from Interface.front import startInterface
from Interface.app_state import app_state

#Scripts todos os passos do DTE
from scripts.DTE.start import startProcess
from scripts.DTE.company_finder import companyFinder
from scripts.DTE.sigetWindow import enterSiget
from scripts.DTE.Break import passBreak
from scripts.DTE.searchCsv import downloadCsvAut,downloadCsvCancel

#Scripts todos os passos do Ambiente Seguro
from scripts.AmbienteSeguro.start import loginAmbienteSeguro
from scripts.AmbienteSeguro.enterFMeModule import enterMfeModule
from scripts.AmbienteSeguro.company_finder import company_finder_AmbSeg
from scripts.AmbienteSeguro.CfeQuery import cfeQuery

#Scripts para puxar todos os XML
from scripts.PullXML.LinkAPI import LinkXML
from scripts.PullXML.GetXML import getXML

import time
import os

from classes.CFElist import cfe_list

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

acessValidator = authorize_access() #True or False


try:
    
    startInterface()
    
    if app_state.next == True:   
        driver = Chorme()
        
        startProcess(driver)
        
        formatedCode = formatCompanyCode(app_state.inscricao_estadual)
        
        companyFinder(driver, formatedCode)
        
        enterSiget(driver)
        
        passBreak(driver)
        
        responseAut = downloadCsvAut(driver)
        if responseAut == True:
            readCSV(downloads_path, 'Autorizados')
            apagarCSV(downloads_path)
            
        responseCancel = downloadCsvCancel(driver)
        if responseCancel == True:
            readCSV(downloads_path, 'Cancelados')
            apagarCSV(downloads_path)
            
        print(cfe_list.totalList)
        print(len(cfe_list.totalList))
        
        
        #Credenciais ambiente seguro
        user = user_login.username
        password = user_login.password
        
        loginAmbienteSeguro(driver,user,password)
        enterMfeModule(driver)
        company_finder_AmbSeg(driver, app_state.inscricao_estadual)
        
        
        #tem que ver a opção da janela
        cfeQuery(driver, cfe_list.totalList[0])
        
        filterList = analisadorXmls(cfe_list.totalList)
        linkApi = LinkXML(driver)
        
        #Começar processo de download dos XMLS
        for xml in filterList:
            getXML(xml ,linkApi)
            
        time.sleep(2)
        organizarPastas()
        
        time.sleep(1000)
    else:
        raise Exception('Programa encerrado...')

except Exception as e:
    print(f'Erro: {e}')