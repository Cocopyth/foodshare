from emoji import emojize
from telegram import ParseMode
from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton as IKB
from telegram import InlineKeyboardMarkup
from foodshare.handlers.cook_conversation import ConversationStage, \
    get_message, create_meal_message
from foodshare.keyboards.confirmation_keyboard import confirmation_keyboard
from foodshare.bdd.database_communication import get_user_from_chat_id, \
    add_meal, get_users_to_contact
import threading

import copy

def ask_for_conclusion(update, context, highlight=None):
    ud = context.user_data
    query = update.callback_query
    ud['last_query'] = query
    epilog = (
        'Now I will send a message to people if you want'
        + ' to add a text message just send it to me. '
        + 'Press confirm when you\'re ready!'
    )
    context.user_data['confirmation_stage'] = True
    text = get_message(context, epilog=epilog, highlight=highlight)
    if (
        update.message is None
    ):  # reply doesn't work if there is no message to reply to
        update.callback_query.edit_message_text(
            text=text,
            reply_markup=confirmation_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        update.message.reply_text(
            text=text,
            reply_markup=confirmation_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )

    return ConversationStage.CONFIRMATION


def additional_message(update, context):
    bot = context.bot
    ud = context.user_data
    ud['message2others'] = update.message.text
    bot.deleteMessage(update.message.chat_id, update.message.message_id)
    query = ud['last_query']
    epilog = (
        'Now I will send a message to people if you want'
        + ' to add a text message just send it to me. '
        + 'Press confirm when you\'re ready!'
    )
    text = get_message(context, epilog=epilog)

    bot.edit_message_text(
        text=text,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=confirmation_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationStage.CONFIRMATION


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""

    update.callback_query.edit_message_text(
        text=emojize(
            f'Messages sent : I will update you on the answers '
            f':nerd_face: '
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    sticker_id = (
        'CAACAgIAAxkBAAIJNF6N7Cj5oZ7qs9hrRce8HdLTn'
        '7FdAAKcAgACa8TKChTuhP744omRGAQ'
    )  # Lazybone ID
    bot = context.bot
    chat_id = context.user_data['chat_id']
    ud = context.user_data
    who_cooks = get_user_from_chat_id(chat_id)
    add_meal(who_cooks, ud)
    to_contact = get_users_to_contact(who_cooks)
    how_many = ud['nb_of_person']
    meal_info =copy.copy(ud)
    meal_info['who_cooks']=who_cooks
    thread = threading.Thread(target=ask_participation,
                         args=
                         (context, to_contact, how_many, meal_info))
    thread.start()
    bot.send_sticker(chat_id, sticker_id)
    ud.clear()
    return ConversationHandler.END


def ask_participation(context, to_contact, how_many, meal_info):
    accepted = 0
    refused = 0
    jq = context.job_queue
    job_list=[]
    participants=[]
    def create_job_context(user):
        job_context = {}
        job_context['pot_participant'] = user

        job_context[
            'meal_info'] = meal_info  # there is more info in there than what's
        # needed
        job_context['has_answered'] = False
        job_context['is_coming'] = False
        return job_context
    for user in to_contact[:how_many]:
        job_context = create_job_context(user)
        job_list.append(jq.run_once(ask_user_participation, when=1,
                                    context=job_context))
    while accepted < how_many-1: #how many includes the cook
        for job in job_list:
            if job.context['has_answered']:
                if job.context['is_coming']:
                    accepted+=1
                    participants.append(job.context['pot_participant'])
                    job_list.remove(job)
                else:
                    user = to_contact[how_many+refused]
                    job_context = create_job_context(user)
                    job_list.append(jq.run_once(ask_user_participation,
                                                context=job_context))



def ask_user_participation(context):
    bot = context.bot
    job = context.job
    job_context = job.context
    user = job_context['pot_participant']
    meal_info = job_context['meal_info']
    message = create_meal_message(meal_info)
    keyboard = InlineKeyboardMarkup(
        [
            [
                IKB('Yes', callback_data='secret_key_yes'),
                IKB('No', callback_data='secret_key_no'),
            ],
        ]
    )
    bot.send_message(
        chat_id = user.telegram_id, text= message,reply_markup=keyboard
    )

