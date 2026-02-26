import telebot
import phonenumbers
from phonenumbers import geocoder, carrier

# Твой токен
bot = telebot.TeleBot('8742924227:AAFtHcF-AXTRMoAA6CahVxvAWUSpqvyIZps')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Привет! Я бот, который определяет информацию по номеру телефона.\n"
        "Просто отправь мне номер в международном формате, например:\n"
        "• +79161234567\n"
        "• +375291234567\n"
        "• +74951234567"
    )

@bot.message_handler(func=lambda message: True)
def handle_number(message):
    text = message.text.strip()
    try:
        # Парсим номер
        phone = phonenumbers.parse(text, None)

        if not phonenumbers.is_valid_number(phone):
            bot.reply_to(message, "❌ Номер недействителен. Проверь формат и попробуй снова.")
            return

        # Получаем страну
        country = geocoder.country_name_for_number(phone, "ru")
        # Получаем регион/город
        region = geocoder.description_for_number(phone, "ru")
        # Получаем оператора
        operator_name = carrier.name_for_number(phone, "ru")
        # Форматируем номер
        formatted_number = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        # Если регион совпадает со страной (библиотека вернула страну вместо региона), считаем регион неопределённым
        if region and region == country:
            region = None

        # Формируем ответ
        response = f"📱 *Номер:* {formatted_number}\n"
        response += f"🌍 *Страна:* {country}\n"
        response += f"📍 *Регион/город:* {region if region else 'не определен'}\n"
        response += f"📞 *Оператор:* {operator_name if operator_name else 'не определен'}"

        bot.send_message(message.chat.id, response, parse_mode="Markdown")

    except phonenumbers.NumberParseException:
        bot.reply_to(message, "❌ Не удалось распознать номер. Убедись, что он написан правильно.")
    except Exception as e:
        bot.reply_to(message, "❌ Произошла внутренняя ошибка. Попробуй позже.")
        print(f"Ошибка: {e}")  # для отладки

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
