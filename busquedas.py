from arbol import Nodo

# =====================================================
# CONEXIONES BFS y DFS
# =====================================================

conexiones_simple = {

    'Jiloyork': {'Celaya', 'CDMX', 'Querétaro'},
    'Sonora': {'Zacatecas', 'Sinaloa'},
    'Guanajuato': {'Aguascalientes'},
    'Oaxaca': {'Querétaro'},
    'Sinaloa': {'Celaya', 'Sonora', 'Jiloyork'},
    'Querétaro': {
        'Tamaulipas',
        'Zacatecas',
        'Sinaloa',
        'Jiloyork',
        'Oaxaca'
    },
    'Celaya': {'Jiloyork', 'Sinaloa'},
    'Zacatecas': {
        'Sonora',
        'Monterrey',
        'Querétaro'
    },
    'Monterrey': {
        'Zacatecas',
        'Sinaloa'
    },
    'Tamaulipas': {'Querétaro'}
}

# =====================================================
# CONEXIONES UCS
# =====================================================

conexiones_ucs = {

    'Jiloyork': {
        'CDMX': 125,
        'Queretaro': 513
    },

    'Morelos': {
        'Queretaro': 524
    },

    'CDMX': {
        'Jiloyork': 125,
        'Queretaro': 423,
        'Hidalgo': 491
    },

    'Hidalgo': {
        'CDMX': 491,
        'Queretaro': 456,
        'Mexicali': 309,
        'Monterrey': 346
    },

    'Queretaro': {

        'San Luis Potosi': 203,
        'Morelos': 514,
        'Jiloyork': 513,
        'CDMX': 423,
        'Monterrey': 603,
        'Sonora': 437,
        'Hidalgo': 356,
        'Mexicali': 313,
        'Aguascalientes': 599
    },

    'San Luis Potosi': {
        'Queretaro': 203,
        'Aguascalientes': 390
    },

    'Aguascalientes': {
        'San Luis Potosi': 390,
        'Queretaro': 599
    },

    'Sonora': {
        'Queretaro': 437,
        'Mexicali': 394
    },

    'Mexicali': {
        'Monterrey': 296,
        'Hidalgo': 309,
        'Queretaro': 313
    },

    'Monterrey': {
        'Hidalgo': 346,
        'Queretaro': 603,
        'Mexicali': 296
    }
}

# =====================================================
# BFS
# =====================================================

def buscar_solucion_BFS(conexiones, estado_inicial, solucion):

    nodos_visitados = []
    nodos_frontera = []

    nodo_inicial = Nodo(estado_inicial)

    nodos_frontera.append(nodo_inicial)

    while len(nodos_frontera) != 0:

        nodo = nodos_frontera.pop(0)

        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()

        lista_hijos = []

        for un_hijo in conexiones.get(dato_nodo, []):

            hijo = Nodo(un_hijo)

            hijo.set_padre(nodo)

            lista_hijos.append(hijo)

            if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):

                nodos_frontera.append(hijo)

        nodo.set_hijos(lista_hijos)

    return None

# =====================================================
# UCS
# =====================================================

def buscar_solucion_UCS(conexiones, estado_inicial, solucion):

    nodos_visitados = []
    nodos_frontera = []

    nodo_inicial = Nodo(estado_inicial)

    nodo_inicial.set_costo(0)

    nodos_frontera.append(nodo_inicial)

    while len(nodos_frontera) != 0:

        nodos_frontera = sorted(
            nodos_frontera,
            key=lambda x: x.get_costo()
        )

        nodo = nodos_frontera.pop(0)

        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()

        lista_hijos = []

        for un_hijo in conexiones[dato_nodo]:

            hijo = Nodo(un_hijo)

            costo = conexiones[dato_nodo][un_hijo]

            hijo.set_costo(
                nodo.get_costo() + costo
            )

            hijo.set_padre(nodo)

            lista_hijos.append(hijo)

            if not hijo.en_lista(nodos_visitados):

                if hijo.en_lista(nodos_frontera):

                    for n in nodos_frontera:

                        if n.igual(hijo) and n.get_costo() > hijo.get_costo():

                            nodos_frontera.remove(n)
                            nodos_frontera.append(hijo)

                else:
                    nodos_frontera.append(hijo)

        nodo.set_hijos(lista_hijos)

    return None

# =====================================================
# DFS PROFUNDIDAD ITERATIVA
# =====================================================

def DFS_profundidad_iterativa(nodo, solucion):

    for limite in range(0, 100):

        visitados = []

        sol = buscar_solucion_DFS_Rec(
            nodo,
            solucion,
            visitados,
            limite
        )

        if sol is not None:
            return sol

    return None

def buscar_solucion_DFS_Rec(
    nodo,
    solucion,
    visitados,
    limite
):

    if nodo.get_datos() == solucion:
        return nodo

    if limite == 0:
        return None

    visitados.append(nodo.get_datos())

    dato_nodo = nodo.get_datos()

    lista_hijos = []

    if dato_nodo in conexiones_simple:

        for un_hijo in conexiones_simple[dato_nodo]:

            if un_hijo not in visitados:

                hijo = Nodo(un_hijo)

                hijo.set_padre(nodo)

                lista_hijos.append(hijo)

    nodo.set_hijos(lista_hijos)

    for nodo_hijo in nodo.get_hijos():

        sol = buscar_solucion_DFS_Rec(
            nodo_hijo,
            solucion,
            visitados,
            limite - 1
        )

        if sol is not None:
            return sol

    return None