import re
import subprocess


def ping_host(host):
    """Функция для выполнения пингования одного IP-адреса."""
    try:
        output = subprocess.check_output(["ping", "-n", "2", "-w", "4", host]).decode('cp866')
        ping = re.findall(r'\d+\.*\d*', output)[-1]
        return {'status': True, 'ping': ping + ' ms'}  # IP-адрес доступен, возвращаем размер пинга
    except subprocess.CalledProcessError as e:
        return {'status': False, 'ping': None}  # IP-адрес не доступен, размер пинга не определен
