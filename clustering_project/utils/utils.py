import os
import re

REGEX_PATH_FILE = "./data/headers.txt"

def load_header_patterns():
    """
    Carga las expresiones regulares desde un archivo y crea un patrón combinado.

    Returns:
        re.Pattern: Objeto de expresión regular para identificar encabezados en
        los archivos.
    """

    with open(REGEX_PATH_FILE, "r") as file:
        headers = [line.strip() for line in file if line.strip()]
    
    return re.compile(r"^(" + "|".join(headers) + r").*$")


def process_headers(input_directory, output_directory):
    """
    Procesa la estructura de directorios donde se encuentran los ficheros. Para
    cada fichero se invoca a la función que se encarga de eliminar los
    encabezados.

    Args:
        input_directory (str): Ruta del directorio de entrada que contiene los
        archivos organizados en subdirectorios.

        output_directory (str): Ruta del directorio de salida donde se guardarán
        los archivos procesados.
    """

    header_regex = load_header_patterns()
    
    for directory in os.listdir(input_directory):
        subdirectory = os.path.join(input_directory, directory)
        if os.path.isdir(subdirectory):
            files = os.listdir(subdirectory)
            for filename in files:
                process_file(input_file= os.path.join(subdirectory, filename),
                             output_file= os.path.join(output_directory,
                                                       filename),
                             header_regex=header_regex)


def process_file(input_file, output_file, header_regex):
    """
    Procesa un archivo eliminando encabezados (basádose en un patrón de
    expresión regular) y elimina tanto las líneas de encabezado como las líneas
    continuadas (aquellas que comienzan con espacio o tabulación) asociadas a
    dichos encabezados. El contenido filtrado se escribe en un archivo de salida.

    Args:
        input_file (str): Ruta del archivo de entrada a procesar.

        output_file (str): Ruta del archivo de salida donde se guardará el
        contenido filtrado.

        header_regex (re.Pattern): Objeto de expresión regular que identifica
        líneas de encabezado.
    """
    
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        header_detected = False
        for line in infile:
            if header_regex.match(line):
                header_detected = True
            elif not (header_detected and re.compile(r"^[ \t]").match(line)):
                header_detected = False
                outfile.write(line)