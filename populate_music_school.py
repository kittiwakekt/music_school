#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta
import random

# Добавляем путь к проекту в Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Настройка Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Замените на имя вашего проекта
django.setup()

from music_school.models import Direction, Teacher, Student, Group, Enrollment
from django.contrib.auth import get_user_model

def create_directions():
    """Создание направлений обучения"""
    directions_data = [
        {'name': 'Фортепиано', 'years_of_study': 7, 'description': 'Классическое фортепианное искусство'},
        {'name': 'Гитара', 'years_of_study': 5, 'description': 'Акустическая и классическая гитара'},
        {'name': 'Скрипка', 'years_of_study': 8, 'description': 'Струнные инструменты'},
        {'name': 'Вокал', 'years_of_study': 6, 'description': 'Академический и эстрадный вокал'},
        {'name': 'Ударные', 'years_of_study': 4, 'description': 'Ударная установка и перкуссия'},
        {'name': 'Флейта', 'years_of_study': 6, 'description': 'Духовые инструменты'},
    ]
    
    directions = []
    for data in directions_data:
        direction, created = Direction.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        directions.append(direction)
        print(f"Направление: {direction}")
    
    return directions

def create_teachers(directions):
    """Создание преподавателей"""
    teachers_data = [
        {'first_name': 'Анна', 'last_name': 'Иванова', 'middle_name': 'Сергеевна', 'directions': [0, 3]},  # Фортепиано, Вокал
        {'first_name': 'Дмитрий', 'last_name': 'Петров', 'middle_name': 'Александрович', 'directions': [1, 4]},  # Гитара, Ударные
        {'first_name': 'Ольга', 'last_name': 'Сидорова', 'middle_name': 'Викторовна', 'directions': [2, 5]},  # Скрипка, Флейта
        {'first_name': 'Михаил', 'last_name': 'Кузнецов', 'middle_name': 'Игоревич', 'directions': [0, 1]},  # Фортепиано, Гитара
        {'first_name': 'Екатерина', 'last_name': 'Смирнова', 'middle_name': 'Дмитриевна', 'directions': [3, 5]},  # Вокал, Флейта
    ]
    
    teachers = []
    for data in teachers_data:
        teacher, created = Teacher.objects.get_or_create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data['middle_name'],
            defaults={'is_active': True}
        )
        
        # Добавляем направления
        for dir_index in data['directions']:
            teacher.directions.add(directions[dir_index])
        
        teachers.append(teacher)
        print(f"Преподаватель: {teacher} - {[d.name for d in teacher.directions.all()]}")
    
    return teachers

def create_students():
    """Создание студентов"""
    students_data = [
        {'first_name': 'Иван', 'last_name': 'Соколов', 'middle_name': 'Алексеевич', 'birth_date': date(2012, 5, 15), 'phone_parent': '+79161234567'},
        {'first_name': 'Мария', 'last_name': 'Орлова', 'middle_name': 'Дмитриевна', 'birth_date': date(2013, 8, 22), 'phone_parent': '+79162345678'},
        {'first_name': 'Алексей', 'last_name': 'Волков', 'middle_name': 'Сергеевич', 'birth_date': date(2011, 3, 10), 'phone_parent': '+79163456789'},
        {'first_name': 'София', 'last_name': 'Попова', 'middle_name': 'Андреевна', 'birth_date': date(2014, 11, 5), 'phone_parent': '+79164567890'},
        {'first_name': 'Артем', 'last_name': 'Лебедев', 'middle_name': 'Игоревич', 'birth_date': date(2012, 7, 18), 'phone_parent': '+79165678901'},
        {'first_name': 'Анна', 'last_name': 'Козлова', 'middle_name': 'Викторовна', 'birth_date': date(2013, 2, 28), 'phone_parent': '+79166789012'},
        {'first_name': 'Максим', 'last_name': 'Новиков', 'middle_name': 'Дмитриевич', 'birth_date': date(2011, 9, 14), 'phone_parent': '+79167890123'},
        {'first_name': 'Виктория', 'last_name': 'Морозова', 'middle_name': 'Александровна', 'birth_date': date(2014, 6, 30), 'phone_parent': '+79168901234'},
        {'first_name': 'Даниил', 'last_name': 'Павлов', 'middle_name': 'Сергеевич', 'birth_date': date(2012, 12, 8), 'phone_parent': '+79169012345'},
        {'first_name': 'Елизавета', 'last_name': 'Семенова', 'middle_name': 'Игоревна', 'birth_date': date(2013, 4, 17), 'phone_parent': '+79160123456'},
    ]
    
    students = []
    for data in students_data:
        student, created = Student.objects.get_or_create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data['middle_name'],
            defaults={
                'birth_date': data['birth_date'],
                'phone_parent': data['phone_parent']
            }
        )
        students.append(student)
        print(f"Студент: {student} ({student.age} лет)")
    
    return students

def create_groups(directions, teachers):
    """Создание групп"""
    groups_data = [
        {'direction': directions[0], 'year_of_study': 1, 'teacher': teachers[0], 'name': 'Фортепиано-1-А', 'schedule': 'Пн, Ср 16:00-17:30'},
        {'direction': directions[0], 'year_of_study': 2, 'teacher': teachers[3], 'name': 'Фортепиано-2-Б', 'schedule': 'Вт, Чт 17:00-18:30'},
        {'direction': directions[1], 'year_of_study': 1, 'teacher': teachers[1], 'name': 'Гитара-1-В', 'schedule': 'Пн, Пт 15:30-17:00'},
        {'direction': directions[1], 'year_of_study': 3, 'teacher': teachers[3], 'name': 'Гитара-3-А', 'schedule': 'Ср, Пт 18:00-19:30'},
        {'direction': directions[2], 'year_of_study': 1, 'teacher': teachers[2], 'name': 'Скрипка-1-Б', 'schedule': 'Вт, Чт 16:30-18:00'},
        {'direction': directions[3], 'year_of_study': 2, 'teacher': teachers[4], 'name': 'Вокал-2-А', 'schedule': 'Пн, Ср 17:30-19:00'},
        {'direction': directions[4], 'year_of_study': 1, 'teacher': teachers[1], 'name': 'Ударные-1-В', 'schedule': 'Чт, Сб 15:00-16:30'},
        {'direction': directions[5], 'year_of_study': 1, 'teacher': teachers[2], 'name': 'Флейта-1-А', 'schedule': 'Ср, Пт 16:00-17:30'},
    ]
    
    groups = []
    for data in groups_data:
        group, created = Group.objects.get_or_create(
            name=data['name'],
            defaults={
                'direction': data['direction'],
                'year_of_study': data['year_of_study'],
                'teacher': data['teacher'],
                'schedule': data['schedule']
            }
        )
        groups.append(group)
        print(f"Группа: {group}")
    
    return groups

def create_enrollments(students, groups):
    """Создание зачислений студентов в группы"""
    enrollments_data = [
        # Фортепиано-1-А
        {'student': students[0], 'group': groups[0]},
        {'student': students[1], 'group': groups[0]},
        {'student': students[2], 'group': groups[0]},
        
        # Фортепиано-2-Б
        {'student': students[3], 'group': groups[1]},
        {'student': students[4], 'group': groups[1]},
        
        # Гитара-1-В
        {'student': students[5], 'group': groups[2]},
        {'student': students[6], 'group': groups[2]},
        {'student': students[7], 'group': groups[2]},
        
        # Гитара-3-А
        {'student': students[8], 'group': groups[3]},
        {'student': students[9], 'group': groups[3]},
        
        # Многопрофильные студенты (учатся на нескольких направлениях)
        {'student': students[0], 'group': groups[2]},  # Соколов на фортепиано и гитаре
        {'student': students[1], 'group': groups[5]},  # Орлова на фортепиано и вокале
        {'student': students[5], 'group': groups[6]},  # Козлова на гитаре и ударных
    ]
    
    enrollments = []
    for data in enrollments_data:
        enrollment, created = Enrollment.objects.get_or_create(
            student=data['student'],
            group=data['group'],
            defaults={'is_active': True}
        )
        enrollments.append(enrollment)
        print(f"Зачисление: {enrollment}")
    
    return enrollments

def main():
    """Основная функция заполнения базы данных"""
    print("=" * 50)
    print("НАЧАЛО ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ МУЗЫКАЛЬНОЙ ШКОЛЫ")
    print("=" * 50)
    
    # Очистка базы данных (осторожно!)
    # Раскомментируйте следующие строки, если хотите очистить базу перед заполнением
    '''
    Enrollment.objects.all().delete()
    Group.objects.all().delete()
    Student.objects.all().delete()
    Teacher.objects.all().delete()
    Direction.objects.all().delete()
    print("База данных очищена")
    '''
    
    try:
        # Создание данных
        directions = create_directions()
        print()
        
        teachers = create_teachers(directions)
        print()
        
        students = create_students()
        print()
        
        groups = create_groups(directions, teachers)
        print()
        
        enrollments = create_enrollments(students, groups)
        print()
        
        print("=" * 50)
        print("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ УСПЕШНО ЗАВЕРШЕНО!")
        print("=" * 50)
        
        # Статистика
        print(f"Создано:")
        print(f"  - Направлений: {len(directions)}")
        print(f"  - Преподавателей: {len(teachers)}")
        print(f"  - Студентов: {len(students)}")
        print(f"  - Групп: {len(groups)}")
        print(f"  - Зачислений: {len(enrollments)}")
        
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()