# Módulo de ecualización de histograma.
# Este módulo es una implementación en lenguaje Python
# del difundido método de ecualización de histogramas
# para el procesamiento digital de imágenes.
#
# La implementación se hizo a partir del algoritmo explicado en
# "Image Processing in C" pp. 33-43, del autor Dwayne Phillips.
# http://dwaynephillips.net/
# Implementación realizada por Carlos Mauricio Silva
# para Pyreduc.

import numpy as np

def histograma(imagen, absi, orde, grises):
    # Función que arma el histograma de la imagen.
    hist = np.zeros(grises)
    for i in range(absi):
        for j in range(orde):
            k = imagen[i,j]
            hist[k] = hist[k] + 1
    return np.array(hist)


def histograma_acumulativo(hist):
    sum = 0
    hist_acum = np.zeros(len(hist))
    for gris in range(len(hist)):
        sum = sum + hist[gris]
        hist_acum[gris] = sum
    return np.array(hist_acum)


def transformacion(imagen):
    imagen = imagen.astype(int) # convierto la imagen a enteros 32 bits con signo
    grises = np.max(imagen)-np.min(imagen) # cant. de niveles de gris de la imagen
    absi, orde = imagen.shape   # Medidas de la imagen
    area = absi * orde
    coef = grises/area
    hist = histograma(imagen, absi, orde, grises)
    hist_acum = histograma_acumulativo(hist)
    salida = np.zeros((absi, orde))
    for i in range(absi):
        for j in range(orde):
            k = int(imagen[i,j])
            salida[i,j]=coef*hist_acum[k]
    return np.array(salida)
