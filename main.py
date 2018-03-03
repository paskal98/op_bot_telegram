import telebot
import datetime
from time import sleep
import codecs
from telebot import types
import threading
import json
import gc


#bot=telebot.TeleBot('516454220:AAEBUTygMYAHsKzjzJvqRlesULc7Q4wnbo8', threaded=False) #@StarterPack_bot
bot=telebot.TeleBot('539989058:AAGJsaK1LAMklwJJhtERJi0jcwloyayitmc', threaded=False) #@nuft_op_bot

# ГЛАВНАЯ КЛАВИАТУРА
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('{} Ввести группу'.format(u'\U0001f393', u'\U0001f393'),
           '{} День'.format(u'\U0001f4c5', u'\U0001f4c5'))
markup.row('{} Уведомлять'.format(u'\U0001f4cc', u'\U0001f4cc'))
markup.row('{} Время уведомлений'.format(u'\U000026a0', u'\U000026a0'))
markup.row('{} Помощь'.format(u'\U00002753', u'\U00002753'),
           '{} Инфо'.format(u'\U0001f4bf', u'\U0001f4bf'))


# данные о клиентах
clients=[]


#данные о подержуемых группах
groups_list=[]


# Обработка расписания (по базе)
def Base(group,setday):
    with open('{}.txt'.format(group),'r') as file:
        out=file.read()
    text=out.split('----------')

    split_setday=setday.split('.')
    i=0
    while i!=len(text):
        if '{}.{}.{}'.format(int(split_setday[0]),int(split_setday[1]),int(split_setday[2])-2000) in text[i]:
            return text[i]
        i+=1

    return "NULL"


# Сплит полученого расписания
def ParseString(outHTML):
    timetable=outHTML.split('tdtd')
    return timetable


# Многопоточный цыкл автоуведомления
def clock(user_id):

 for i in clients:
  if i['user']['chat_id']==user_id:
    while True:
        if i['user']['notify_on_of'] == True:
            break
        now=datetime.datetime.now()
        wakeup=datetime.time(int(i['user']['hour']),int(i['user']['minutes']),0)
        bot.send_message(user_id, '+')
        if now.hour == wakeup.hour and now.minute == wakeup.minute:

            if int(i['user']['hour']) >= 16:
                now=now+datetime.timedelta(days=1)
                clock_on_process(user_id, now, i['user']['hour'])
            elif int(i['user']['hour']) < 16:
                clock_on_process(user_id, now, i['user']['hour'])
    i['user']['notify_on_of'] = False

def clock_on_process(user_id,now,setday):
    setday = str(now.day) + '.' + str(now.month) + '.' + str(now.year)
    bot.send_message(user_id, '<b>{} - {}</b>'.format(setday, day_of_week(now.isoweekday())), parse_mode="html")
    handle_text_3(user_id)
    sleep(61)


#сохранение клиентской базы
def save():
    try:
        write_clients()
    except:
        print('write_clients errors')

def write_clients():
    with open('clients.txt','w') as file:
        file.write(json.dumps(clients))


# Возврат в главной клавиатуре
def main_keyboard(message,inject="!"):
    bot.send_message(message.chat.id, '<b>{}</b> '.format(inject), reply_markup=markup,parse_mode='html')

def main_keyboard_2(message,inject="!"):
    bot.send_message(message.chat.id, 'С возвращением в главное меню <b>{}</b> '.format(inject), reply_markup=markup,parse_mode='html')


#Если вовремя заполнения используються главнные выражения

def check_main_commands_bool(text):
    if 'группу' in text or 'День' in text or 'Уведомлять' in text or 'Время уведомлений' in text or 'Помощь' in text or 'Инфо' in text:
        return True
    else :
        return  False

def check_main_commands(message):
    handle_text_0(message)

def check_this(message,parameter='NULL'):
    try:
        if parameter=='Ввести группу':
            if check_main_commands_bool(message.text) == True:
                bot.send_message(message.chat.id, 'Нажмите еще раз - <b>{}</b>'.format(message.text), parse_mode='html')
            else:
                # bot.send_message(message.chat.id, '<b>{}</b> - это точно верная группа?\nПишите групу вот так - <b>ОП-3-8</b>'.format(message.text),parse_mode='html')
                bot.send_message(message.chat.id, '<b>{}</b> - эта группа есть в списке?\nДоступные группы - <b>ОП-3-7, ОП-3-7ск, ОП-3-8</b>'.format(message.text), parse_mode='html')
                bot.send_message(message.chat.id,'<b>Нажмите еще раз</b> - {} или выберите другой вариант ответа'.format(u'\U0001f393'), parse_mode='html')
        elif parameter=='День':
            if check_main_commands_bool(message.text) == True:
                bot.send_message(message.chat.id, 'Нажмите еще раз - <b>{}</b>'.format(message.text), parse_mode='html')
            else:
                bot.send_message(message.chat.id, '<b>Нажмите еще раз</b> - {} или выберите другой вариант ответа'.format(u'\U0001f4c5'), parse_mode='html')
                bot.send_message(message.chat.id, '<b>{}</b> - так вписывать дату нельзя!\nНужно писать вот так - <b>04.04.20</b>'.format( message.text), parse_mode='html')
                main_keyboard_2(message,inject=u'\U0001f609')

        elif parameter=='Уведомлять':
            if check_main_commands_bool(message.text) == True:
                bot.send_message(message.chat.id, 'Нажмите еще раз - <b>{}</b>'.format(message.text), parse_mode='html')
            else:
                bot.send_message(message.chat.id, '<b>Эй, тут всего три кнопки...</b>', parse_mode='html')
                main_keyboard(message, inject=u'\U0001f609')
        elif parameter=='Время уведомлений':
            if check_main_commands_bool(message.text) == True:
                bot.send_message(message.chat.id, 'Нажмите еще раз - <b>{}</b>'.format(message.text), parse_mode='html')
            else:
                bot.send_message(message.chat.id, '<b>{}</b> - это не верно!! \nНужно писать вот так - <b>09:30</b>'.format(message.text), parse_mode='html')
                bot.send_message(message.chat.id,'<b>Нажмите еще раз</b> - {} или выберите другой вариант ответа'.format(u'\U000026a0'),parse_mode='html')
        elif parameter == 'Время уведомлений_2':
            if check_main_commands_bool(message.text) == True:
                bot.send_message(message.chat.id, 'Нажмите еще раз - <b>{}</b>'.format(message.text), parse_mode='html')
            else:
                bot.send_message(message.chat.id,'<b>{}</b> - это не верно и не забывайте про   <b>:</b>\nНужно писать вот так - <b>06:00</b>'.format( message.text), parse_mode='html')
                bot.send_message(message.chat.id, '<b>Нажмите еще раз</b> - {} или выберите другой вариант ответа'.format(u'\U000026a0'), parse_mode='html')

    except:
        bot.send_message(message.chat.id, 'Возникли ошибки... :(')



#Админ панель


@bot.message_handler(commands=['time'])
def handle_text(message):
    now=datetime.datetime.now()
    bot.send_message(message.chat.id,'{}:{}:{}'.format(now.hour,now.minute,now.second))

@bot.message_handler(commands=['write'])
def handle_text(message):
  if message.chat.id == 442738038:
    try:
        write_clients()
    except:
        bot.send_message(message.chat.id,'Возникли ошибки')
  else:
      bot.send_message(message.chat.id, 'Нет прав!')

@bot.message_handler(commands=['start'])
def handle_text_start(message):
 try:
     create=False
     bot.send_message(message.chat.id, 'Привет, {}! {}'.format(message.chat.first_name,u'\U0001f60a'), reply_markup=markup)
     handle_text_5(message)
     if len(clients)==0:
         clients.append({'user':{'chat_id': 0, 'group' : '','name':'','username':'', 'setday':'','setday2':'0.0.0','triger':False, 'notification_time':'', 'notification_bool':False,'notify_on_of':False, 'hour':7,'minutes':0}})
         clients[len(clients)-1]['user']['chat_id']=message.chat.id
         clients[len(clients) - 1]['user']['name'] = message.chat.first_name
         clients[len(clients) - 1]['user']['username'] = message.from_user.username
     elif len(clients)>0:
         for i in clients:
             if i['user']['chat_id']!= message.chat.id:
                 create=True
             elif i['user']['chat_id']== message.chat.id:
                 create=False
                 break
         if create==True:
             clients.append({'user':{'chat_id': 0, 'group' : '','name':'', 'username':'','setday':'','setday2':'0.0.0','triger':False, 'notification_time':'', 'notification_bool':False,'notify_on_of':False, 'hour':7,'minutes':0}})
             clients[len(clients)-1]['user']['chat_id']=message.chat.id
             clients[len(clients) - 1]['user']['name'] = message.chat.first_name
             clients[len(clients) - 1]['user']['username'] = message.from_user.username

 except:
     bot.send_message(message.chat.id, 'Возникли ошибки')

@bot.message_handler(commands=['list'])
def handle_text(message):
 if message.chat.id == 442738038:
     bot.register_next_step_handler(message, handle_list)
 else:
     bot.send_message(message.chat.id, 'Нет прав!')

def handle_list(message):
    try:
        j = 0
        print(clients)
        bot.send_message(message.chat.id, '<b>User count:</b> {}'.format(len(clients)), parse_mode='html')
        for i in clients:
            if int(message.text)<=j:
                 bot.send_message(message.chat.id,
                             '<b>Name:</b> {}\n<b>ID:</b> {}\n<b>Group:</b> {}\n<b>Notify is</b> {}\n<b>Notifytime is</b> {}:{}\n<b>Username:</b> {}'.format(
                                 i['user']['name'], i['user']['chat_id'], i['user']['group'],
                                 i['user']['notification_bool'], i['user']['hour'], i['user']['minutes'],
                                 i['user']['username']), parse_mode='html')
            j +=1

    except:
        bot.send_message(message.chat.id, 'Возникли ошибки')


@bot.message_handler(content_types=['text'])
def handle_text(message):
 handle_text_0(message)



#Text coomands

def handle_text_0(message):
        try:
            if 'группу' in message.text:
                handle_text_1(message)
            elif 'День' in message.text:
                handle_text_2(message)
            elif 'Показать' in message.text:
                handle_text_3(message.chat.id)
            elif 'Уведомлять' in message.text:
                handle_text_4(message)
            elif 'Помощь' in message.text:
                handle_text_5(message)
            elif 'Инфо' in message.text:
                handle_text_6(message)
            elif 'Время уведомлений' in message.text:
                handle_text_7(message)
            elif 'Назад' in message.text:
                main_keyboard_2(message, inject=u'\U0001f609')
            gc.collect()
        except:
            bot.send_message(message.chat.id, 'Возникли ошибки... :(')


#Группа

def handle_text_1(message):
    bot.send_message(message.chat.id, '<b>Введите вашу групу</b>\nДоступные группы :\n<b>ОП-3-7, ОП-3-7ск, ОП-3-8, ОП-4-8, ОП-4-7, ОП-1-6м, ОП-1-7м</b>\nВнимание, введёная группа <b>сохранаяется!</b>\n(Пример: ОП-3-7)',parse_mode='html')

    bot.register_next_step_handler(message, get_answer)

def get_answer(message):
    for i in clients:
        if i['user']['chat_id']==message.chat.id:
            if Check_groups(message.text)==True:
                 i['user']['group']=message.text
                 news = 'Отлично!\nВаша група: {}'.format(i['user']['group'])
                 bot.send_message(message.chat.id, news)
                 save()
            else :
                check_this(message,parameter='Ввести группу')
        break  ###BOOST

def Check_groups(group):
    group=group.lower()
    if group in groups_list:
        return True
    else:
        return False


#Дата

def handle_text_2(message):

    #bot.send_message(message.chat.id, 'Введите дату \n(Пример: 04.04.20)')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Сегодня', 'Завтра')
    markup.row('Эта неделя', 'Следующая неделя')
    markup.row('{} Назад'.format(u'\U00002b05'))
    bot.send_message(message.chat.id, '<b>Выберете вариант ответа или введите дату</b>\n(Пример: 04.04.20)', reply_markup=markup,parse_mode='html')

    bot.register_next_step_handler(message, get_days)

def get_days(message):
 for i in clients:
   if i['user']['chat_id']==message.chat.id:
         dayset = message.text.replace('/chooseday', '')
         if 'Сегодня' in message.text:
             now = datetime.datetime.now()
             news = '\nОтлично!\nДата: {}.{}.{}'.format(now.day, now.month, now.year)
             i['user']['setday'] = '{}.{}.{}'.format(now.day, now.month,now.year)
             main_keyboard(message, inject=news)
             handle_text_3(message.chat.id)
         elif 'Завтра' in message.text:
             now = datetime.datetime.now()
             tommorow = now + datetime.timedelta(days=1)
             news = '\nОтлично!\nДата: {}.{}.{}'.format(tommorow.day, tommorow.month, tommorow.year)
             i['user']['setday'] = '{}.{}.{}'.format(tommorow.day, tommorow.month, tommorow.year)
             main_keyboard(message, inject=news)
             handle_text_3(message.chat.id)
         elif 'Назад' in message.text:
             main_keyboard_2(message, inject=u'\U0001f609')
         elif 'Эта неделя' in message.text:
             set_date_week(message, i, DAYS=0)
         elif 'Следующая неделя' in message.text:
             set_date_week(message, i, DAYS=7)
         elif '.' in message.text:
             dayset_check = dayset.split('.')
             if len(dayset_check) == 3 and dayset_check[0].isdigit() and dayset_check[1].isdigit() and dayset_check[2].isdigit():
                i['user']['setday'] ='{}.{}.{}'.format(dayset_check[0], dayset_check[1],int(dayset_check[2])+2000)
                news = '\nОтлично!\nДата: {}'.format(i['user']['setday'])
                main_keyboard(message, inject=news)
                handle_text_3(message.chat.id)
             else :
                 check_this(message,parameter='День')
         else :
             check_this(message, parameter='День')
   break  ###BOOST

def set_date_week(message,i,DAYS=0):
    now = datetime.datetime.now()
    now = now + datetime.timedelta(days=DAYS)

    Mon = now - datetime.timedelta(days=now.weekday())
    Fri = now + datetime.timedelta(days=6 - now.weekday())

    news = 'Отлично!\nДата: {}.{}.{} - {}.{}.{}'.format(Mon.day, Mon.month, Mon.year, Fri.day, Fri.month, Fri.year)
    i['user']['setday'] = '{}.{}.{}'.format(Mon.day, Mon.month, Mon.year)
    i['user']['setday2'] = '{}.{}.{}'.format(Fri.day, Fri.month, Fri.year)
    main_keyboard(message, inject=news)
    handle_text_3_week(message)


#Показать

def handle_text_3(user_id):
 for i in clients:
   if i['user']['chat_id']==user_id:
     if i['user']['group'] != '' and i['user']['setday'] != '':
        bot.send_message(user_id, "Подождите пожайлуста пару секунд...")

        out=Base(i['user']['group'],i['user']['setday'])
        text=ParseString(out)


        I = 1
        para =1
        send = ''
        if  'NULL'  in text[0] :
            bot.send_message(user_id, '<b>За вашим запрсом, ничего не найдено</b>', parse_mode="html")
            break  ###BOOST
        elif text[0].find('За вашим запитом записів не знайдено')!=-1:
            bot.send_message(user_id, '<b>Нет пар по такому запросу</b>', parse_mode="html")
        else:
          while I != len(text):
            if len(text[I]) == 1:
                send += '-\n\n'
            elif I % 2 != 0:
                send += '<b>{} пара {}</b>\n'.format(para, text[I])
                para+=1
            else:
                send += '{}\n\n'.format(text[I][0:-1])
            I += 1
          bot.send_message(user_id, send,parse_mode="html")
     else:
        bot.send_message(user_id, "<b>Группа не заполнена! Что бы вывести расписание, её нужно заполнить</b>")
   break  ###BOOST

def handle_text_3_week(message):
    for i in clients:
        if i['user']['chat_id'] == message.chat.id:
            if i['user']['group'] != '' and i['user']['setday'] != '':
              bot.send_message(message.chat.id, "Подождите пожайлуста пару секунд...")
              j=1
              while True:

                out = Base(i['user']['group'], i['user']['setday'])
                text = ParseString(out)



                if  'NULL' in text[0]:
                    bot.send_message(message.chat.id, '<b>За вашим запрсом, ничего не найдено</b>', parse_mode="html")
                    week_set_daysofweek(i)
                    j+=1
                    if i['user']['setday'] == i['user']['setday2']:
                        break
                elif 'За вашим запитом записів не знайдено.' in text[0]:
                    weekday = day_of_week(day=j)
                    if  j<=5:
                        send=' '
                        send += '<b>{} - {}</b>\n'.format(i['user']['setday'], weekday)
                        bot.send_message(message.chat.id, '{}<b>Пар нет</b>'.format(send), parse_mode="html")
                    week_set_daysofweek(i)
                    j += 1
                    if i['user']['setday'] == i['user']['setday2']:
                        break
                elif len(text)!=1:
                    I = 1
                    para = 1
                    send = ''
                    weekday=day_of_week(day=j)
                    send+='<b>{} - {}</b>\n'.format(i['user']['setday'],weekday)

                    while I != len(text):
                        if len(text[I]) == 1:
                            send += '-\n\n'
                        elif I % 2 != 0:
                            send += '<b>{} пара {}</b>\n'.format(para, text[I])
                            para += 1
                        else:
                            send += '{}\n\n'.format(text[I][0:-1])
                        I += 1
                    bot.send_message(message.chat.id, send, parse_mode="html")
                    week_set_daysofweek(i)
                    if i['user']['setday'] == i['user']['setday2']:
                        break
                    j+=1
            else:
                bot.send_message(message.chat.id, "<b>Сначала заполните группу, тогда расписание появиться</b>")
        break  ###BOOST

def day_of_week(day=0):
    if day==1:
        return 'Понедельник'
    elif day==2:
        return 'Вторник'
    elif day==3:
        return 'Среда'
    elif day==4:
        return 'Четверг'
    elif day==5:
        return 'Пятница'
    elif day==6:
        return 'Суббота'
    elif day==7:
        return 'Воскресение'
    else:
        return 'NULL'

def week_set_daysofweek(i):
    to_split = i['user']['setday'].split('.')
    dat = datetime.datetime(int(to_split[2]), int(to_split[1]), int(to_split[0]))
    dat = dat + datetime.timedelta(days=1)
    i['user']['setday'] = '{}.{}.{}'.format(dat.day, dat.month, dat.year)


#Вкл\Выкл уведомления

def handle_text_4(message):
    #bot.send_message(message.chat.id, 'Включить уведомления о парах?')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(u'\U00002714', u'\U00002716')
    markup.row('{} Назад'.format(u'\U00002b05'))
    bot.send_message(message.chat.id, '<b>Включить уведомления о парах?</b>', reply_markup=markup,parse_mode='html')

    bot.register_next_step_handler(message, set_notificate)

def set_notificate(message):
 for i in clients:
  if i['user']['chat_id'] == message.chat.id:
    t=threading
    if message.text==u'\U00002714':
        if i['user']['notification_bool']==False:
            i['user']['notification_bool']=True
            t=threading.Thread(target=clock,args=(message.chat.id,))
            t.daemon=True
            t.start()
            main_keyboard(message,inject="\nУведомления включены")
            save()
        elif i['user']['notification_bool']==True:
             main_keyboard(message, inject="\nУведомления уже включены")
    elif message.text==u'\U00002716':
        if i['user']['notification_bool']==True:
            i['user']['notification_bool']=False
            i['user']['notify_on_of'] = True
            main_keyboard(message, inject="\nУведомления отключены")
            save()
        elif i['user']['notification_bool']==False:
            main_keyboard(message, inject="\nУведомления уже отключены")
    elif 'Назад' in message.text:
        main_keyboard_2(message, inject=u'\U0001f609')
    else :
        check_this(message,parameter='Уведомлять')
  break  ###BOOST


#Помощь

def handle_text_5(message):
    bot.send_message(message.chat.id,
                     '{}  <b>Ввести группу</b> - заполните свою группу, она сохранится и в дальнейшем по ней будет виводиться расписание. Чтобы заполнить ее правильно, необходимо ставить \" - \" \n<b>Пример:</b> ОП-1-11\n\n '
                     '{}  <b>День</b> - с помощью этой команды можно ввести дату самому <b>(дд.мм.гг)</b>, так же можно нажать на кнопки  <b>(Сегодня, Завтра, Эта неделя, Следующая неделя)</b>\n<b>Пример:</b> 20.04.20\n\n'
                     '{} <b>Уведомлять</b> - здесь есть возможность включить автооповещание о парах, по умолчанию стоит <b>7:00</b> и уведомления отключены\n\n'
                     '{}  <b>Инфо</b> - информация о заполненых полях и не только\n\n'
                     '{} <b>Время уведомлений</b> - тут можно изменить время с <b>7:00</b> на любое другое'.format(
                         u'\U0001f393', u'\U0001f4c5',
                         u'\U0001f4cc', u'\U0001f4bf',
                         u'\U000026a0'), parse_mode="html")


#Инфо

def handle_text_6(message):
 for i in clients:
  if i['user']['chat_id'] == message.chat.id:
    on_off = ''
    if i['user']['notification_bool'] == False:
        on_off = 'ВЫКЛ'
    elif i['user']['notification_bool'] == True:
        on_off = 'ВКЛ'
    bot.send_message(message.chat.id, '<b>Вас зовут :</b> {}\n'
                                      '<b>Ваша група :</b> {}\n'
                                      '<b>Уведомления :</b> {}.\n'
                                      '<b>Время уведомлений :</b> {}:{}\n'.format(message.chat.first_name, i['user']['group'], on_off,i['user']['hour'],i['user']['minutes']),parse_mode="html")
  break  ###BOOST


#Время уведомлений

def handle_text_7(message):
    bot.send_message(message.chat.id, '<b>Введите время автоопповещения</b> (Пример: 7:00)\n'
                                      '<b>ВАЖНО!</b> Время введеное до <b>16</b> будет показывать расписание на текущий день\n'
                                      '<b>ВАЖНО!</b> Время введеное после <b>16</b> будет показывать расписание на следующий день\n',parse_mode='html')
    bot.register_next_step_handler(message, set_aday)

def set_aday(message):
    for i in clients:
        if i['user']['chat_id']==message.chat.id:
            if ':' in message.text:
                str=(message.text).split(':')

                if str[0].isdigit()==True and str[1].isdigit()==True and len(str)==2:
                    bot.send_message(message.chat.id, 'Отлично!\nВремя уведомлений: {}'.format(message.text))
                    i['user']['hour']=str[0]
                    i['user']['minutes'] = str[1]
                    save()
                else :
                    check_this(message,parameter='Время уведомлений')
            else:
                check_this(message, parameter='Время уведомлений_2')
        break  ###BOOST





# main start

def read_clients():
    with open('clients.txt','r') as json_file:
        data = json.load(json_file)
        return data

def read_count_groups():
    with open('count_groups.txt', 'r') as file:
        out = file.read()
        text = out.split(',')
        for i in text:
            groups_list.append(i)

def update_bot():
    for i in clients:
        bot.send_message(i['user']['chat_id'], 'Бот обновлен! {}'.format(u'\U0001f609'), reply_markup=markup,parse_mode='html')

def auto_notify():
    for i in clients:
       if i['user']['notification_bool'] == True:
            t=threading
            t = threading.Thread(target=clock, args=(int(i['user']['chat_id']),))
            t.daemon = True
            t.start()




if __name__ =='__main__':
   try:
    clients=read_clients()
    read_count_groups()
    auto_notify()
    #update_bot()
   except Exception as e:
       print(e)

   while True:
       try:
           bot.polling(none_stop=True, interval=0)
       except Exception as e:
           print(e)



