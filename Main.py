'''
    Eder Abraham Sampayo Gonzalez
    miércoles, 29 de abril de 2026
    Declaro que el presente código es de mi autoría y ha
    sido desarrollado bajo los criterios de integridad académica de la FCFM.
'''
'''
    LIBRERIAS USADAS:
    - matplotlib: Configuración de gráficas.
    - Networkx: Creación y manipulación de grafos, cálculo de árboles de expansión mínima. 
    SE NECESITAN INSTALAR ESTAS LIBRERIAS PARA EJECUTAR EL CODIGO

    EJECUTAR LOS SIGUIENTES COMANDOS EN LA TERMINAL PARA INSTALAR LAS LIBRERIAS:
    pip install networkx
    pip install matplotlib
'''


# Importar librerias necesarias
import networkx as nx
import matplotlib.pyplot as plt

'''
Conjunto de datos que guarda información de las conexiones del parque industrial
Lista de diccionarios, cada diccionario representa una conexión entre dos nodos
Cada diccionario tiene las siguientes claves:
- 'nodos': tupla con los nodos de la conexión (nodo1, nodo2)
- 'distancia': distancia entre los nodos
- 'penalizaciones': LISTA penalizaciones asociadas a la conexión
'''
Arbol = [
    {'nodos': ('ADMIN1', 'ADMIN2'), 'distancia': 161, 'penalizaciones': []},
    {'nodos': ('ADMIN1', 'P2'), 'distancia': 383, 'penalizaciones': ['C']},

    {'nodos': ('ADMIN2', 'P1'), 'distancia': 267, 'penalizaciones': ['C']},
    {'nodos': ('ADMIN2', 'P3'), 'distancia': 181, 'penalizaciones': ['C']},
    {'nodos': ('ADMIN2', 'A2'), 'distancia': 283, 'penalizaciones': ['P', 'C']},

    {'nodos': ('P1', 'P2'), 'distancia': 88, 'penalizaciones': []},
    {'nodos': ('P1', 'P3'), 'distancia': 65, 'penalizaciones': []},

    {'nodos': ('P3', 'A1'), 'distancia': 193, 'penalizaciones': ['P', 'C']},
    {'nodos': ('P3', 'A1'), 'distancia': 469, 'penalizaciones': []},

    {'nodos': ('A1', 'A2'), 'distancia': 136, 'penalizaciones': []},
    {'nodos': ('A1', 'SE'), 'distancia': 258, 'penalizaciones': ['A']},

    {'nodos': ('A2', 'S1'), 'distancia': 338, 'penalizaciones': ['A']},
    {'nodos': ('A2', 'V1'), 'distancia': 301, 'penalizaciones': ['P','C']},

    {'nodos': ('V1', 'S1'), 'distancia': 194, 'penalizaciones': []},

    {'nodos': ('S1', 'SE'), 'distancia': 112, 'penalizaciones': ['C']},
    {'nodos': ('S1', 'A3'), 'distancia': 138, 'penalizaciones': ['P']},

    {'nodos': ('A3', 'SE'), 'distancia': 163, 'penalizaciones': ['P']},
]


def calcular_costo(conexion):
    '''
    Función para calcular el costo de una conexión.

    El costo se calcula como la distancia multiplicada por el costo base y las penalizaciones.
    
    Parámetros:
    - conexion: diccionario con la información de la conexión
    Retorna:
    - costo_total: costo total de la conexión
    '''
    costo_base = 50  # Costo base por unidad de distancia
    multiplicador_penalizaciones = {
        'A': 10.0, # Penalización por afectación CFE
        'P': 2.5,  # Penalización por zona de carga pesada
        'C': 2.0   # Penalización por construcción en carretera
    }

    distancia = conexion['distancia']
    penalizaciones = conexion['penalizaciones']

    costo_total = distancia * costo_base

    for penalizacion in penalizaciones:
        if penalizacion in multiplicador_penalizaciones:
            costo_total *= multiplicador_penalizaciones[penalizacion]

    return costo_total


def agregar_nodos(G, Arbol):
    '''
    Función para agregar los nodos al grafo.

    Recorre el conjunto de datos Arbol y agrega los nodos al grafo G
    Calcula el costo de cada conexión con la distancia y las penalizaciones asociadas.
    
    Parámetros:
    - G: grafo de NetworkX al que se agregarán los nodos
    - Arbol: conjunto de datos con las conexiones del parque industrial
    '''

    for conexion in Arbol:
        tupla = conexion['nodos']
        costo = calcular_costo(conexion)
        G.add_edge(*tupla, weight=costo) #Agrega la conexión al grafo con el costo calculado como peso
        # print(f"Agregando nodos: {tupla[0]}, {tupla[1]}, con costo: {costo}")


if __name__ == "__main__":
    # Crear un multigrafo no dirigido
    # (necesario para manejarlas multiples conexiones entre P3 y A1)
    G = nx.MultiGraph()

    # Agregar los nodos al grafo utilizando el conjunto de datos Arbol
    agregar_nodos(G, Arbol)

    # Calcular el arbol de expansión mínima utilizando el algoritmo de kruskal
    arbol_expansion_minima = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')

    # Imprimir las conexiones resultantes del arbol de expansión mínima con su costo
    print("Árbol de Expansión Mínima:")
    for edge in arbol_expansion_minima.edges(data=True):
        print(edge[0], "\t-->\t", edge[1], "\tcon costo:", edge[2]['weight'])

    # Calcular el costo total del arbol de expansión mínima
    costo_total = sum(edge[2]['weight'] for edge in arbol_expansion_minima.edges(data=True))
    print("Costo total del árbol de expansión mínima: ", costo_total, "pesos")


    # Dibujar el árbol de expansión mínima
    plt.figure(figsize=(12, 6))
    plt.title("Conexiones del Parque Industrial - Árbol de Expansión Mínima")
    pos = {'ADMIN2': (114, 28), 'ADMIN1': (141, 30), 'P1': (106, 64), 'P2': (122, 76), 'P3': (91, 46),
           'A1': (67, 40), 'A2': (74, 18), 'S1': (37, 14), 'V1': (58, -5), 'A3': (15, 18), 'SE': (33, 40)}
    nx.draw(arbol_expansion_minima,
            with_labels=True, pos=pos,
            node_color='lightblue',
            edge_color='black',
            node_size=2200,
            width=3)
    edge_labels = nx.get_edge_attributes(arbol_expansion_minima, 'weight')
    nx.draw_networkx_edge_labels(arbol_expansion_minima,
                                pos=pos,
                                edge_labels=edge_labels,
                                font_size=7)
    plt.show()

    '''# dibujar el grafo original
    plt.figure(figsize=(12, 6))
    pos = {'ADMIN2': (114, 28), 'ADMIN1': (141, 30), 'P1': (106, 64), 'P2': (122, 76), 'P3': (91, 46),
           'A1': (67, 40), 'A2': (74, 18), 'S1': (37, 14), 'V1': (58, -5), 'A3': (15, 18), 'SE': (33, 40)}
    nx.draw(G,
            with_labels=True, pos=pos,
            node_color='lightblue',
            edge_color='black',
            node_size=2200,
            width=3,
            connectionstyle='arc3,rad=0.1')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.show()'''