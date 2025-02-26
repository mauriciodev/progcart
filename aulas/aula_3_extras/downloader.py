import requests
import os

class Downloader:
    def __init__(self, server_url_format, destination_folder):
        self.server_url_format = server_url_format
        self.destination_folder = destination_folder
        #verifica se a pasta existe, se não existe, cria.
        os.makedirs(self.destination_folder, exist_ok=True)
    
    def download_file(self, name):
        url = self.server_url_format.format(name)
        response = requests.get(url)
        file_Path = f'{self.destination_folder}/{name}.zip'

        if response.status_code == 200:
            with open(file_Path, 'wb') as file:
                file.write(response.content)
            print('File downloaded successfully')
        else:
            print('Failed to download file')

obj_teste = Downloader( \
    "https://geoftp.ibge.gov.br/cartas_e_mapas/folhas_topograficas/vetoriais/escala_1000mil/shapefile/{}.zip", \
    "/home/mauricio/Desktop/progcart/aulas" )

print(dir(obj_teste))

obj_teste.download_file("g04_na19")