#!/usr/bin/env python
from django.contrib import admin
from expenses.models import Category, Expense

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'amount', 'date')
    date_hierarchy = 'date'
    search_fields = ('category__name', 'description')
    list_filter = ('category',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)