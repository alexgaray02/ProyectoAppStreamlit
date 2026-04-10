# import pandas as pd

# def documento(archivo):
#     df = pd.read_excel(archivo)
#     cols= [col.strip().lower() for col in df.columns] #Limpiar espacios y pasar a minúsculas

#     if "mes" in cols:
#         tipo = "AM" #año-mes
#     else:
#         tipo = "A" #año
    
#     return df, tipo



######################
import pandas as pd

def documento(archivo):

    # Si ya es DataFrame (viene de Drive)
    if isinstance(archivo, pd.DataFrame):
        df = archivo

    # Si es archivo (upload o ruta)
    else:
        df = pd.read_excel(archivo)

    # Limpiar columnas
    cols = [col.strip().lower() for col in df.columns]

    # Detectar tipo
    if "mes" in cols:
        tipo = "AM"  # año-mes
    else:
        tipo = "A"   # año

    return df, tipo