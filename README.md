# PyReduc
[![DOI](https://zenodo.org/badge/133057983.svg)](https://zenodo.org/badge/latestdoi/133057983)

## Programa de reducción de imágenes astronómicas FITS usando Python
Autor: Carlos Mauricio Silva

Versión: 0.2.5

Licencia GNU GENERAL PUBLIC LICENSE

Leer archivo LICENSE que se distribuye con este programa.
________________________________________________________
[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

Parte del código de calibración con Darks/Bias/Flats está
basado en el tutorial [*"Cómo hacer una reducción básica de imágenes FITS con Python"*](https://freeshell.de/~rgh/arch/python/python-red-basica.pdf)
de Ricardo Gil-Hutton. Este tutorial empleaba la librería PyFits, que ya no se usa
y ha sido reemplazada por astropy.io.fits para escribir PyReduc.
La fórmula de reducción de imágenes científicas que se utiliza aquí fue tomada del curso
[*"Introduction to Astronomical Image Analysis"*](http://image-analysis.readthedocs.io/en/latest/index.html) de  Matthew Craig, Juan Cabanela & Linda Winkler.
_______________________________________________________

### INSTALACIÓN:
Para correr este programa es necesario tener instalado Python 3 y las librerías científicas numpy, astropy.io, scikit-image.
Si está en un sistema operativo basado en Debian (como ubuntu) asegúrese de instalar las dependencias previamente:
```
	sudo apt-get install python3 python3-numpy python3-scipy python3-astropy python3-pip python3-skimage
```
Este programa utiliza para alinear las imágenes, una vez calibradas, el programa [*Astroalign* de Martin Beroiz](https://github.com/toros-astro/astroalign). El mismo se puede instalar desde la Terminal:
```
	pip3 install astroalign
```

Una vez instaladas las dependencias, extraiga el programa en el directorio "~/pyreduc/", donde ~/ representa su directorio home.

Para ejecutar el programa, estando en la carpeta ~/pyreduc/ ejecute la orden:
```
	./pyreduc.py
```

### IMPORTANTE:
Las imágenes FITS deben estar en un directorio llamado "~/pyreduc/FITS/".
- Los prefijos de los archivos deben seguir las siguientes reglas:
  - FLATS: "flat*"
  - DARKS: "dark*"
  - BIAS: "bias*"
donde "*" significa "cualquier cosa a partir de aquí".
- El prefijo de los LIGHTS se ingresa por teclado.

Por ejemplo:
- En la carpeta ~/pyreduc/FITS/ se tienen los archivos:
  - bias001.fit, bias002.fit, bias003.fit bias004.fit,...
  - darkA.fit, darkB.fit, darkC.fit,...
  - flat_0001.fit,..., flat_0005.fit,..., flat_0011.fit
  - RCnc_001.fit, RCnc_002.fit, RCnc_003.fit,...,
entonces sus tomas de calibración tienen el nombre correcto. Cuando el programa pida el prefijo de las tomas LIGHTS (es decir, sus tomas científicas),
se deberá ingresar por teclado:
```
	RCnc
```
Nota: *En este caso también puede ingresar "R", puesto que es el único prefijo de archivo que comienza con esa letra en su directorio FITS/.*


*Por favor, note que este programa no convierte imágenes RAW a FITS (¿Quizás en una próxima versión?).*
*Por ahora el programa funciona bien con imágenes monocromáticas. RGB/RGGB/otras yerbas, quizás en un futuro...*
