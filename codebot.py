from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import io
import asyncio
import nest_asyncio
import telegram.error

BOT_TOKEN = '8086701406:AAGKpDDVNysglDTLCtrXSvdWw98DlsczVQs'

ADMIN_IDS = []

GMAIL_SENDER = "baoboitele@gmail.com"
GMAIL_PASSWORD = "123456aA@"
GMAIL_RECEIVER = "baoboitele@gmail.com"

qr_image_data = None

def send_email_notification(subject, body):
    print(f"[Email notification disabled] Subject: {subject}, Body: {body}")

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, text: str):
    print(f"[Notify admin disabled] {text}")

def format_user(user):
    username = f"@{user.username}" if user.username else "(chưa có username)"
    return f"{user.id} {username}"

async def load_qr_image():
    global qr_image_data
    if qr_image_data is None:
        with open(r'D:\BOT TELEGRAM\qr_vietcombank.jpg', 'rb') as f:
            qr_image_data = io.BytesIO(f.read())
    qr_image_data.seek(0)
    return qr_image_data

async def safe_edit_message_text(query, text, reply_markup=None, parse_mode=None):
    """Hàm an toàn gọi edit_message_text, tránh lỗi 'Message is not modified'."""
    try:
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=parse_mode)
    except telegram.error.BadRequest as e:
        if 'Message is not modified' in str(e):
            pass
        else:
            raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await notify_admin(context, f"Người dùng {format_user(user)} đã bắt đầu bot bằng lệnh /start.")

    text = (
        "👋 *Shop Bảo Bối* xin chào..  ! \n"
        "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        "•\t*Ngoài bán mình cho tư bản ra thì nay em Bối còn bán thêm cả Bank Online & Tele Premium.*\n"
        "🔰\t*Bank Online*: Giao dịch nhanh chóng, an toàn, giá rẻ!\n"
        "🔰\t*Tele Premium*: Nick xịn, mõm hay, nâng tầm đẳng cấp!\n\n"
    )

    keyboard = [
        [InlineKeyboardButton("🚀  Telegram Premium", callback_data='premium')],
        [InlineKeyboardButton("🏦  Bank Online", callback_data='bank')],
        [
            InlineKeyboardButton("🎯 Báo Lỗi", url='https://t.me/lamgicoloi'),
            InlineKeyboardButton("☎️ ADMIN", url='https://t.me/boibank6789'),
            InlineKeyboardButton("💰 Nạp Tiền", callback_data='nap_tien'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        if update.callback_query.message and update.callback_query.message.text:
            await safe_edit_message_text(update.callback_query, text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_nap_tien(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await notify_admin(context, f"Người dùng {format_user(user)} đã xem thông tin Nạp Tiền.")

    photo = await load_qr_image()
    bank_info = (
        "Thông tin chuyển khoản:\n"
        "- Số tài khoản: 123456789\n"
        "- Chủ tài khoản: Nguyễn Văn A\n"
        "- Ngân hàng: Vietcombank\n\n"
        "⚠️ Vui lòng quét mã QR hoặc dùng thông tin trên để chuyển khoản  !!.\n "
    )

    keyboard = [
        [InlineKeyboardButton("✅   DONE   ✅", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=query.message.chat.id,
        photo=photo,
        caption=bank_info,
        reply_markup=reply_markup
    )

async def handle_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await notify_admin(context, f"Người dùng {format_user(user)} đã xem menu Premium.")

    text = ('''
🚀 *TELEGRAM PREMIUM – LỢI ÍCH SIÊU XỊN*

• 📤 *Gửi file 4GB* – tha hồ gửi phim dài tập không lo bóp file.
• ⚡️ *Tải xuống nhanh* – không giới hạn, khỏi đợi mòn mỏi.    
• 🎙️ *Voice thành chữ* – lười nghe? Đọc luôn cho tiện mình toàn thế.  
• 🖼️ *Avatar động đậy* – nổi bật giữa rừng avatar đứng im.  
• 🧼 *Không quảng cáo* – tám chuyện không bị làm phiền.  
• 🤫 *Ẩn nhãn bot* – chuyển tiếp trông như “tự nghĩ ra”, sang xịn hẳn.  
• 💎 *Sticker xịn, emoji chất* – tung ra là đối phương cười xỉu.  
• 📈 *Tăng giới hạn nhóm, kênh, ghim,...* – dành cho hội nhiều bạn, nhiều drama.
'''    
    )

    keyboard = [
        [
            InlineKeyboardButton("1 Tháng", callback_data='order_premium_1'),
            InlineKeyboardButton("3 Tháng", callback_data='order_premium_3'),
            InlineKeyboardButton("6 Tháng", callback_data='order_premium_6'),
        ],
        [
            InlineKeyboardButton("12 Tháng", callback_data='order_premium_12'),
            InlineKeyboardButton("Kênh Sao", url='https://t.me/boibanvip'),
            InlineKeyboardButton("↩️ Quay lại", callback_data='main_menu')
        ],
    ]

    await safe_edit_message_text(query, text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_order_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data = query.data
    period = data.split('_')[-1]

    prices = {
        '1': '169.000đ',
        '3': '369.000đ',
        '6': '569.000đ',
        '12': '869.000đ',
    }
    price = prices.get(period, 'Không xác định')

    descriptions = {
        '1': (
            "      💎 *Gói 1 tháng cao cấp* 💎\n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  169.000 VND*\n"
        ),
        '3': (
            "      💎 *Gói 3 tháng cao cấp* 💎 \n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  369.000 VND*\n"
        ),
        '6': (
            "      💎 *Gói 6 tháng cao cấp* 💎\n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  569.000 VND*\n"
        ),
        '12': (
            "      💎 *Gói 12 tháng cao cấp* 💎\n"
            "• Tốc độ tải xuống nhanh hơn\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• Biểu tượng siêu ngầu, huy hiệu VIP\n"
            "• Tăng giới hạn gửi tin nhắn và tệp tin\n"
            "• *Thanh Toán  :  869.000 VND*\n"
        ),
    }

    description = descriptions.get(period, "Không có mô tả cho gói này.")

    text = f"*♦️Gói được chọn:* *{period} Tháng Premium  ♦️* \n\n{description}"

    keyboard = [
        [InlineKeyboardButton("🎁 Xác nhận mua gói này", callback_data='nap_tien')],
        [InlineKeyboardButton("↩️ Quay lại", callback_data='premium')]
    ]

    await safe_edit_message_text(query, text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text = (
        "𝐁𝐀𝐍𝐊 𝐆𝐈𝐀́ 𝐑𝐄̉ & 𝐀𝐍 𝐓𝐎𝐀̀𝐍\n\n"
        "🎆 Bank online hạn mức 100m/1 tháng (tên, CCCD random, sđt của bạn) sống cực lâu\n"
        "        🚀 Giá 1m5\n"
        "🎆 Bank Quầy: Full hạn mức tháng All ngân hàng (20m/ngày) tên + sđt + gmail = của bạn.\n"
        "                   Inbox\n\n"
        "😯 Bank đã sẵn SINH TRẮC HỌC, khi nhận bank bạn chỉ cần Login và Dùng, ko cần động tác thừa nào nữa 😉"
    )
    keyboard = [
        [
            InlineKeyboardButton("Bank Web", callback_data='bank_web'),
            InlineKeyboardButton("Bank App", callback_data='bank_app'),
        ],
        [
            InlineKeyboardButton(" 🏡 Back Home", callback_data='main_menu'),  # <-- Sửa callback_data đúng
        ],
    ]
    await safe_edit_message_text(query, text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user

    if data not in ('premium', 'start_command', 'done_from_nap_tien'):
        context.user_data['previous_screen'] = data

    if data == 'nap_tien':
        await handle_nap_tien(update, context)
    elif data == 'done_from_nap_tien' or data == 'main_menu':
        previous = context.user_data.get('previous_screen')
        if not previous or data == 'main_menu':
            await start(update, context)
            return
        if previous == 'premium':
            await handle_premium(update, context)
        elif previous == 'bank':
            await handle_bank(update, context)
        elif previous and previous.startswith('order_premium_'):
            await handle_order_premium(update, context)
        else:
            await start(update, context)
    elif data == 'start_command':
        await notify_admin(context, f"Người dùng {format_user(user)} bấm nút DONE, trở về màn hình chính.")
        await start(update, context)
    elif data == 'back':
        await notify_admin(context, f"Người dùng {format_user(user)} bấm nút Back to Bot, quay lại màn hình trước đó.")
        previous = context.user_data.get('previous_screen', 'start_command')
        if previous == 'nap_tien':
            await handle_nap_tien(update, context)
        elif previous == 'premium':
            await handle_premium(update, context)
        elif previous and previous.startswith('order_premium_'):
            await handle_order_premium(update, context)
        else:
            await start(update, context)
    elif data == 'premium':
        await handle_premium(update, context)
    elif data and data.startswith('order_premium_'):
        await handle_order_premium(update, context)
    elif data == 'bank':
        await handle_bank(update, context)
    elif data == 'bank_web':
        await safe_edit_message_text(
            query,
            "Bạn đã chọn Bank Web.\nThông tin chi tiết sẽ được cập nhật sau.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Quay lại", callback_data='bank')]]),
            parse_mode='Markdown'
        )
    elif data == 'bank_app':
        await safe_edit_message_text(
            query,
            "Bạn đã chọn Bank App.\nThông tin chi tiết sẽ được cập nhật sau.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Quay lại", callback_data='bank')]]),
            parse_mode='Markdown'
        )
    else:
        await start(update, context)

async def main():
    nest_asyncio.apply()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bảo Bối Shop đang chạy 24/7...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
