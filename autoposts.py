"""Импорт библиотек"""
import os # Для работы с переменными окружения
import time
from datetime import datetime
import vk_api  # Импорт библиотеки для взаимодействия с API VK
from vk_api.utils import get_random_id  # Импорт функции для генерации уникального ID для каждого
# поста (требуется ВКонтакте, чтобы избежать дублирования)

def vk_post(group_id, text, vk_token):  # Функция публикации поста
    # (Цифровой ID группы, Текст поста, Токен [ключ] доступа)

    try:  # Перехват ошибок
        """Авторизация"""
        vk_session = vk_api.VkApi(token=vk_token)  # Создание сессии ВК с переданным токеном
        vk = vk_session.get_api()  # Передача доступа к методам API VK

        """Публикация поста"""
        result = vk.wall.post(  # wall.post - публикация поста
            owner_id=f"-{group_id}",  # '-' означает, что это группа, а не личная страница
            from_group=1,  # '1' - опубликовать от имени группы
            message=text,  # Текст поста
            random_id=get_random_id()  # Уникальный id поста, чтобы ВК не считал пост дубликатом
        )

        print(f"[{datetime.now()}] Пост успешно опубликован! ID: {result['post_id']}")
        return True  # Отслеживание выполнения функции
    except Exception as e:  # Exception - название ошибки
        print(f"[{datetime.now()}] Ошибка публикации в ВК: {e}")
        return False  # Отслеживание невыполнения функции


def main():
    """Настройки"""
    VK_ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")  # Ключ доступа
    if VK_ACCESS_TOKEN is None:
        print("Ошибка: переменная VK_ACCESS_TOKEN не найдена")
    VK_GROUP_ID = "231800152"  # ID группы (только цифры)
    POST_INTERVAL = 60  # Интервал между постами в сек

    num = 0  # Вспомогательная переменная

    while True:  # бесконечный цикл

        print(f"[{datetime.now()}] Начало новой итерации")
        post_text = f"Текст{num}"  # Текст поста
        print(f"[{datetime.now()}] Сгенерированный текст:\n{post_text}")

        """Публикация в ВК"""
        if vk_post(VK_GROUP_ID, post_text, VK_ACCESS_TOKEN):  # Вызов функции и проверка на выполнение
            num += 1
        else:
            pass

        """Ожидание следующего поста"""
        print(f"[{datetime.now()}] Ожидание {POST_INTERVAL // 60} минут до следующего поста...")
        time.sleep(POST_INTERVAL)  # Пауза


if __name__ == "__main__":  # Исполнение только при прямом запуске файла, а не при импорте
    main()
