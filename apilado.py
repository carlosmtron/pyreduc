# Módulo de apilado para PyReduc.
# Autor: Carlos Mauricio Silva
# Recibe una lista de lights y realiza un apilado basado en el promedio de los pixeles.
# Por el momento no se implementó ningún tipo de Pixel Rejection.

import numpy as np
from astropy.io import fits as ft


def stacking(lista):
    cantidad=len(lista)
    print("\nComenzando el apilado...")
    # Genero una matriz 3D de ceros
    cubo=np.zeros((cantidad,ft.getval(lista[0],'naxis2'),ft.getval(lista[0], 'naxis1')),dtype=float)
    # Copio los lights a la matriz 3D
    nro=0
    for ii in lista:
        ff=ft.open(ii)
        img=ff[0].data
        hdr=ff[0].header
        ff.close()
        cubo[nro,:,:]=np.copy(img)
        nro+=1

    # Ordeno los pixeles de mayor a menor a lo largo del primer eje.
    # cubo=np.sort(cubo,axis=0)

    # Creo una nueva imagen con el valor de la media.
    stack=np.mean(cubo[0:cantidad],axis=0)
    ft.writeto("stacking.fit",stack,header=hdr,overwrite=True)
    print("Apilado realizado con éxito. La salida se ha guardado en el archivo stacking.fit")

