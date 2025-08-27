from django.db import models

class Direction(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name='Название направления',
        unique=True
    )
    years_of_study = models.PositiveSmallIntegerField(
        verbose_name='Количество лет обучения'
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание направления'
    )
    
    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.years_of_study} год(а))"
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name='Отчество'
    )
    directions = models.ManyToManyField(
        Direction,
        related_name='teachers',
        verbose_name='Направления'
    )
    is_active = models.BooleanField(default=True, verbose_name='Преподаёт')
    
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name[0]}.{self.middle_name[0] + '.' if self.middle_name else ''}"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name='Отчество'
    )
    birth_date = models.DateField(verbose_name='Дата рождения')
    phone_parent = models.CharField(
        max_length=20, 
        verbose_name='Телефон родителя'
    )
    
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
class Group(models.Model):
    direction = models.ForeignKey(
        Direction,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name='Направление'
    )
    year_of_study = models.PositiveSmallIntegerField(verbose_name='Год обучения')
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='groups',
        verbose_name='Преподаватель'
    )
    students = models.ManyToManyField(
        Student,
        through='Enrollment',
        through_fields=('group', 'student'),
        verbose_name='Студенты'
    )
    name = models.CharField(max_length=100, verbose_name='Название группы')
    schedule = models.CharField(max_length=200, verbose_name='Расписание')
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['direction', 'year_of_study', 'name']
        unique_together = ['direction', 'year_of_study', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.direction.name}, {self.year_of_study} год)"
    
    def save(self, *args, **kwargs):
        # Валидация: год обучения не может превышать общее количество лет по направлению
        if self.year_of_study > self.direction.years_of_study:
            raise ValueError("Год обучения не может превышать общее количество лет по направлению")
        super().save(*args, **kwargs)

class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        verbose_name='Студент'
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    date_joined = models.DateField(
        auto_now_add=True,
        verbose_name='Дата зачисления'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активное обучение'
    )
    
    class Meta:
        verbose_name = 'Зачисление'
        verbose_name_plural = 'Зачисления'
        unique_together = ['student', 'group']
    
    def __str__(self):
        status = "активно" if self.is_active else "неактивно"
        return f"{self.student} -> {self.group} ({status})"
    
