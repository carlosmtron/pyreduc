#!/usr/bin/python3

# PyReduct
# Programa de reducción de imágenes FITS
# Autor: Carlos Mauricio Silva
# Versión: 0.15
#
# Licencia GNU GENERAL PUBLIC LICENSE
# Leer archivo LICENSE que se distribuye con este programa.
#
# Parte del código de calibración con Darks/Bias/Flats está
# basado en el Tutorial "Cómo hacer una reducción básica de imágenes FITS con Python"
# de Ricardo Gil-Hutton. Este tutorial estaba basado en la librería PyFits,
# que ya no se usa y ha sido reemplazada por astropy.io.fits.

import numpy as np
from astropy.io import fits as ft
import glob
import os, shutil
from pathlib import Path

# Presentación
print("_______________________________________")
print("PyReduct")
print("\nPrograma de reducción de imágenes FITS")
print("Autor: Carlos Mauricio Silva")
print("Versión: 0.15")
print("_______________________________________")
print("\nLas imágenes FITS deben estar en un directorio llamado")
print('''"pyreduc/FITS/", dentro del directorio home.''')
print("Los prefijos de los archivos deben seguir las siguientes regla:")
print(''' FLATS: "flat*"\n DARKS: "dark*"\n BIAS: "bias*" \ndonde "*" significa "cualquier cosa". El prefijo de los LIGHTS se ingresa por teclado\n''')

# Averiguo el nombre del directorio home
home = str(Path.home())

#################
### FUNCIONES ###
#################


def copia_de_imagenes():
    # Hago una copia de todos los archivos para no sobreescribir los FITS
    # En la carpeta ~/pyreduc/procesado/
    home = str(Path.home())
    os.chdir(home+"/pyreduc/FITS")
    origen = os.getcwd()
    destino = home+"/pyreduc/procesado/"
    ignorar_pat = shutil.ignore_patterns('*.seq')
    if os.path.exists(destino): # Si el directorio destino existe, lo elimino con todo su contenido
        print("Antes de empezar a trabajar, se borrará el directorio ~/pyreduc/procesado/")
        input("Para cancelar la operación presione Ctrl+C. Para continuar presione Enter")
        shutil.rmtree(destino)
        print("Aguarde mientras se crea una copia de sus imágenes\n") 
        try:                   # Y ahora lo vuelvo a crear copiando todas las imagenes allí     
            arbol = shutil.copytree(origen, destino, ignore=ignorar_pat) 
            print('Todas las imágenes se han copiado a', arbol)
        except:
            print('Error en la copia')
    else:
        print("Aguarde mientras se crea una copia de sus imágenes\n") 
        try:                        
            arbol = shutil.copytree(origen, destino, ignore=ignorar_pat) 
            print('Todas las imágenes se han copiado a', arbol)
        except:
            print('Error en la copia')


def resta_bias(lista,stacked_img):
    for ii in lista:
        ff=ft.open(ii)
        img=ff[0].data
        hdr=ff[0].header
        ff.close()
        img=img-stacked_img
        hdr.add_comment("Procesado por BIAS con PyReduct")
        ft.writeto(ii,img,header=hdr,clobber=True)  # clobber=True significa que va a sobreescribir el archivo.



#####################
### FIN FUNCIONES ###
#####################

copia_de_imagenes() # Llamo a la función que me backupeará las imágenes

# continuar=input("Presione una tecla para continuar")

# Voy al directorio donde están las imágenes copiadas
os.chdir(home+"/pyreduc/procesado")

# Pido al usuario el prefijo de los archivos light
print("\nComenzando a trabajar con sus imágenes en el directorio", os.getcwd())
prefijo=input("\nIntroduzca el prefijo de los archivos lights: ")

# Construyo listas de tomas dark, bias, flat y lights
lista_dark=glob.glob("dark*.fit")
lista_bias=glob.glob("bias*.fit")
lista_flat=glob.glob("flat*.fit")
lista_lights=glob.glob(prefijo+"*.fit")

print("\n")
print("Archivos DARK:\n")
for ii in lista_dark:
    print("{:}: {:}x{:}".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1')))

print("\n")
print("Archivos BIAS:\n")
for ii in lista_bias:
    print("{:}: {:}x{:}".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1')))

print("\n")
print("Archivos FLAT:\n")
for ii in lista_flat:
    print("{:}: {:}x{:}".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1')))

print("\n")
print("Archivos LIGHTS:\n")
for ii in lista_lights:
    print("{:}: {:}x{:}".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1')))

# Guardo la cantidad de archivos de cada lista en una variable distinta:
numflat=len(lista_flat)
numbias=len(lista_bias)
numdark=len(lista_dark)
numlights=len(lista_lights)


# Proceso de BIAS. Voy a armar una matriz cúbica de los bias.
print("\nProcesando BIAS. Por favor, aguarde...")

# Genero una matriz 3D de ceros
cubo_bias=np.zeros((numbias,ft.getval(lista_bias[1],'naxis2'),ft.getval(lista_bias[1],'naxis1')),dtype=float)
# Copio los BIAS a la matriz cúbica
nro=0
for ii in lista_bias:
    ff=ft.open(ii)
    img=ff[0].data
    hdr=ff[0].header
    ff.close()
    cubo_bias[nro,:,:]=np.copy(img)
    nro+=1

# Ordeno los pixeles de mayor a menor a lo largo del primer eje.
cubo_bias=np.sort(cubo_bias,axis=0)

# Creo una nueva imagen con el valor de la mediana, despreciando el valor más alto de cada pixel.
stbias=np.median(cubo_bias[0:numbias-1],axis=0)

# Resto la nueva imagen a los lights
resta_bias(lista_lights,stbias)
    
# Resto la nueva imagen a los flats
resta_bias(lista_flat,stbias)

    

# Proceso de FLATS. Voy a armar una matriz cúbica de los flats.
# Nótese que los flats ya fueron procesados con los bias.
print("\nProcesando FLATS. Por favor, aguarde...")
# Genero una matriz 3D de ceros
cubo_flat=np.zeros((numflat,ft.getval(lista_bias[1],'naxis2'),ft.getval(lista_bias[1],'naxis1')),dtype=float)

# Copio los FLATS a la matriz cúbica
nro=0
sum=0
for ii in lista_flat:
    ff=ft.open(ii)
    img=ff[0].data
    hdr=ff[0].header
    ff.close()
    med=np.median(img)
    sum+=med
    cubo_flat[nro,:,:]=np.copy(img)*med
    nro+=1

# Creo una nueva imagen a partir de los valores medios, despreciando los valores más altos,
# pero normalizo con la suma de las medianas de cada imagen.
stflat=np.mean(cubo_flat[0:numflat-1],axis=0)/sum
mflat=np.mean(stflat)


# Divido las imágenes lights por el master-flat resultante.
for ii in lista_lights:
    ff=ft.open(ii)
    img=ff[0].data
    hdr=ff[0].header
    ff.close()
    img=img/stflat*mflat
    hdr.add_comment("Procesado por FLATS con PyReduct")
    ft.writeto(ii,img,header=hdr,clobber=True)


