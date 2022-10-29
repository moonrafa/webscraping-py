from bs4 import BeautifulSoup
import requests
from pathlib2 import Path
from zipfile36 import ZipFile, ZIP_DEFLATED
from typing import Union


# 1.1 Acessar o site: https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude

# Pegar o html da página
get_html = requests.get(
    'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude').text

soup = BeautifulSoup(get_html, 'lxml')

# Filtrar o html para selecionar todas as tags <p class="callout"> </p>
anexos = soup.find_all("p", class_='callout')

# 1.2 - Baixar os Anexos I ao Anexo IV


def download_anexos(anexos):
    for anexo in anexos:
        # Filtrar para pegar apenas os anexos
        if ("Anexo" in anexo.text):
            # Selecionar as tags <a class="internal-link"> <a>
            links = anexo.find("a", class_="internal-link")
            # Pegar o link dentro do atributo href
            download = (links.get('href'))
            # Pegar o nome do arquivo
            string = anexo.text
            # Pegar a extensão do arquivo
            extension = string[string.find("(")+1:string.find(")")]
            # Selecionar apenas o nome sem a extensão
            name = string[:string.index("(")]
            # Selecionar o caminho do arquivo
            filename = Path('anexos/'f'{name}{extension}')
            print('Baixando 'f'{name}{extension}...')
            response = requests.get(download)
            # Baixar
            filename.write_bytes(response.content)
    # Zipar os arquivos apenas quando todos já estiverem baixados
    print('Arquivos baixados com sucesso... começando a compactação')
    zip_files('anexos', 'anexos.zip')

# 1.3 - Agrupar os anexos em um mesmo arquivo compactado (ZIP, RAR, ...)


def zip_files(dir: Union[Path, str], filename: Union[Path, str]):
    # Selecionar diretório a ser zipado
    dir = Path(dir)
    # Zipando cada arquivo do diretório
    with ZipFile(filename, "w", ZIP_DEFLATED) as zip_file:
        for file in dir.rglob("*"):
            zip_file.write(file, file.relative_to(dir))
    print('Arquivos compactados com sucesso!')


# Por fim chamar a função
download_anexos(anexos)
