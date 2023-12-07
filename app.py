from pywebio.input import *
from pywebio.output import *
from pymongo import MongoClient
from pywebio import start_server


connection_string = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.0"
client = MongoClient(connection_string)
db = client["sample_mflix"]
colecao = db["movies"]

def main ( ):
    pegar_input()

def pegar_input ( ):
    generos = colecao.distinct("genres")
    genero = select("generos: ", generos)
    mostrar_filmes(genero)


def mostrar_filmes(genero):
    filmes = colecao.find({"genres": genero})
    for index, filme in enumerate(filmes):
        put_text(index, ' - ', filme['title'])

if __name__ == '__main__':
    start_server(main, port=8080, auto_open_webbrowser=True)
