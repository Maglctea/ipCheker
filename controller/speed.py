import speedtest

def get_internet_speed():
    """Функция для получения скорости интернета"""
    try:
        # Создаем объект Speedtest
        st = speedtest.Speedtest()
        # Выполняем тесты на загрузку и выгрузку данных
        st.get_best_server()
        download_speed = st.download() / 10**6  # Мбит/с
        upload_speed = st.upload() / 10**6  # Мбит/с
        # Возвращаем скорость загрузки и выгрузки
        return download_speed, upload_speed
    except speedtest.SpeedtestException as e:
        print(f"Произошла ошибка при тестировании скорости интернета: {e}")
        return None, None

# Получаем скорость интернета
download_speed, upload_speed = get_internet_speed()

# Выводим результаты
if download_speed is not None and upload_speed is not None:
    print(f"Скорость загрузки: {download_speed:.2f} Мбит/с")
    print(f"Скорость выгрузки: {upload_speed:.2f} Мбит/с")
