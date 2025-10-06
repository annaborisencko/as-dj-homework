from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            form.cleaned_data
            if form.cleaned_data.get('is_main') == True:
                is_main_count += 1
            if is_main_count > 1:
                raise ValidationError('Основным может быть только один тег')
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if is_main_count == 0:
            raise ValidationError('Добавьте основной тег')
        return super().clean()  # вызываем базовый код переопределяемого метода

class ScopeInline(admin.TabularInline):
    model=Scope
    formset = ScopeInlineFormset

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['name']
    list_display_links=['name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=['title', 'published_at']
    list_display_links=['title']
    inlines=[ScopeInline]

