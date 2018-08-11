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


def imprimir_info(p, ii):
    # Esta función imprime por pantalla la info de la transformación que se aplicará.
    # Aunque es innecesaria, sirve para que el usuario sepa que la máquina está haciendo algo.
    print("\nAlineando imagen {:}".format(ii))
    print("Rotación: {:.2f} grados".format(p.rotation * 180.0 / np.pi))
    print("Factor de escala: {:.2f}".format(p.scale))
    print("Traslación: (x, y) = ({:.2f}, {:.2f})".format(*p.translation))


def registra_lista(lista):
    cantidad=len(lista)
    
    # La primera imagen de la lista será la toma de referencia.
    print("\nComenzando la alineación.")
    print("\nLa toma de referencia es {:}".format(lista[0])) 
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
        p, (pos_img, pos_img_rot) = astroalign.find_transform(img_torcida, img_blanco)
        imprimir_info(p, ii)
        img_aligned = astroalign.register(img_torcida, img_blanco)
        hdr_torcida.add_comment("Registrado con Astroalign y PyReduc")
        ft.writeto(ii,img_aligned,header=hdr_torcida,overwrite=True)

    print("\nRegistrado realizado con éxito")


