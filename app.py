from flask import Flask, render_template, request

from busquedas import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def inicio():

    resultados = None

    if request.method == "POST":

        inicio_ciudad = request.form["inicio"].strip()

        destino_ciudad = request.form["destino"].strip()

        # =================================================
        # BFS
        # =================================================

        nodo_bfs = buscar_solucion_BFS(
            conexiones_simple,
            inicio_ciudad,
            destino_ciudad
        )

        resultado_bfs = []

        if nodo_bfs:

            while nodo_bfs:

                resultado_bfs.append(
                    nodo_bfs.get_datos()
                )

                nodo_bfs = nodo_bfs.get_padre()

            resultado_bfs.reverse()

        # =================================================
        # UCS
        # =================================================

        resultado_ucs = []
        costo_ucs = 0

        if inicio_ciudad in conexiones_ucs:

            nodo_ucs = buscar_solucion_UCS(
                conexiones_ucs,
                inicio_ciudad,
                destino_ciudad
            )

            if nodo_ucs:

                costo_ucs = nodo_ucs.get_costo()

                while nodo_ucs:

                    resultado_ucs.append(
                        nodo_ucs.get_datos()
                    )

                    nodo_ucs = nodo_ucs.get_padre()

                resultado_ucs.reverse()

        # =================================================
        # DFS ITERATIVO
        # =================================================

        nodo_inicial = Nodo(inicio_ciudad)

        nodo_dfs = DFS_profundidad_iterativa(
            nodo_inicial,
            destino_ciudad
        )

        resultado_dfs = []

        if nodo_dfs:

            while nodo_dfs:

                resultado_dfs.append(
                    nodo_dfs.get_datos()
                )

                nodo_dfs = nodo_dfs.get_padre()

            resultado_dfs.reverse()

        resultados = {

            "bfs": resultado_bfs,

            "dfs": resultado_dfs,

            "ucs": f"{resultado_ucs} | Costo: {costo_ucs}"
        }

    return render_template(
        "index.html",
        resultados=resultados
    )

if __name__ == "__main__":
    app.run(debug=True)