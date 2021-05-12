# TCP File Transfer

## Descripción :book:

Trabajo Práctico número 1 de la materia **Introducción a los Sistemas Distribuidos** (75.43), dictada en la Facultad de Ingeniería de la Universidad de Buenos Aires.

## Integrantes :busts_in_silhouette:

| Nombre | Apellido | Padrón | Mail                |
| ------ | -------- | ------ | ------------------- |
| Mauro  | Parafati | 102749 | mparafati@fi.uba.ar |
| Taiel | Colavecchia | 102510 | tcolavecchia@fi.uba.ar |
| Yuhong | Huang | 102146 | yhuang@fi.uba.ar |

## Requisitos :ballot_box_with_check:

Se listan a continuación los requisitos necesarios para poder correr el proyecto:

-   [Python3](https://www.python.org/downloads/)

## Uso :computer:

Se detalla a continuación una breve explicación para correr el programa:

### Servidor

El servidor consta de un sólo comando `start-server`, que permite iniciar el servidor. Para ejecutarlo, o bien se puede optar por:

```bash
./start-server [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]
```

Para lo cual podría ser necesario darle permisos de ejecución al script (`chmod +x ./start-server`), o bien por la segunda opción:

```bash
python3 start-server [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]
```

Pueden utilizarse distintos flags:

* [`-h` o `--help`] permite mostrar el mensaje de ayuda y detalle de los distintos flags.
* [`-v` o `--verbose` | `-q` o `--quiet`] maneja el nivel de profundidad del logging.
* [`-H` o `--host`] permite indicar el host donde se quiere levantar el servidor.
* [`-p` o `--port`] permite indicar el puerto donde se quiere levantar el servidor.
* [`-s` o `--storage`] permite indicar el directorio donde se quieren bajar los archivos.

### Cliente

El cliente cuenta con tres comandos distintos:
* `list-files`: permite descargar la lista de archivos disponibles en el servidor.
* `upload-file`: permite subir un archivo al servidor.
* `download-file`: permite descargar un archivo del servidor.
