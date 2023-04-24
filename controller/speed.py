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
        return {'download': download_speed, 'upload': upload_speed}
    except speedtest.SpeedtestException as e:
        return e