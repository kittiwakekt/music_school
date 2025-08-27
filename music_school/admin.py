from django.contrib import admin
from django.utils.html import format_html
from .models import Direction, Teacher, Student, Group, Enrollment

# Inline-модели для отображения связей
class GroupInline(admin.TabularInline):
    """Inline для отображения групп в направлении"""
    model = Group
    extra = 0
    fields = ('name', 'year_of_study', 'teacher', 'schedule')
    readonly_fields = ('name', 'year_of_study', 'teacher', 'schedule')
    can_delete = False
    max_num = 0
    show_change_link = True

class EnrollmentInline(admin.TabularInline):
    """Inline для отображения зачислений в группе"""
    model = Enrollment
    extra = 0
    fields = ('student', 'date_joined', 'is_active')
    readonly_fields = ('date_joined',)
    show_change_link = True

class StudentGroupsInline(admin.TabularInline):
    """Inline для отображения групп студента через зачисления"""
    model = Enrollment
    extra = 0
    fields = ('group', 'date_joined', 'is_active')
    readonly_fields = ('date_joined', 'group')
    can_delete = False
    max_num = 0
    show_change_link = True

# Фильтры для админки
class YearOfStudyFilter(admin.SimpleListFilter):
    """Фильтр по году обучения для групп"""
    title = 'Год обучения'
    parameter_name = 'year_of_study'

    def lookups(self, request, model_admin):
        return [
            ('1', '1 год'),
            ('2', '2 год'),
            ('3', '3 год'),
            ('4', '4+ год'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '4':
            return queryset.filter(year_of_study__gte=4)
        if self.value():
            return queryset.filter(year_of_study=self.value())

class ActiveStatusFilter(admin.SimpleListFilter):
    """Фильтр по активному статусу"""
    title = 'Активный статус'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return [
            ('active', 'Активные'),
            ('inactive', 'Неактивные'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)

# Модели админки
@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'years_of_study', 'teachers_count', 'groups_count')
    list_filter = ('years_of_study',)
    search_fields = ('name', 'description')
    readonly_fields = ('teachers_count', 'groups_count')
    inlines = [GroupInline]
    
    def teachers_count(self, obj):
        return obj.teachers.count()
    teachers_count.short_description = 'Кол-во преподавателей'
    
    def groups_count(self, obj):
        return obj.groups.count()
    groups_count.short_description = 'Кол-во групп'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'directions_list', 'active_groups_count', 'is_active')
    list_filter = ('is_active', 'directions')
    search_fields = ('last_name', 'first_name', 'middle_name')
    filter_horizontal = ('directions',)
    readonly_fields = ('active_groups_count',)
    
    def directions_list(self, obj):
        return ", ".join([d.name for d in obj.directions.all()])
    directions_list.short_description = 'Направления'
    
    def active_groups_count(self, obj):
        return obj.groups.count()
    active_groups_count.short_description = 'Кол-во групп'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'age', 'phone_parent', 'active_groups_count')
    list_filter = (ActiveStatusFilter,)
    search_fields = ('last_name', 'first_name', 'middle_name', 'phone_parent')
    readonly_fields = ('age', 'active_groups_count')
    inlines = [StudentGroupsInline]
    
    def active_groups_count(self, obj):
        return obj.enrollment_set.filter(is_active=True).count()
    active_groups_count.short_description = 'Активных групп'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'year_of_study', 'teacher', 'students_count', 'schedule')
    list_filter = ('direction', YearOfStudyFilter, 'teacher')
    search_fields = ('name', 'direction__name', 'teacher__last_name')
    readonly_fields = ('students_count',)
    inlines = [EnrollmentInline]
    
    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = 'Кол-во студентов'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'date_joined', 'is_active', 'duration_days')
    list_filter = ('is_active', 'date_joined', 'group__direction')
    search_fields = ('student__last_name', 'student__first_name', 'group__name')
    readonly_fields = ('date_joined', 'duration_days')
    list_editable = ('is_active',)
    
    def duration_days(self, obj):
        from datetime import date
        if obj.date_joined:
            delta = date.today() - obj.date_joined
            return delta.days
        return 0
    duration_days.short_description = 'Дней в группе'

# Дополнительные настройки админки
admin.site.site_header = 'Панель управления Музыкальной школой'
admin.site.site_title = 'Музыкальная школа'
admin.site.index_title = 'Администрирование системы'
