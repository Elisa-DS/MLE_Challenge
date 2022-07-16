import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import numpy as np
import locale
import joblib
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')




#import ds_utilidades as ds



##############################################################################
#                       DATA CLEANING
##############################################################################

# Data Conversion and scale
def convert_int(x):
    return int(x.replace('.', ''))


def to_100(x): #mirando datos del bc, pib existe entre ~85-120 - igual esto es cm (?)
    x = x.split('.')
    if x[0].startswith('1'): #es 100+
        if len(x[0]) >2:
            return float(x[0] + '.' + x[1])
        else:
            x = x[0]+x[1]
            return float(x[0:3] + '.' + x[3:])
    else:
        if len(x[0])>2:
            return float(x[0][0:2] + '.' + x[0][-1])
        else:
            x = x[0] + x[1]
            return float(x[0:2] + '.' + x[2:])



def dcPrecipitaciones():
    
    #
    # Data Cleaning PRECIPITACIONES
    #
    pd.options.mode.chained_assignment = None  # default='warn'
    plt.style.use('seaborn-notebook')
    
    
    precipitaciones = pd.read_csv('./data/precipitaciones.csv')#[mm]
    precipitaciones['date'] = pd.to_datetime(precipitaciones['date'], format = '%Y-%m-%d')
    precipitaciones = precipitaciones.sort_values(by = 'date', ascending = True).reset_index(drop = True)
    
    
    precipitaciones[precipitaciones.isna().any(axis=1)] #no tiene nans
    
    precipitaciones[precipitaciones.duplicated(subset = 'date', keep = False)] #ni repetidos
    
    regiones = ['Coquimbo', 'Valparaiso', 'Metropolitana_de_Santiago',
           'Libertador_Gral__Bernardo_O_Higgins', 'Maule', 'Biobio',
           'La_Araucania', 'Los_Rios']
    precipitaciones[regiones].describe() 



    precipitaciones['mes'] = precipitaciones.date.apply(lambda x: x.month)
    precipitaciones['ano'] = precipitaciones.date.apply(lambda x: x.year)
    
    return precipitaciones



def dcBancoCentral():
    
    #
    # Data Cleaning BANCO CENTRAL
    #
    
    banco_central = pd.read_csv('./data/banco_central.csv')
    banco_central
    
    
    banco_central['Periodo'] = banco_central['Periodo'].apply(lambda x: x[0:10])
    
    banco_central['Periodo'] = pd.to_datetime(banco_central['Periodo'], format = '%Y-%m-%d', errors = 'coerce')
    
    banco_central[banco_central.duplicated(subset = 'Periodo', keep = False)] #repetido se elimina
    
    banco_central.drop_duplicates(subset = 'Periodo', inplace = True)
    banco_central = banco_central[~banco_central.Periodo.isna()]
    

    
    cols_pib = [x for x in list(banco_central.columns) if 'PIB' in x]
    cols_pib.extend(['Periodo'])
    banco_central_pib = banco_central[cols_pib]
    banco_central_pib = banco_central_pib.dropna(how = 'any', axis = 0)
    
    for col in cols_pib:
        if col == 'Periodo':
            continue
        else:
            banco_central_pib[col] = banco_central_pib[col].apply(lambda x: convert_int(x))
    
    banco_central_pib.sort_values(by = 'Periodo', ascending = True)
    
        
            
    cols_imacec = [x for x in list(banco_central.columns) if 'Imacec' in x]
    cols_imacec.extend(['Periodo'])
    banco_central_imacec = banco_central[cols_imacec]
    banco_central_imacec = banco_central_imacec.dropna(how = 'any', axis = 0)
    
    for col in cols_imacec:
        if col == 'Periodo':
            continue
        else:
            banco_central_imacec[col] = banco_central_imacec[col].apply(lambda x: to_100(x))
            assert(banco_central_imacec[col].max()>100)
            assert(banco_central_imacec[col].min()>30)
    
    banco_central_imacec.sort_values(by = 'Periodo', ascending = True)
    banco_central_imacec
    
    banco_central_iv = banco_central[['Indice_de_ventas_comercio_real_no_durables_IVCM', 'Periodo']]
    banco_central_iv = banco_central_iv.dropna() # -unidades? #parte 
    banco_central_iv = banco_central_iv.sort_values(by = 'Periodo', ascending = True)
    
    
    banco_central_iv.head() #unidades? https://si3.bcentral.cl/siete/ES/Siete/Canasta?idCanasta=M57TP1161519 porcentajes?
    
    banco_central_iv['num'] = banco_central_iv.Indice_de_ventas_comercio_real_no_durables_IVCM.apply(lambda x: to_100(x))
    
    banco_central_iv.Periodo.min()
    
    banco_central_iv.Periodo.max()
    
    banco_central_num = pd.merge(banco_central_pib, banco_central_imacec, on = 'Periodo', how = 'inner')
    banco_central_num = pd.merge(banco_central_num, banco_central_iv, on = 'Periodo', how = 'inner')

    banco_central_num['mes'] = banco_central_num['Periodo'].apply(lambda x: x.month)
    banco_central_num['ano'] = banco_central_num['Periodo'].apply(lambda x: x.year)

    return banco_central_num



def dcMilkPrice():
    #
    # Data Cleaning PRECIO LECHE
    #
    
    precio_leche = pd.read_csv('./data/precio_leche.csv')
    precio_leche.rename(columns = {'Anio': 'ano', 'Mes': 'mes_pal'}, inplace = True) # precio = nominal, sin iva en clp/litro
    precio_leche['mes'] = pd.to_datetime(precio_leche['mes_pal'], format = '%b')
    precio_leche['mes'] = precio_leche['mes'].apply(lambda x: x.month)
    precio_leche['mes-ano'] = precio_leche.apply(lambda x: f'{x.mes}-{x.ano}', axis = 1)

    return precio_leche



def dataClean():
    precio_leche_pp = pd.merge(dcMilkPrice(), dcPrecipitaciones(), on = ['mes', 'ano'], how = 'inner')
    precio_leche_pp.drop('date', axis = 1, inplace = True)
    precio_leche_pp #precipitaciones fecha_max = 2020-04-01

    precio_leche_pp_pib = pd.merge(precio_leche_pp, dcBancoCentral(), on = ['mes', 'ano'], how = 'inner')
    precio_leche_pp_pib.drop(['Periodo', 'Indice_de_ventas_comercio_real_no_durables_IVCM', 'mes-ano', 'mes_pal'], axis =1, inplace = True)

    # Using Pickle for Serialization

    joblib.dump(precio_leche_pp_pib, './serialization/trainingDataSet.pkl')
