import pandas as pd

def documento(archivo):
    df = pd.read_excel(archivo)
    cols= [col.strip().lower() for col in df.columns] #Limpiar espacios y pasar a minúsculas

    if "mes" in cols:
        tipo = "AM" #año-mes
    else:
        tipo = "A" #año
    
    return df, tipo
    