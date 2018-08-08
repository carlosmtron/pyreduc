# Este módulo es en realidad un script que utiliza las herramientas de astroalign
# para alinear las imágenes previamente calibradas con flats, darks y bias en
# PyReduc.
#
# Astroalign es un simple paquete que alinea dos imágenes astronómicas buscando
# asterismos de tres puntos (tres estrellas) en común entre las dos imágenes, y
# realizando una transformación afín entre ellas.
# El autor del paquete astroalign es Martin Beroiz.
# https://github.com/toros-astro/astroalign


import astroalign
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits as ft


def registra_lista(lista):
    cantidad=len(lista)
    
    # La primera imagen de la lista será la toma de referencia.
    blanco=ft.open(lista[0])
    img_blanco=blanco[0].data
    hdr_blanco=blanco[0].header
    blanco.close()
    del(lista[0]) # Quito la imagen de referencia del listado
    for ii in lista:
        ff=ft.open(ii)
        img_torcida=ff[0].data
        hdr_torcida=ff[0].header
        ff.close()
        img_aligned = astroalign.register(img_torcida, img_blanco)
        hdr_torcida.add_comment("Registrado con Astroalign y PyReduc")
        ft.writeto(ii,img_aligned,header=hdr_torcida,overwrite=True)

    print("\nRegistrado realizado con éxito")


