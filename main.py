import requests


class YaUploader:
    
    def __init__(self, token: str):
        self.token = token


    def get_headers(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f"OAuth {self.token}"
        }
        return headers


    def _get_link(self, file_path):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": file_path, 'overwrite': 'true'}
        response = requests.get(url=url, params=params, headers=headers)
        response_json = response.json()
        link = dict(response_json)['href']
        return link


    def _get_file_name(self, file_path: str) -> str:
        return file_path.split("\\")[-1]


    def upload(self, file_path: str):
        try:
            file_name = self._get_file_name(file_path)
            link = self._get_link(file_name)
            with open(file_path, 'rb') as file:
                response = requests.put(url=link, data=file)
            response.raise_for_status()
            if response.status_code == 201:
                print("Загружено")
        except:
            print("Ошибка")


if __name__ == '__main__':
    token = input("Введите токен: ")
    path_to_file = input("Введите путь к файлу: ")
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)