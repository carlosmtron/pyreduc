# ToDo List
## Última actualización 11/08/2018

v1.0
- [ ] ¿Registrado basado en PSF?

v0.7 "Avanzada"
- [ ] ¿Implementar PSF?
- [ ] Solucionar el problema de escalado a 64 bits. Las imágenes resultantes de cada proceso tendrían que volver a ser de 16 bits.

v0.3 "Amanecida"
- [ ] ¿Debayering sí o no?
- [ ] Implementar un módulo de reconocimiento de estrellas.
- [ ] Eliminar los archivos Darks, Bias y Flats de la carpeta procesado una vez que los lights ya estén calibrados.
- [ ] Implementar alguna forma de "Pixel rejection".

v0.2 "Crepuscular"
- [x] Alinear las imágenes con algún algoritmo de terceros.
- [x] Apilar las imágenes lights ya calibradas.

v0.17 "Oscura"
- [x] Hacer un módulo para restar Bias a los lights y a los flats, y separarlo del 'main'.
- [x] Cambiar la librería PyFits por astropy.io.fits.
- [x] Actualizar comandos de PyFits que quedaron obsoletos.
- [x] Hacer un módulo para restar los DARKS.

v0.15 "Respetuosa"
- [x] Que los archivos de imagen se copien a otro directorio para no sobreescribir los FITS originales.

v0.11 "Ordenada"
- [x] Que los archivos de imagen estén en una carpeta separada del ejecutable.

v0.1 "Original"
- [x] Subir todo a un repositorio Git
- [x] Procesado básico con Bias y Flats
