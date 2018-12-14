# Script de visualización de imágenes FITS.
# Primero se muestra un histograma de la imagen y se le pide
# al usuario que acote el rango de visualización máximo y mínimo
# a partir del histograma. Otra opción posible es que el programa ajuste automáticamente el histograma a través de una ecualización. Por último, también se proporciona la opción de reescalar el histograma entre los percentiles 2 y 98, solo con fines de explorar la librría skimage. Las otras opciones de esa librería no proporcionaron buenos resultados.

import numpy as np
from astropy.io import fits as ft
import matplotlib
import matplotlib.pyplot as plt

from skimage import data, img_as_float
from skimage import exposure

import ecualizado

def modo_histograma(n, imagen):
    def caso_manual(image_data):
        print("\nA continuación se mostrará el histograma de la imagen apilada y se le pedirá que elija los valores límites para estirar el histograma antes de visualizar la imagen. Esto es solo para visualizarla mejor y no afectará los datos de la imagen.")
        print("Cierre el histograma para continuar...")
        #
        valmin=np.mean(image_data)-3*np.std(image_data)
        valmax=np.mean(image_data)+3*np.std(image_data)
        image_hist = plt.hist(image_data.flatten(), bins=1000, range=(valmin,valmax))
        plt.show(image_hist)
        #
        valmin=input("A partir del histograma, ingrese el mínimo valor deseado: ")
        valmax=input("Ingrese el máximo valor deseado: ")
        interpolar=input('Desea usar una interpolación para mejorar el aspecto visual de la imágen? (Esto no afectará a los datos de la imagen, es solo para la visualización) (s/N): ')
        if(interpolar=="s" or interpolar=="S"):
            interp='bilinear'
        else:
            interp='none'
            
        plt.imshow(image_data, cmap='gray', vmin=valmin, vmax=valmax, interpolation=interp)
        plt.colorbar()
        plt.show()
            
            
    def caso_ecualizador(imagen):
        nueva_imagen = ecualizado.transformacion(imagen)
        plt.imshow(nueva_imagen, cmap='gray', interpolation='bilinear')
        plt.colorbar()
        plt.show()


    def caso_avanzado(imagen):
        # Esta función utiliza el reescalado de la librería skimage
        p2, p98 = np.percentile(imagen, (2, 98))
        img_rescale = exposure.rescale_intensity(imagen, in_range=(p2, p98))
        # Si quiero probar la ecualización de histograma de skimage, en lugar de la «casera»
        # exposure.equalize_hist(imagen)
        #
        plt.imshow(img_rescale, cmap='gray', interpolation='bilinear')
        plt.colorbar()
        plt.show()
        

    def caso_invalido(imagen):
        print("Opción inválida")

    print(n)    
    tabla = {"1": caso_manual, "2": caso_ecualizador, "3": caso_avanzado}
    opcion = tabla.get(n, caso_invalido)
    opcion(imagen)
    

def visual(imagen):
    image_data = ft.getdata(imagen)
    print("\nEstadísticas de la imagen:")
    print('Min:', np.min(image_data))
    print('Máx:', np.max(image_data))
    print('Promedio:', np.mean(image_data))
    print('Desvío Estándar:', np.std(image_data))
    #
    print("\nPara visualizar la imagen correctamente, se puede realizar un clipping (recorte manual) personalizado del histograma, elegir el ecualizado automático o un stretching automático entre los percentiles 2 y 98. ¿Qué desea hacer?")
    print("1. Recorte Manual del histograma")
    print("2. Ecualización automática del histograma")
    print("3. Recorte automático entre los percentiles 2 y 98")
    n = input("Ingrese 1, 2 o 3: ")
    modo_histograma(n, image_data)

    
#Las siguientes líneas sirven para probar el Script sin necesidad de ejecutar el main.
if __name__ == '__main__':
    import os
    from pathlib import Path
    
    home = str(Path.home())
    os.chdir(home+"/pyreduc/procesado")
    imagen = input("Ingrese el nombre de archivo de la imagen a visualizar. Se asume que la imagen está ubicada en la carpeta procesado.\n")
    visual(imagen)
