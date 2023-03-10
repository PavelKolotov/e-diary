import random


from datacenter.models import (Schoolkid, Mark, Chastisement, Lesson, Commendation)


COMMENDATION_TEXT = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]


def get_schoolkid(schoolkid_name):
    if not schoolkid_name:
        print('Введите фамилию и имя ученика')
    else:
        try:
            schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
            return schoolkid
        except Schoolkid.DoesNotExist:
            print(f'Ученик {schoolkid_name} не найден')
            return
        except Schoolkid.MultipleObjectsReturned:
            print('Найдено несколько учеников по введенным данным, повторите ввод')
            return


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid:
        Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name, lesson_name):
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid:
        lesson = Lesson.objects.filter(
            subject__title=lesson_name,
            group_letter=schoolkid.group_letter,
            year_of_study=schoolkid.year_of_study
        ).order_by('?').first()
        if not lesson:
            print('Уроков по введенному предмету не найдено')
            return
        commendation_text = random.choice(COMMENDATION_TEXT)
        Commendation.objects.create(text=commendation_text, created=lesson.date, schoolkid=schoolkid,
                                    subject=lesson.subject, teacher=lesson.teacher)


def main(schoolkid_name, lesson_name):
    fix_marks(schoolkid_name)
    remove_chastisements(schoolkid_name)
    create_commendation(schoolkid_name, lesson_name)
