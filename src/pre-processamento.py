import os
import pandas as pd
from pathlib import Path


def get_project_root() -> Path:    
    if '__file__' in globals():        
        return Path(os.path.abspath(__file__)).parent.parent
    else:
        #Path fixo para IPYTHON
        return 'E:/_python_projects/desafio-grpcom'


#Importa dados não tratados
correntistas = pd.read_csv(str(get_project_root()) + "/data/raw/correntistas_banco_bravos.csv",
                           encoding = "ISO-8859-1",
                           sep=';')

obitos = pd.read_csv(str(get_project_root()) + "/data/raw/correntistas_obito.csv",
                         encoding = "ISO-8859-1",
                         sep=';')

#Adiciona atributo para facilitar manipulação
obitos['obitio']=True

#Uni or arquivos pelo nome do correntistas
bravos_correntistas = pd.merge(correntistas, 
                    obitos, 
                    left_on="name", 
                    right_on="Name",
                    how="left")

#verifica integridades dos campos
#House
bravos_correntistas["house"] = bravos_correntistas.apply(lambda x : x['house'] if pd.isna(x['house']) else x['house'].lower().replace('house','').strip(), axis = 1)
bravos_correntistas["Allegiances"] = bravos_correntistas.apply(lambda x : x['Allegiances'] if pd.isna(x['Allegiances']) else x['Allegiances'].lower().replace('house','').strip(), axis = 1)
bravos_correntistas["check_house"] = bravos_correntistas.apply(lambda x : 1 if x['house'] == x['Allegiances'] else 0, axis = 1)

#Nobresa
bravos_correntistas["check_nobresa"] = bravos_correntistas.apply(lambda x : 1 if x['Nobility'] == x['isNoble'] else 0, axis = 1)
check = bravos_correntistas.loc[bravos_correntistas['obitio']==True]
check  = check[['name','house','Allegiances','check_house']]
bravos_correntistas.columns