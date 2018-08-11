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
    stack = np.mean(cubo[0:cantidad],axis=0)
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


#Las siguientes líneas sirven para probar el Script sin necesidad de ejecutar el main.
if __name__ == '__main__':
    import os
    from pathlib import Path
    
    home = str(Path.home())
    os.chdir(home+"/pyreduc/procesado")

    matriz1 = [[1.21, 1.51, 2.19, 3.25], [1.22, 1.56, 3.58, 4.25], [1.21, 2.16, 4,32, 5.52], [1.8, 2.4, 3.3, 2.9]]
    matriz2 = [[1.23, 1.56, 2.29, 3.45], [1.32, 1.66, 3.68, 4.25], [1.10, 2.16, 4,52, 5.62], [1.82, 2.34, 3.13, 3.1]]
    matriz3 = [[1.30, 1.46, 2.29, 3.65], [1.33, 1.57, 3.78, 4.55], [1.20, 5.16, 7,52, 5.60], [1.83, 2.33, 3.14, 2.69]]
    matriz4 = [[1.33, 1.51, 2.29, 3.45], [1.32, 1.66, 3.78, 4.25], [1.10, 2.36, 4,52, 5.62], [1.82, 2.34, 3.13, 3.1]]
    matriz5 = [[1.63, 1.56, 2.31, 3.35], [7.32, 2.66, 3.68, 4.28], [1.11, 2.16, 4,55, 5.63], [1.85, 2.36, 3.21, 2.74]]

