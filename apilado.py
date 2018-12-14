# Módulo de apilado para PyReduc.
# Autor: Carlos Mauricio Silva
# Recibe una lista de lights y realiza un apilado basado en el promedio de los pixeles.
# Hay un pixel rejection pero lleva MUCHO tiempo, así que no se recomienda.

import numpy as np
from astropy.io import fits as ft
import numpy.ma as ma

def pixel_rejection(cubo, m):
    numimages, absi, orde = cubo.shape
    stack = np.zeros((absi, orde))
    data = np.zeros(numimages)
    print(absi, orde)
    for i in range(absi):
        for j in range(orde):
            data[:] = cubo[:,i,j]
            maskmin = np.mean(data) - np.std(data) * m
            maskmax = np.mean(data) + np.std(data) * m
            stack[i,j] = ma.masked_outside(data, maskmin, maskmax).mean()
            print(i,j)
    return np.array(stack)

def no_rejection(cubo):
    # Creo una nueva imagen con el valor de la media.
    stack = np.mean(cubo,axis=0)
    return np.array(stack)


def stacking(lista, rechazar):
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
    #
    if(rechazar=="1"):
        stack = no_rejection(cubo)
    else:
        stack = pixel_rejection(cubo, m=2)
    ft.writeto("stacking.fit",stack,header=hdr,overwrite=True)
    print("Apilado realizado con éxito. La salida se ha guardado en el archivo stacking.fit")
