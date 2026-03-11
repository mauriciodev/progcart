import requests, os 
from owslib import csw

class Downloader:
    def __init__(self, server_url_format, destination_folder):
        # Inicialização dos atributos da classe
        self.server_url_format = server_url_format
        self.destination_folder = destination_folder
        #verifica se a pasta existe, se não existe, cria.
        os.makedirs(self.destination_folder, exist_ok=True)

    def download_file(self, name):
        # Esta não é a melhor forma de fazer isso. É um exemplo.
        url = self.server_url_format.format(name)
        response = requests.get(url)
        file_Path = f'{self.destination_folder}/{name}.zip'
    
        if response.status_code == 200:
            with open(file_Path, 'wb') as file:
                file.write(response.content)
                print('File downloaded successfully')
        else:
            print('Failed to download file')

    def download_bdgex(self, uuid):
        # BDGEx anonymous login
        session = requests.Session()
        resp1 = session.get(
            "https://bdgex.eb.mil.br/mediador/?modulo=Login&acao=VisitanteExterno"
        )
        done = 0
        file_url = self.get_bdgex_download_link(uuid)
        resp = session.get(file_url, stream=True)
        tif_file_name = f"{uuid}.tif"
        if resp.status_code == 200:
            with open(tif_file_name, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

    """ Get the download URL from BDGEx for a product with metadata id uuid. """
    def get_bdgex_download_link_filename(self, uuid):
        """cswClient = csw.CatalogueServiceWeb("http://bdgex.eb.mil.br/csw")
        cswClient.getrecordbyid(id=[uuid])
        if len(cswClient.records)>0:
            metadata = cswClient.records[uuid]
            file_url = f"https://bdgex.eb.mil.br/mediador/index.php?modulo=download&acao=baixar&identificador={metadata.identifier}"
        else:
            file_url = "None"
        """
        file_url = f"https://bdgex.eb.mil.br/mediador/index.php?modulo=download&acao=baixar&identificador={uuid}"
        return file_url, filename

    def list_bdgex_uuids(search_string):
        

        # BDGEx anonymous login
        session = requests.Session()
        session.post(
            "https://bdgex.eb.mil.br/mediador/?modulo=Login&acao=VisitanteExterno"
        )
        done = 0




# Esta parte do código só será executada se este for o arquivo principal.
# Ou seja: python downloader.py
if __name__=="__main__": 
    # Cria o objeto da classe Downloader
    obj_teste = Downloader( \
    "https://geoftp.ibge.gov.br/cartas_e_mapas/folhas_topograficas/vetoriais/escala_1000mil/shapefile/{}.zip", \
    "/home/mauricio/Desktop/progcart/pixi_env/" )
    
    # Lista os atributos e métodos do objeto.
    print(dir(obj_teste))
    
    # Chama uma função do objeto criado.
    #obj_teste.download_file("g04_na19")

    test_uuid = "ce253e42-c7e7-11df-94c5-00270e07db9f"
    # test bdgex urls from csw
    print( obj_teste.get_bdgex_download_link(test_uuid))
    obj_teste.download_bdgex(test_uuid)
