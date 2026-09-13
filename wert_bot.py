import os
import requests
import telebot

# إعداد التوكن والآيدي الخاص بك
TOKEN = "8864854283:AAEROI_8D48-oyspYk162eAfAVY9w-UZjiw"
ADMIN_ID = '7434938603'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو تيك توك وسأقوم بتحميله لك بدون علامة مائية 🚀")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    
    # التأكد من أن الرابط من تيك توك
    if "tiktok.com" not in url:
        bot.reply_to(message, "يرجى إرسال رابط تيك توك صحيح.")
        return

    msg = bot.reply_to(message, "جاري تحميل الفيديو، انتظر لحظة... ⏳")

    try:
        # استخدام API مجاني لاستخراج فيديو تيك توك بدون علامة مائية
        api_url = f"https://tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()

        if response.get("code") == 0:
            video_url = response["data"]["play"]
            title = response["data"].get("title", "فيديو تيك توك")
            
            # إرسال الفيديو للمستخدم
            bot.send_video(
                message.chat.id, 
                video_url, 
                caption=f"تم التحميل بنجاح! ✅\n\n📌 العنوان: {title}"
            )
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("حدث خطأ أثناء جلب الفيديو، تأكد من صحة الرابط.", message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text("فشل الاتصال بالسيرفر، حاول لاحقاً.", message.chat.id, msg.message_id)

# تشغيل البوت
bot.infinity_polling()
