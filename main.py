import pickle
import io
import os
from envio import Envio

ARCHIVO_BINARIO = "envios.bin"
ARCHIVO_CSV = "prueba.csv"

def crear_binario():
    if os.path.exists(ARCHIVO_BINARIO):
        conf = input("¿Está seguro que desea crear el archivo de nuevo? (s. Si - n. No): ")
        if conf.lower() != "s":
            print("Operacion cancelada.")
            return
    
    csv = open(ARCHIVO_CSV, "rt")
    control = csv.readline()
    encabezado = csv.readline()
    binaryFile = open(ARCHIVO_BINARIO, "wb")
    
    for linea in csv:
        datos = linea.strip().split(",")
        envio = Envio(datos[0], datos[1], datos[2], datos[3])
        pickle.dump(envio, binaryFile)
        
    binaryFile.close()
    csv.close()
    
    print("El archivo fue creado correctamente. \n")
    return


def crear_nuevo_envio():
    codigo_postal = input("Ingrese el código postal: ")
    direccion = input("Ingrese la dirección: ")
    tipo_envio = int(input("Ingrese el tipo de envío (0-6): "))
    if tipo_envio < 0 or tipo_envio > 6:
        tipo_envio = int(input('Ingrese un tipo válido.')) 
    forma_pago = int(input("Ingrese la forma de pago (1: efectivo, 2: tarjeta de crédito): "))
    while forma_pago != 1 and forma_pago != 2:
        forma_pago = int(input('Ingrese una forma de pago válida.'))
    nuevo_envio = Envio(codigo_postal, direccion, tipo_envio, forma_pago)
    while not os.path.exists(ARCHIVO_BINARIO):
        print('Debe crear el archivo binario.')
        return
    arch_bin = open(ARCHIVO_BINARIO, 'ab')
    pickle.dump(nuevo_envio, arch_bin)
    arch_bin.close()


def mostrar_todos():
    pais_destino = None
    if not os.path.exists(ARCHIVO_BINARIO):
        print("No existe el archivo binario.")
        return
    bin_file = open(ARCHIVO_BINARIO, "rb")
    t = os.path.getsize(ARCHIVO_BINARIO)
    while bin_file.tell() < t:
        envio = pickle.load(bin_file)
        pais_destino = envio.obtener_pais_destino()
        print(envio, 'Pais de destino: ', pais_destino)
        pais_destino = None
    bin_file.close()
    return

    
def buscar_por_cp():
    if not os.path.exists(ARCHIVO_BINARIO):
        print("No existe el archivo binario.")
        return
    cp = input("Ingrese el código postal: ")
    bin_file = open(ARCHIVO_BINARIO, "rb")
    t = os.path.getsize(ARCHIVO_BINARIO)
    while bin_file.tell() < t:
        envio = pickle.load(bin_file)
        if envio.codigo_postal == cp:
            print(envio)
    bin_file.close()
    return

def buscar_por_direccion():
    if not os.path.exists(ARCHIVO_BINARIO):
        print("No existe el archivo binario.")
        return
    d = input("Ingrese la dirección: ")
    bin_file = open(ARCHIVO_BINARIO, "rb")
    t = os.path.getsize(ARCHIVO_BINARIO)
    while bin_file.tell() < t:
        envio = pickle.load(bin_file)
        if envio.direccion == d:
            print(envio)
            break
    bin_file.close()
    return

def cant_por_combinacion(Arch_bin):
    mat = [[0]*7 for i in range(2)]
    for i in range(len(mat)):
        fila = mat[i].tipo - 1
        col = mat[i].calificacion
        mat[fila][col] += mat[i].reproducciones
    return mat



def mostrar_arreglo_promedios():
    if not os.path.exists(ARCHIVO_BINARIO):
        print("No existe el archivo binario.")
        return
    d = input("Ingrese la dirección: ")
    bin_file = open(ARCHIVO_BINARIO, "rb")
    t = os.path.getsize(ARCHIVO_BINARIO)
    while bin_file.tell() < t:
        envio = pickle.load(bin_file)
        if envio.direccion == d:
            print(envio)
            break
    bin_file.close()
    return

def mostar_arreglo_promedios():
    if not os.path.exists(ARCHIVO_BINARIO):
        print("No existe el archivo binario.")
        return
    
    bin_file = open(ARCHIVO_BINARIO, "rb")
    size = os.path.getsize(ARCHIVO_BINARIO)
    bin_file.seek(0, io.SEEK_SET)
    
    arreglo = []
    promedio = 0
    cant = 0
    
    while bin_file.tell() < size:
        envio = pickle.load(bin_file)
        promedio += envio.obtener_importe_final()
        cant += 1

    if cant != 0:
        promedio //= cant
    print("Promedio total:", promedio)
    
    bin_file.seek(0, io.SEEK_SET)
    while bin_file.tell() < size:
        envio = pickle.load(bin_file)
        if envio.obtener_importe_final() > promedio:
            arreglo.append(envio)
    bin_file.close()
    
    for env in arreglo:
        print(env)
    
    ### FALTA ORDENAR EL ARREGLO
    return

def main():
    opcion = -1
    while opcion != "0":
        print("1. Crear archivo binario")
        print("2. Cargar envio manualmente")
        print("3. Mostrar los datos de todos los envíos del archivo binario")
        print("4. Buscar y mostrar los datos de todos los envíos cuyo código postal sea igual a x")
        print("5. Buscar un envío por su dirección")
        print("6. Mostrar la cantidad de envíos de cada combinación posible entre tipo de envío y forma de pago")
        print("7. Mostrar la cantidad total de envíos contados por cada tipo de envío posible," + 
              " y la cantidad total de envíos contados por cada  forma de pago posible")
        print("8. Calcular el importe promedio pagado entre todos los envíos que figuran en el archivo")
        print("0. Salir del programa")
        print()
        opcion = input("Ingrese el numero de opcion: ")
        
        if not opcion in "012345678":
            print("Ingrese una opción válida")
            continue
        
        if opcion == "0":
            print("Saliendo del programa...")
            return
        
        if opcion == "1":
            crear_binario()
        if opcion == "2":
            crear_nuevo_envio()
        
        if opcion == "3":
            mostrar_todos()
        
        if opcion == "4":
            buscar_por_cp()
            
        if opcion == "5":
            buscar_por_direccion()
            
        if opcion == "6":
            pass
        
        if opcion == "7":
            pass
        
        if opcion == "8":
            mostar_arreglo_promedios()
    return

if __name__ == "__main__":
    main()