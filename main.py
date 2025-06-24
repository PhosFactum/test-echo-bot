import logging
import os
import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Внутренняя память для замеров
durations: list[float] = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я — Echo-бот. Пришли что угодно, и я повторю.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def addtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        return await update.message.reply_text("Использование: /addtime <секунды>")
    try:
        t = float(args[0])
    except ValueError:
        return await update.message.reply_text("Нужно число, например: /addtime 42.5")
    durations.append(t)
    await update.message.reply_text(f"Добавлено время: {t} сек. Всего замеров: {len(durations)}")

async def progression(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(durations) < 2:
        return await update.message.reply_text("Нужно хотя бы 2 замера для анализа.")
    
    ratios = []
    is_geom = True
    for i in range(len(durations)-1):
        if durations[i] == 0:
            is_geom = False
            break
        ratios.append(durations[i+1] / durations[i])
    if is_geom:
        is_geom = all(abs(ratios[i] - ratios[0]) < 1e-6 for i in range(1, len(ratios)))
    
    diffs = [durations[i+1] - durations[i] for i in range(len(durations)-1)]
    is_arith = all(abs(diffs[i] - diffs[0]) < 1e-6 for i in range(1, len(diffs)))
    
    if is_geom:
        await update.message.reply_text("Это геометрическая прогрессия.")
    elif is_arith:
        await update.message.reply_text("Это арифметическая прогрессия.")
    else:
        await update.message.reply_text("Ни арифметика, ни геометрия.")

async def squares(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        return await update.message.reply_text("Использование: /squares <числа через пробел>")
    try:
        numbers = [float(x) for x in args]
    except ValueError:
        return await update.message.reply_text("Все аргументы должны быть числами.")
    
    squared = [x**2 for x in numbers]
    result = "Квадраты чисел: " + " ".join(f"{x:.2f}" for x in squared)
    await update.message.reply_text(result)

async def wait(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        return await update.message.reply_text("Использование: /wait <секунды>")
    try:
        seconds = float(args[0])
    except ValueError:
        return await update.message.reply_text("Нужно число, например: /wait 2.5")
    
    time.sleep(seconds)
    await update.message.reply_text(f"Ожидание {seconds} сек завершено.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CommandHandler("addtime", addtime))
    app.add_handler(CommandHandler("progression", progression))
    app.add_handler(CommandHandler("squares", squares))
    app.add_handler(CommandHandler("wait", wait))
    app.run_polling()

if __name__ == "__main__":
    main()
