from telegram import ReplyKeyboardMarkup

class Config:
    confirmation_keyboard = [['شروع دوباره', 'مورد تایید است']]
    confirmation_keys = ReplyKeyboardMarkup(confirmation_keyboard, resize_keyboard = True, one_time_keyboard = True)

    degree_keyboard = [['۱', '۲', '۳', '۴'],
                        ['۵', '۶', '۷', '۸'],
                        ['۹', '۱۰', '۱۱', '۱۲']]
    degree_keys = ReplyKeyboardMarkup(degree_keyboard, resize_keyboard = True, one_time_keyboard = True)

    lesson_keyboard = [['ادبیات', 'زبان', 'دینی', 'عربی'],
                        ['ریاضی', 'فیزیک', 'شیمی', 'زیست']]
    lesson_keys = ReplyKeyboardMarkup(lesson_keyboard, resize_keyboard = True, one_time_keyboard = True)

    quiz_keyboard = [['شروع', 'نه،هنوز آماده نیستم']]
    quiz_keys = ReplyKeyboardMarkup(quiz_keyboard, resize_keyboard = True, one_time_keyboard = True)

    answer_keyboard = [['1', '2'],
                        ['3', '4']]
    answer_keys = ReplyKeyboardMarkup(answer_keyboard, resize_keyboard = True, one_time_keyboard = True)
        