import os
import json
import pandas as pd
from pathlib import Path

def get_project_root() -> Path:    
    if '__file__' in globals():        
        return Path(os.path.abspath(__file__)).parent.parent
    else:
        #Path fixo para executar via IPYTHON
        return 'E:/_python_projects/desafio-grpcom'

def convert_float(x):
    return float(x.lower().replace('r$ ','').strip().replace('.','').replace(',','.'))

def correcao_house(x):
    if pd.isna(x['house']):
        return x['name']
    elif x['house']=='House Starrkk':
        return 'House Stark'
    elif x['house']=='House Lannnister':
        return 'House Lannister'
    else:
        return x['house']

#Importa dados não tratados
correntistas = pd.read_csv(str(get_project_root()) + "/data/raw/correntistas_banco_bravos.csv",
                           encoding = "ISO-8859-1",
                           sep=';')

obitos = pd.read_csv(str(get_project_root()) + "/data/raw/correntistas_obito.csv",
                         encoding = "ISO-8859-1",
                         sep=';')

#Adiciona atributo para facilitar manipulação
obitos['isDead']=True

#Uni or arquivos pelo nome do correntistas
bravos_correntistas = pd.merge(correntistas, 
                    obitos, 
                    left_on="name", 
                    right_on="Name",
                    how="left")

#remove contas inativas
bravos_correntistas = bravos_correntistas.loc[bravos_correntistas['isDead']!=True]
#remove linha em branco
bravos_correntistas = bravos_correntistas.dropna(subset = ['name'])

#converte divida e capacidade de pagamento para float
bravos_correntistas["Dívida"] = bravos_correntistas["Dívida"].apply(convert_float)
bravos_correntistas["Capacidade de pagamento anual"] = bravos_correntistas["Capacidade de pagamento anual"].apply(convert_float)

#calcula patrimonio Capacidade de pagamento - Divida
bravos_correntistas["patrimonio"] = bravos_correntistas.apply(lambda x : x['Capacidade de pagamento anual']-x['Dívida'] , axis = 1)

#Correção no nome das casas e sem casas
bravos_correntistas["house"] = bravos_correntistas.apply(correcao_house , axis = 1)

#agrupa por casas
gp = bravos_correntistas.groupby(['house']).sum().sort_values(by='patrimonio', ascending=False)

#remover patrimonios negativos
gp = gp.loc[gp['patrimonio']>0]

#Calcula Acumulado
gp['acumulado']= gp['patrimonio'].cumsum()
gp['representacao']= gp['patrimonio']/gp['patrimonio'].sum()
gp['acumulado%']= round(gp['representacao'].cumsum()*100,2)

len(gp.loc[gp['acumulado%']<0.5])

dic_json = {
        "chart":{
                   "categories" : gp.index.tolist(),
                   "acumulado" : gp['acumulado%'].tolist(),
                   "patrimonio" : gp['patrimonio'].tolist(),
                   "plot_bands": {
                        "a": len(gp.loc[gp['acumulado%']<50]),
                        "b": len(gp.loc[gp['acumulado%']<80]),
                        "c": len(gp['acumulado%'])
                        }
                }
        }

with open(get_project_root()+'/data/result/chart.json', 'w') as outfile:
    json.dump(dic_json, outfile)


#Codigo usado para analise
#verifica integridades dos campos
#House
#bravos_correntistas["house"] = bravos_correntistas.apply(lambda x : x['house'] if pd.isna(x['house']) else x['house'].lower().replace('house','').strip(), axis = 1)
#bravos_correntistas["Allegiances"] = bravos_correntistas.apply(lambda x : x['Allegiances'] if pd.isna(x['Allegiances']) else x['Allegiances'].lower().replace('house','').strip(), axis = 1)
#bravos_correntistas["check_house"] = bravos_correntistas.apply(lambda x : 1 if x['house'] == x['Allegiances'] else 0, axis = 1)

#Nobresa
#bravos_correntistas["check_nobresa"] = bravos_correntistas.apply(lambda x : 1 if x['Nobility'] == x['isNoble'] else 0, axis = 1)
#check = bravos_correntistas.loc[bravos_correntistas['obitio']==True]
#check  = check[['name','house','Allegiances','check_house']]


