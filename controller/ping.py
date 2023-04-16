import threading
import subprocess

def ping_host(host):
    """Функция для выполнения пингования одного IP-адреса."""
    try:
        # Выполняем пинг и ждем до 1 секунды на каждый пинг
        subprocess.check_output(["ping", "-n", "1", "-w", "1", host])
        return True  # IP-адрес доступен
    except subprocess.CalledProcessError:
        return False  # IP-адрес не доступен

def ping_hosts(hosts):
    """Функция для выполнения пингования списка IP-адресов в отдельных потоках."""
    results = {}
    threads = []
    for host in hosts:
        # Создаем отдельный поток для выполнения пингования
        t = threading.Thread(target=lambda: results.update({host: ping_host(host)}))
        t.start()
        threads.append(t)

    # Ожидаем завершения всех потоков
    for t in threads:
        t.join()

    return results

# Список IP-адресов для пингования
hosts_list = ["youtube.com", "fwfasd.ru", "192.100.0.3"]



while True:
# Вызываем функцию для выполнения пингования и получения результатов
    ping_results = ping_hosts(hosts_list)

    # Выводим результаты пингования
    for host, status in ping_results.items():
        if status:
            print(f"IP-адрес {host} доступен.")
        else:
            print(f"IP-адрес {host} недоступен.")
