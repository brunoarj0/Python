#IMPORTAÇÕES
from datetime import date
from fastapi import FastAPI, UploadFile, File, HTTPException
from camelot import read_pdf
import shutil
import os
import time
import PyPDF2

#ATIVAÇÃO API
app = FastAPI()

#URL DA API
@app.post('/final')

#PASSANDO OS PARÂMETROS DA API
async def final(file : UploadFile = File(...), pag: str="1", fla: str="stream", tab: str="31.409828707107494,689.9798115213234,308.27997292985225,466.1200817912839", col: str="53.058767880338735,106.11747687979764,156.278746103733,209.32076237375776,259.49881264844703", spl: bool=False, rct: str='2', cct: str='0', flg: bool=False):

    #COLETANDO OS PARÂMETROS
    parametros = {"flavor": fla, "pages": pag, 'table_areas': tab, "columns": col, "split_text": spl, "row_close_tol": rct, "col_close_tol": cct, "flag_size": flg}

    #CONTANDO PÁGINAS

    #CRIANDO ARQUIVO A PARTIR DO UPLOAD
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    #TRATANDO ERROS NA DEFINICAO DE PARAMETROS
    pdfFileObj = open(f'{file.filename}', 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    pdf_pag = pdfReader.numPages

    if int(pag) > pdf_pag:
        raise HTTPException(status_code=500, detail="Numero de paginas incorreto")

    if fla != "stream":
        raise HTTPException(status_code=500, detail="Flavor incorreto")

    #COLETANDO DATA DA CRIAÇÃO DO ARQUIVO
    date_seg = os.path.getctime(file.filename)
    date_nor = time.ctime(date_seg)

    #CONVERTENDO A TABELA DO PDF EM ARQUIVO 'JSON'
    #print(pag, fla, tab.split(','), col.split(','))
    table = read_pdf(f'{file.filename}', pages=pag, flavor=fla, table_areas=[tab], columns=[col], split_text=spl, row_close_tol=rct, col_close_tol=cct, flag_size=flg)
    table.export(f'{file.filename}' + '.json', f='json')
    
    #COLETANDO OS DADOS DO ARQUIVO 'JSON'
    with open(f'{file.filename}' + f'-page-{pag}-table-1.json', 'r') as arquivo:
        data = arquivo.read()

    #RETORNANDO AS INFORMAÇÕES (DADOS, PARAMETROS E DATA)
    return{"data": data, "parametros": parametros, "criacao": date_nor}
