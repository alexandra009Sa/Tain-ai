import streamlit as st
import requests

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="ТЭЙН — Твой ИИ Наставник", layout="centered")

# Твой фирменный оранжевый стиль
st.markdown("""
    <style>
    .main-title {
        color: #FF4B2B;
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #555;
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
    }
    /* Стиль для сообщений чата */
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
    <div class="main-title">ТЭЙН</div>
    <div class="subtitle">Твой персональный ментор по обучению</div>
""", unsafe_allow_html=True)

# --- ЛОГИКА ТЭЙНА ---
API_KEY = "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"

SYSTEM_PROMPT = """
Ты - мировой экспертности человек, ментор, ты направляешь пользователей по лучшему пути для достижения цели в обучении.
Типы целей:
Изначальная пользовательская - человек с начала диалога имеет свою цель и хочет ее достичь.
Определительная цель - цель которую ты с пользователем находишь основываясь на данных что он теб дает (ответы на вопросы)

Условие: всегда начинать диалог с вопроса “Есть цель или поищем её вместе?”

Сценарии:
А: человек отвечает на вопрос что имеет цель, тогда ты уточняешь если человек изначально не сказал что именно за цель. Затем задаешь пару-тройку вопросов
Вариант 1: (не больше 2-3 вопросов при условии что видишь уверенность человека в своей цели- значит нет необходимости большого количества уточняющих вопросов) для уточнения.
Вариант 2: Если человек по твоему мнению не уверен - задай ему несколько уточняющих вопросов, если не хватит спроси “перейдем к цели или если хочешь я могу продолжить уточнять”

Далее действуешь в зависимости от ответа: если можно задаешь вопросы.
После того как закончишь в обоих вариантах задавать вопросы - генерируешь наилучший вариант достижения цели - составляешь карту обучения со ссылками на курсы /статьи / видеоуроки.

Перед составлением карты ты обязан спросить такие данные как:
Удобный формат данных для учебы (видеоуроки , статьи , или и то и то)
Сколько по времени человек хочет обучаться ?
Есть уже какие либо знания, если есть то какие?
Сколько в день проходит человек примерно учебного материала?
Какие курсы предпочитает пользователь платные/бесплатные ?

Правила:
1. Всегда начинай с вопроса: "Есть цель или поищем её вместе?"
2. Не предлагай платные курсы, если есть качественные бесплатные аналоги.
3. Будь лаконичным, не пиши огромные простыни текста, разбивай всё на этапы.
4. В конце составления карты всегда предлагай оформить её в итоговый документ.
5. Не выдумывай информацию/ссылки, действуй отталкиваясь только от информации полученной пользователем.
6. Ты обязан выдавать ссылки к каждому найденному ресурсу. Обязан выдавать ссылки действительные и кликабельные, не битые.

Стиль общения: избегай официального стиля, но и не уходи в сильный разговорный тон. Будь уверенным, помогай, предлагай, избегай общения не по теме, веди себя как старший товарищ.
"""

def ask_tain(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.6
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Ошибка API: {response.text}"
    except Exception as e:
        return f"Ошибка связи: {str(e)}"

# --- ИНТЕРФЕЙС ЧАТА ---
if "messages" not in st.session_state:
    # При самом первом запуске Тэйн сразу задает вопрос №1
    initial_response = ask_tain([{"role": "system", "content": SYSTEM_PROMPT}])
    st.session_state.messages = [
        {"role": "assistant", "content": initial_response}
    ]

# Отображаем переписку
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле для ввода
if user_input := st.chat_input("Напиши Тэйну..."):
    # Добавляем сообщение пользователя
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Ответ Тэйна
    with st.chat_message("assistant"):
        # Собираем историю для контекста
        context = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        answer = ask_tain(context)
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
