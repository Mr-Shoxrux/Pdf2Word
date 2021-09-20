from telegram.ext import Updater, CommandHandler, ConversationHandler,MessageHandler,Filters,CallbackQueryHandler
from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup

custom_keyboard = [["Lotin","Kirill"]]
button_replykeyboard = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
Krill = False
Lotin = False
Azolik = False

def start(update, context):
    try:

        update.message.reply_html("😃Siz  botimizdan bemalol foydalanishingiz mumkin.",
                                     reply_markup=button_replykeyboard)


    except Exception as ex:
        print(ex)
def xato(update, context):
    pass
import os
def document(update, context):
    global Krill,Lotin
    chat_id = update.message.chat_id
    dirName = 'Input/' + str(chat_id)
    dirName1 = 'Output/' + str(chat_id)
    try:
        os.mkdir(dirName)
    except FileExistsError:
        pass
    try:
        os.mkdir(dirName1)
    except FileExistsError:
        pass
    file_name = str(update.message.document['file_name'])
    if file_name.endswith('.pdf') :

        path = dirName + '/' + file_name
        with open(path, 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)
        output_file=file_name.replace(".pdf",".docx")
        document_path = dirName1 + '/' + output_file
        if Lotin:
            print("lotin ishladi")
            update.message.reply_html('Biroz kuting. Jarayon davom etmoqda...')
            import process
            process.main(path,document_path,"UzbekLatin")
            context.bot.sendDocument(chat_id=chat_id,
                                     caption="Pdfdan Wordga o'tkazilgan faylingiz.",
                                     document=open(document_path, 'rb'))
            try:
                os.remove(dirName + '/' + file_name)
                os.remove(dirName1 + '/' + output_file)
            except OSError as e:
                pass
        elif Krill:
            print("kril ishladi")
            update.message.reply_html('Biroz kuting. Jarayon davom etmoqda...')
            import process
            process.main(path, document_path, "UzbekCyrillic")
            context.bot.sendDocument(chat_id=chat_id,
                                     caption="Pdfdan Wordga o'tkazilgan faylingiz. ",
                                     document=open(document_path, 'rb'))
            try:
                os.remove(dirName + '/' + file_name)
                os.remove(dirName1 + '/' + output_file)
            except OSError as e:
                pass
        else:
            context.bot.send_message(chat_id=chat_id,text="Lotin yoki Kirill tugmasini tanlang !!!")

def text(update, context):
    try:
        if update.message.to_dict()['text'] == "Kirill" or  update.message.to_dict()['text'] == "✅ Kirill":
            kril(update,context)
        elif update.message.to_dict()['text'] == "Lotin" or  update.message.to_dict()['text'] == "✅ Lotin":
            lotin(update,context)
        else:
            update.message.reply_html("Botimiz faqat <b> Pdf </b> fayllarini <b> Word </b> fayllariga o'tkazib beradi.",
                                      reply_markup=button_replykeyboard)

    except Exception:
        pass
def kril(update, context):
    try:
        global Krill,Lotin
        Lotin = False
        Krill = True
        custom_keyboard = [["Lotin", "✅ Kirill"]]
        button_replykeyboard = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_html("Kirill alifbosida yozilgan <b> Pdf </b> fayllarini yuborishingiz mumkin. ",
                              reply_markup=button_replykeyboard)
    except Exception:
        pass


def lotin(update, context):
    try:
        global Krill, Lotin
        # Azolik, prim, yangi = primer.azolikni_tekshirish(update.message.chat_id)
        # if Azolik:
        Krill = False
        Lotin = True
        custom_keyboard = [["✅ Lotin", "Kirill"]]
        button_replykeyboard = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_html(
                "Lotin alifbosida yozilgan <b> Pdf </b> fayllarini yuborishingiz mumkin. ",
                reply_markup=button_replykeyboard)
    except Exception:
        pass

def main():
    try:
        updater = Updater('')

        start_handler = CommandHandler('start', start)
        xato_handler = CommandHandler('xato', xato)
        doc_handler = MessageHandler(Filters.document, document)
        text_handler = MessageHandler(Filters.text, text)
        # tekshir = CallbackQueryHandler(tekshirish)

        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(xato_handler)
        updater.dispatcher.add_handler(doc_handler)
        updater.dispatcher.add_handler(text_handler)
        # updater.dispatcher.add_handler(tekshir)

        updater.start_polling()
        updater.idle()
    except Exception as ex:
        print(ex)
if __name__ == '__main__':
    main()