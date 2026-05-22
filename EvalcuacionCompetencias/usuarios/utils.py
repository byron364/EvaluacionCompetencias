def calcular_nota(
    test,
    respuestas_correctas
):

    total_preguntas = (
        test.preguntas.count()
    )

    if total_preguntas == 0:

        return 0

    valor_pregunta = (

        test.puntaje_maximo
        / total_preguntas

    )

    nota = (

        respuestas_correctas
        * valor_pregunta

    )

    return round(
        nota,
        2
    )