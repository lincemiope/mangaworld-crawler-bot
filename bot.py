from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from const import TELEGRAM_TOKEN, URL_PATTERN, CHECK_COOLDOWN
import spider
import user_data as ud
from models import Userdata
import re, locale, time, html
from utils import date_to_str

#region user settings
def get_user(update):
    if update.effective_user.is_bot:
        return None
    user_id = update.effective_user.id
    ud.read_data()
    return ud.get_user_data(user_id)

def start_handler(update, context):
    user = get_user(update)
    update.message.reply_html(
        '\n'.join([
            '<b>MangaWorld BOT</b>',
            '<i>Resta aggiornato sulle ultime uscite</i>',
            '\n',
            'Comandi:',
            "&#9679; /start => crea le impostazioni iniziali e mostra questo prospetto",
            "&#9679; /list_issues => mostra i manga seguiti",
            "&#9679; /add_issue => aggiunge un manga ai seguiti (specificare l'indirizzo completo)",
            "&#9679; /del_issue => elimina un manga dai seguiti (specificare l'indirizzo completo)",
            "&#9679; /check => visualizza le ultime uscite (massimo 3 volumi per manga e 15 minuti tra una ricerca e l'altra)",
        ])
)
#region issues
def list_issues(update, context):
    user = get_user(update)
    update.message.reply_text('Manga seguiti:\n' + \
        '\n'.join(user.followed_issues))

def add_issue(update, context):
    issue_text = update.message.text
    g = re.search(URL_PATTERN, issue_text)
    if not g or len(g.groups()) < 2:
        update.message.reply_text('Inserisci tutto l\'indirizzo (https://...)')
    else:
        user = get_user(update)
        issue = g.group(2)
        if issue in user.followed_issues:
            update.message.reply_text('Manga già presente in lista. Usare il comando /list_issues per verificare')
        else:
            user.followed_issues.append(issue)
            ud.save_user_data(user)
            update.message.reply_text('Manga aggiunto alla lista. Usare il comando /list_issues per verificare')

def del_issue(update, context):
    issue_text = update.message.text
    g = re.search(URL_PATTERN, issue_text)
    if not g or len(g.groups()) < 2:
        update.message.reply_text('Inserisci tutto l\'indirizzo (https://...)')
    else:
        user = get_user(update)
        issue = g.group(2)
        if issue in user.followed_issues:
            index = user.followed_issues.index(issue)
            del(user.followed_issues[index])
            ud.save_user_data(user)
            update.message.reply_text('Manga rimosso dalla lista. Usare il comando /list_issues per verificare')
        else:
            update.message.reply_text('Manga non presente in lista. Usare il comando /list_issues per verificare')
#endregion
#region check
def check(update, context):
    user = get_user(update)
    if len(user.followed_issues) == 0:
        update.message.reply_text('Non segui nessun manga, aggiungine con /add_issue')
    elif user.last_check + CHECK_COOLDOWN <= time.time():
        locale.setlocale(locale.LC_TIME, user.language or 'it_IT')
        new_issues = spider.get_new_chapters(user.followed_issues, user.last_check)
        user.last_check = int(time.time())
        ud.save_user_data(user)

        if len(new_issues) == 0:
            update.message.reply_text('Non ci sono novità dall\'ultimo controllo')

        else:
            for i, issue in enumerate(new_issues):
                reply = [
                    f'<b>{issue}</b>'
                ]
                volumes = list(new_issues[issue].keys())
                if len(volumes) > 3:
                    volumes = volumes[0:3]
 
                for volume in volumes:
                    reply.append(volume)
                    chapters = new_issues[issue][volume]['chapters']
                    chapters.sort(key=lambda x: x['title'])

                    for chapter in chapters:
                        title = chapter['title']
                        url = chapter['url']
                        released = date_to_str(chapter['release'])

                        reply.append(f'&#9679; <a href="{url}">{title}</a> - <i>{released}</i>')

                    reply.append('\n')

                update.message.reply_html('\n'.join(reply))

                if i < len(new_issues) - 1:
                    time.sleep(1.0)

    else:
        update.message.reply_text('Si può effettuare un controllo ogni 15 minuti')
        
#endregion
#region notifications
def notif_y_handler(update, context):
    user = get_user(update)
    user.notifications = True
    ud.save_user_data(user)
    update.message.reply_text('Notifiche abilitate')

def notif_n_handler(update, context):
    user = get_user(update)
    user.notifications = False
    ud.save_user_data(user)
    update.message.reply_text('Notifiche disabilitate')
#endregion
#endregion
def main():
    upd = Updater(TELEGRAM_TOKEN, use_context=True)
    disp = upd.dispatcher

    # start
    disp.add_handler(CommandHandler("start", start_handler))
    # issues
    disp.add_handler(CommandHandler("list_issues", list_issues))
    disp.add_handler(CommandHandler("add_issue", add_issue))
    disp.add_handler(CommandHandler("del_issue", del_issue))
    # check
    disp.add_handler(CommandHandler("check", check))

    upd.start_polling()

    upd.idle()

if __name__ == '__main__':
    main()

