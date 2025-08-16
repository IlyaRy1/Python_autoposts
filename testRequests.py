import requests
import os

def get_ai_response(prompt):
    """Запрос к DeepSeek API с улучшенной обработкой ошибок"""
    try:
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=10  # Таймаут на запрос (секунды)
        )

        # Проверка статуса ответа
        if response.status_code != 200:
            print(f"[Ошибка] HTTP-статус: {response.status_code}, Ответ: {response.text}")
            return None

        # Проверка, что ответ содержит JSON
        try:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except (KeyError, ValueError) as e:
            print(f"[Ошибка] Неверный формат ответа: {e}, Ответ: {response.text[:200]}...")
            return None

    except requests.exceptions.RequestException as e:
        print(f"[Ошибка] Проблема с запросом: {e}")
        return None

print(get_ai_response("Расскажи анекдот"))