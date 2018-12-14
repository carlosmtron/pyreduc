#!/usr/bin/python3

# PyReduc
# Programa de reducción de imágenes FITS
# Autor: Carlos Mauricio Silva
# Versión: 0.2.5
#
# Licencia GNU GENERAL PUBLIC LICENSE
# Leer archivo LICENSE que se distribuye con este programa.
#
# Parte del código de calibración con Darks/Bias/Flats está
# basado en el Tutorial "Cómo hacer una reducción básica de imágenes FITS con Python"
# de Ricardo Gil-Hutton. Este tutorial estaba basado en la librería PyFits,
# que ya no se usa y ha sido reemplazada por astropy.io.fits.
# La fórmula de reducción de imágenes científicas que se utiliza aquí fue tomada del curso
# "Introduction to Astronomical Image Analysis" de  Matthew Craig, Juan Cabanela & Linda Winkler.

import numpy as np
from astropy.io import fits as ft
import glob
import os, shutil
from pathlib import Path

import apilado
import registrado
import visualizacion

# Presentación
print("_______________________________________")
print("PyReduc")
print("\nPrograma de reducción de imágenes FITS")
print("Autor: Carlos Mauricio Silva")
print("Versión: 0.2.0")
print("_______________________________________")
print("\nLas imágenes FITS deben estar en un directorio llamado")
print('''"pyreduc/FITS/", dentro del directorio home.''')
print("Los prefijos de los archivos deben seguir las siguientes reglas:")
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


def mediana_calib(listaimg,numimg):
    # Genero una matriz 3D de ceros
    cubo_nuevo=np.zeros((numimg,ft.getval(listaimg[0],'naxis2'),ft.getval(listaimg[0],'naxis1')),dtype=float)
    # Copio las tomas de calibración a la matriz cúbica
    nro=0
    for ii in listaimg:
        ff=ft.open(ii)
        img=ff[0].data
        hdr=ff[0].header
        ff.close()
        cubo_nuevo[nro,:,:]=np.copy(img)
        nro+=1
        
    # Ordeno los pixeles de menor a mayor a lo largo del primer eje.
    cubo_nuevo=np.sort(cubo_nuevo,axis=0)
    
    # Creo una nueva imagen con el valor de la mediana, despreciando el valor más alto de cada pixel.
    return np.median(cubo_nuevo[0:numbias-1],axis=0)


            
def resta_master(lista,stacked_img):
    for ii in lista:
        ff=ft.open(ii)
        img=ff[0].data
        hdr=ff[0].header
        ff.close()
        img=img-stacked_img
        hdr.add_comment("Procesado por DARK y BIAS con PyReduc")
        ft.writeto(ii,img,header=hdr,overwrite=True)  # overwrite=True va a sobreescribir cada archivo.




#####################
### FIN FUNCIONES ###
#####################

copia_de_imagenes() # Llamo a la función que me backupeará las imágenes

# Voy al directorio donde están las imágenes copiadas
os.chdir(home+"/pyreduc/procesado")

# Pido al usuario el prefijo de los archivos light
print("\nComenzando a trabajar con sus imágenes en el directorio", os.getcwd())
prefijo=input("\nIntroduzca el prefijo de los archivos lights (tomas científicas): ")

# Construyo listas de tomas dark, bias, flat y lights
lista_dark=glob.glob("dark*.fit")
lista_bias=glob.glob("bias*.fit")
lista_flat=glob.glob("flat*.fit")
lista_lights=glob.glob(prefijo+"*.fit")

print("\n")
print("Archivos DARK:\n")
for ii in lista_dark:
    print("{:}: {:}x{:}  EXPTIME={:} s".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1'),ft.getval(ii,'exptime')))

print("\n")
print("Archivos BIAS:\n")
for ii in lista_bias:
    print("{:}: {:}x{:}  EXPTIME={:} s".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1'),ft.getval(ii,'exptime')))    

print("\n")
print("Archivos FLAT:\n")
for ii in lista_flat:
    print("{:}: {:}x{:}  EXPTIME={:} s".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1'),ft.getval(ii,'exptime')))    

print("\n")
print("Archivos LIGHTS (tomas científicas):\n")
for ii in lista_lights:
    print("{:}: {:}x{:}  EXPTIME={:} s".format(ii,ft.getval(ii,'naxis2'),ft.getval(ii,'naxis1'),ft.getval(ii,'exptime')))

print("\nTenga en cuenta que para la calibración se toma el tiempo de exposición de su primer toma científica.")
print("PyReduc no dará los mejores resultados si sus tomas científicas tienen diferentes tiempos de exposición.")

continuar=input("Presione una tecla para continuar")

print("\nAl final del proceso se realizará un apilado de sus imágenes calibradas y alineadas. Este se puede realizar a través de un promedio simple de las imágenes, o con un promedio que rechace valores extremos (Pixel Rejection). ¿Qué desea hacer?")
print("1. Apilar promediando las imágenes")
print("2. Aplicar Pixel Rejection (POCO EFICIENTE. NO RECOMENDADO.)")
print("3. No apilar")
rechazar_pixel = input("Ingrese 1, 2 o 3: ")
while(rechazar_pixel not in ["1", "2", "3"]):
    print("Opción inválida")
    rechazar_pixel = input("Ingrese 1, 2 o 3: ")
    

# Guardo la cantidad de archivos de cada lista en una variable distinta:
numflat=len(lista_flat)
numbias=len(lista_bias)
numdark=len(lista_dark)
numlights=len(lista_lights)

# Voy a obtener el tiempo de exposición de los lights, flats y darks
# Voy a suponer que todas las tomas de un mismo tipo tienen la misma exposición.
exp_lights=ft.getval(lista_lights[0],'exptime')
exp_flat=ft.getval(lista_flat[0],'exptime')
exp_dark=ft.getval(lista_dark[0], 'exptime')

# Proceso de BIAS. Voy a armar una matriz cúbica de los bias.
print("\nProcesando BIAS. Por favor, aguarde...")

stbias = mediana_calib(lista_bias, numbias)


# Proceso de DARK.
print("\nProcesando DARK. Por favor, aguarde...")

# Primero, voy a restar un master-bias a los dark, para formar una lista de pre-DARK-current.
print("\nSustrayendo un master-bias a los dark. Aguarde...")
resta_master(lista_dark, stbias)

# Ahora realizo el apilado para generar la imagen Dark-current
stdark = mediana_calib(lista_dark, numdark)


# Ahora voy a crear una imagen que es la suma de DARK-current escalado y BIAS
# para corregir los lights
master_stack = stbias + stdark/exp_dark*exp_lights

# Resto la nueva imagen a los lights
resta_master(lista_lights, master_stack)


# para corregir los flats
master_stack = stbias + stdark/exp_dark*exp_flat

# Resto la nueva imagen a los flats
resta_master(lista_flat, master_stack)


# Proceso de FLATS. Voy a armar una matriz cúbica de los flats.
# Nótese que los flats ya fueron corregidos con bias y dark-current.
print("\nProcesando FLATS. Por favor, aguarde...")
# Genero una matriz 3D de ceros
cubo_flat=np.zeros((numflat,ft.getval(lista_bias[0],'naxis2'),ft.getval(lista_bias[0],'naxis1')),dtype=float)

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
    hdr.add_comment("Procesado por FLATS con PyReduc")
    ft.writeto(ii,img,header=hdr,overwrite=True)

   
# Alineación de imágenes:

registrado.registra_lista(lista_lights)

salir="1"

# Stacking o apilado de imágenes:
lista_lights=glob.glob(prefijo+"*.fit") # Reconstruyo la lista de lights
# Si el usuario pidio apilar, se apila, y si no, se sale del programa.
if(rechazar_pixel=="1" or rechazar_pixel=="2"):
    apilado.stacking(lista_lights, rechazar_pixel)
else:
    salir="2"


while(salir=="1"):
    print("¿Qué desea hacer?")
    print("1: Ver la imagen resultante")
    print("2: Salir")
    salir=input("Ingrese 1 o 2: ")
    if(salir=="1"):
        # Visualización por pantalla de la imagen:
        visualizacion.visual("stacking.fit")
    elif(salir=="2"):
        break
    else:
        print("Opción no válida")
        salir="1"

    
print("Gracias por utilizar PyReduc")

import gc
# Saco la basura y se la lleva el camión recolector
gc.collect()
