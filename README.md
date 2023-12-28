# [Consistency of Long-Term Trends in the Surface Water Balance of the Amazon River Basin](https://repositorio.unal.edu.co/bitstream/handle/unal/78191/1037589068.2020.pdf?sequence=11)

---
Keywords: Amazon, Hydrologic Balance, Long term Trends, Consistency, Timeseries Gap Filling, Empirical Mode Decomposition
---
The consistency of long-term trends in the water balance of the Amazon basin was studied. For this, series of variables in the water balance equation (precipitation, evaporation, runoff and soil water storage) were obtained from remote sensors and flow stations (CHIRPS, ETR-Amazon, ANA-Brazil and GRACE). The gaps of the timeseries were filled applying an adaptation of the methodology proposed by Kondrashov & Ghil (2006) in the 20-year period between february 1995 and february 2015. To determine the reliability of the gap filling, a validation of the method was performed, resulting in the selection of 64 study basins from a group of 109 initially used. The selected basins obtained an acceptable performance in the reconstruction of the series of at least 3 variables for the EMAR (relative absolute mean error), KS (Kolmogorov-smirnov test) and MK (Mann-Kendall test) metrics.

On the selected series, the DME (decomposition in empirical modes) was applied to filter the natural variability and isolate the residue that represents the average trend of the series. The Mann - Kendall and Sen tests were applied to the residue and the sign and magnitude of the trends was obtained. No generalized unidirectional trend for the Amazon basin was found on any of the variables studied. However, when the main stream basins were analyzed, a uniform behavior of the trends of each variable was found for each stream.

The consistency of the general water balance equation in short-term conditions and its approximation to the long-term condition were also evaluated, finding that in the short-term the balance does not close, and that in the long-term the error in the balance trends asymptotically to a constant value, different from zero, which indicates that in the period of 20 years studied the long-term condition is fulfilled, but there is no closure for the long-term balance either. The consistency of the balance equation was also studied for the signs of the trends, finding that in 51% (32) of the basins studied the signs of the trends presented values that are not consistent with the water balance equation. finally for the remaining 31 basins (with trends consistent in signs), the consistency of the water balance equation was evaluated for the trends sign and magnitude, finding closure errors that reached values up to 281% of the average of the magnitudes of the trends found on each basin.

---
# [Influencia de las tendencias de largo plazo en el balance hidrológico de la cuenca Amazónica](https://repositorio.unal.edu.co/bitstream/handle/unal/78191/1037589068.2020.pdf?sequence=11)

---
### Palabras clave: Amazonas, Balance hídrico, Tendencias, Consistencia, Rellenado de faltantes en series, Descomposición en Modos Empíricos.
---

Se estudió la consistencia de las tendencias de largo plazo en el balance hídrico de la cuenca Amazónica. Para esto se usaron series de las variables de la ecuación de balance hídrico (precipitación, evaporación, escorrentía y almacenamiento de agua en el suelo) obtenidas a partir de información de sensores remotos y estaciones de caudal (CHIRPS, ETR-Amazon, ANA-Brasil y GRACE). Las series de estudio se completaron aplicando una adaptación de la metodología propuesta por Kondrashov & Ghil (2006) para el periodo de 20 años comprendido entre febrero de 1995 y febrero de 2015. Para determinar la confiabilidad de la reconstrucción se realizó una validación del método que dio como resultado la selección de 64 cuencas de estudio de un grupo de 109 reconstruidas.

Las cuencas seleccionadas obtuvieron un desempeño aceptable en la reconstrucción de las series de al menos 3 variables para las métricas EMAR (error medio absoluto relativo), KS (prueba Kolmogorov - smirnov) y MK (Prueba Mann - Kendall). Sobre las series seleccionadas se aplicó la DME (descomposición en modos empíricos) para filtrar la variabilidad natural y aislar el residuo que representa la tendencia media de las series. Se aplicaron sobre el residuo las pruebas Mann – Kendall y Sen que determinaron el signo y la magnitud de las tendencias. No se encontró una tendencia unidireccional generalizada para la cuenca amazónica en ninguna de las variables estudiadas. Sin embargo, al realizar un análisis sobre las cuencas de las corrientes principales se encontró un comportamiento uniforme de las tendencias de cada variable para cada corriente.

También se evaluó la consistencia de la ecuación de balance hídrico general en las condiciones de corto plazo y su aproximación al largo plazo, encontrando que en el corto plazo el balance no cierra, y que en el largo plazo el error en el balance tiende asintóticamente a un valor constante, diferente de cero, lo que indica que en el periodo de 20 años estudiado sí se cumple la condición de largo plazo, pero no se encuentra tampoco un cierre en el balance de largo plazo. Se estudió también la consistencia de la ecuación de balance para los signos de las tendencias, encontrando que en el 51%(32) de las cuencas estudiadas los signos de las tendencias presentaron valores que no son consistentes con la ecuación de balance hídrico. Finalmente para las 31 cuencas restantes (de tendencias con signos consistentes) se evaluó la consistencia de la ecuación de balance hídrico para las tendencias teniendo en cuenta también la magnitud, y se encontraron errores en el cierre que alcanzaron valores de hasta el 281% del promedio de las magnitudes de las tendencias encontradas para cada cuenca.

---

Este repositorio contiene el código usado para el estudio de las tendencias de largo plazo en el balance hidrológico de la cuenca Amazónica.

Está dividido en las siguientes carpetas con el siguiente contenido:

- Formato_mdb2csv:
    Contiene los algoritmos de extracción de la información de series de tiempo de la base de datos de la ANA (Agencia Nacional de aguas del Brasil)

- Formato_rst2series:
    Contiene los algoritmos para hacer la agregación a series de tiempo de la información que originalmente se encuentra en rasters.

- Reconstruccion:
    contiene los algoritmos para la reconstrucción de las series de tiempo usando funciones ortogonales empíricas

- Tendencias:
    contiene los algoritmos para el cálculo de las tendencias de largo plazo usando la descomposición en modos empíricos y la prueba estadística Mann-Kendall

- Figuras:
    contiene los algoritmos de matplotlib con las funciones para construir los gráficos

