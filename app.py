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
   
    for filme in filmes:
        titulos = filme['title']
        plot = filme.get('plot', 'Plot não disponível')[:100] + "..."
        
        put_html(f'''
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #ddd;">
                <div style="display: flex; align-items: center;">
                    <div style="flex: 2; padding-left: 10px;">
                        <p>{plot}</p>
                    </div>
                </div>
            </div>
        ''')
        put_buttons([titulos], onclick=lambda titulos=titulos: detalhes_filme(titulos))


def detalhes_filme(filme):
    clear()

    resultado = colecao.find_one({'title': filme})
    # nome = resultado.get('name', 'Nome não disponível')
    nome = resultado.get('title', 'Nome não disponível')
    generos = resultado.get('genres', [])
    diretores = resultado.get('directors', [])
    ano = resultado.get('year', 'Ano não disponível')
    poster = resultado.get('poster', 'Poster não disponível')
    plot = resultado.get('plot', 'Plot não disponível')

    
    put_text(f'Nome: {nome}')
    put_text(f'Ano: {ano}')
    put_text(f'Generos: {generos}')
    put_text(f'Diretores: {diretores}')
    put_text(f'Plot: {plot}')
    put_image(poster)


if __name__ == '__main__':
    start_server(main, port=8080, auto_open_webbrowser=True)
