import ast

def writeAnswer(answer: list[ tuple ]):
    with open('answer.txt', 'w') as f:
        
        data = str(answer)
        
        f.write(data + '\n')

def readAnswer():
    with open('answer.txt', 'r') as archivo:
        contenido = archivo.readline()
    lista_de_tuplas = ast.literal_eval(contenido)
    return lista_de_tuplas