from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope
from django.forms import BaseInlineFormSet


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0

        for form in self.forms:
            if self.deleted_forms and self._should_delete_form(form):
                continue

            if form.cleaned_data and 'is_main' in form.cleaned_data:
                if form.cleaned_data['is_main']:
                    count += 1

        if count > 1:
            raise ValidationError('Основным должен быть только один раздел')

        if count == 0:
            raise ValidationError('Укажите основной раздел')

        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


