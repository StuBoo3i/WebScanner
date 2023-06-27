from Web_Vulnerablility.burteforce.main import check_burtforce
from Web_Vulnerablility.CSRF.Get import check_csrf_vulnerabilities
from Web_Vulnerablility.file_inclusion.main import check_file_inclusion
from Web_Vulnerablility.PHP.PHP_Deserialization import PHP_Dvul
from Web_Vulnerablility.RCE.main import check_rce_vulnerabilities
from Web_Vulnerablility.SQLinject.wgdscan import main
from Web_Vulnerablility.XSS.main import check_xss_vulnerabilities
from Web_Vulnerablility.dir_list.dir_list import check_directory_traversal
from Web_Vulnerablility.file_upanddown.main import check_file_vulnerabilities
from Web_Vulnerablility.reptile.web_crawler import spider2_content


#合并列表
def merge_results(list1, list2):
    merged_results = {}

    for url, result in list1 + list2:
        if url in merged_results:
            merged_results[url] += ", " + result
        else:
            merged_results[url] = result

    merged_list = [[url, result] for url, result in merged_results.items()]
    return merged_list


def run_detection(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测暴力破解漏洞
        burtforce_result = check_burtforce(url)
        if burtforce_result:
            result_str += "暴力破解漏洞:" + burtforce_result
            print(result_str)

        # 检测CSRF漏洞
        csrf_result = check_csrf_vulnerabilities(url)
        if csrf_result:
            result_str += "CSRF漏洞:" + csrf_result
            print(result_str)

        # 检测文件包含漏洞
        file_inclusion_result = check_file_inclusion(url)
        if file_inclusion_result:
            result_str += "文件包含漏洞:" + file_inclusion_result
            print(result_str)

        # 检测PHP反序列化漏洞
        php_deserialization_result = PHP_Dvul(url)
        if php_deserialization_result:
            result_str += "PHP反序列化漏洞:" + php_deserialization_result
            print(result_str)

        # 检测远程代码执行漏洞
        rce_result = check_rce_vulnerabilities(url)
        if rce_result:
            result_str += "远程代码执行漏洞:" + rce_result
            print(result_str)


        # 检测XSS漏洞
        xss_result = check_xss_vulnerabilities(url)
        if xss_result:
            result_str += "XSS漏洞:" + xss_result
            print(result_str)

        # 检测目录遍历漏洞
        directory_traversal_result = check_directory_traversal(url)
        if directory_traversal_result:
            result_str += "目录遍历漏洞:" + directory_traversal_result
            print(result_str)

        # 检测文件上传和下载漏洞
        file_vulnerabilities_result = check_file_vulnerabilities(url)
        if file_vulnerabilities_result:
            result_str += "文件上传和下载漏洞:" + file_vulnerabilities_result
            print(result_str)
        if result_str:
            results.append([url, result_str.strip()])
            print([url, result_str])
    results_other = main(url)
    print(results)
    print(results_other)
    results = merge_results(results, results_other)
    return results


def perform_xss_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测XSS漏洞
        xss_result = check_xss_vulnerabilities(url)
        if xss_result:
            result_str += "XSS漏洞:" + xss_result

        if result_str:
            results.append([url, result_str.strip()])

    return results


def perform_brute_force_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测暴力破解漏洞
        burtforce_result = check_burtforce(url)
        if burtforce_result:
            result_str += "暴力破解漏洞:" + burtforce_result

        if result_str:
            results.append([url, result_str.strip()])

    return results


def perform_remote_code_execution_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测远程代码执行漏洞
        rce_result = check_rce_vulnerabilities(url)
        if rce_result:
            result_str += "远程代码执行漏洞:" + rce_result

        if result_str:
            results.append([url, result_str.strip()])

    return results


def perform_file_vulnerability_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测文件上传和下载漏洞
        file_vulnerabilities_result = check_file_vulnerabilities(url)
        if file_vulnerabilities_result:
            result_str += "文件上传和下载漏洞:" + file_vulnerabilities_result
        # 检测文件包含漏洞
        file_inclusion_result = check_file_inclusion(url)
        if file_inclusion_result:
            result_str += "文件包含漏洞:" + file_inclusion_result

        if result_str:
            results.append([url, result_str.strip()])

    return results


def scan_choose(url, scan_mode):
    if scan_mode == "quick":
        return run_detection(url)
    elif scan_mode == "full":
        return run_detection(url)
    elif scan_mode == "sql_injection":
        return main(url)
    elif scan_mode == "xss":
        return perform_xss_scan(url)
    elif scan_mode == "brute_force":
        return perform_brute_force_scan(url)
    elif scan_mode == "remote_code_execution":
        return perform_remote_code_execution_scan(url)
    elif scan_mode == "file_vulnerability":
        return perform_file_vulnerability_scan(url)
    else:
        return "无效的扫描模式"


def write_list_to_file(file_path, data_list):
    with open(file_path, 'w') as file:
        for item in data_list:
            file.write(str(item) + '\n')


def scan(url, scan_mode):
    # url = 'http://192.168.1.192:8086/pikachu/'
    # scan_mode = 'full'

    result = scan_choose(url, scan_mode)
    print(result)
    # result_str1 = ['http://192.168.1.192:8086/pikachu/xss_stored.php?id=3834', '暴力破解漏洞:表单暴力破解漏洞文件包含漏洞:远程文件包含漏洞']
    # result_str2 = ['http://192.168.1.192:8086/pikachu/xss_stored.php?id=3830', '暴力破解漏洞:表单暴力破解漏洞文件包含漏洞:远程文件包含漏洞']
    # result = []
    # result.append(result_str1)
    # result.append(result_str2)

    write_list_to_file('result.txt', result)

