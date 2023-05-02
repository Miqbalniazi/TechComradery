from django.contrib import admin
from .models import MasterQuestion, AskingQuestion, UserResponse, BusinessRequirementDocument, Project, QuestionCategory


class MasterQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'named_id', 'id']
    ordering = ["named_id"]

class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'id']
    ordering = ["id"]

class AskingQuestionAdmin(admin.ModelAdmin):
    list_display = ["asking_question", "master_question", "named_id"]
    ordering = ["named_id"]

class UserResponseAdmin(admin.ModelAdmin):
    list_display = ["answer", "question", "rectify_answer", "social_media_user", "date_time", "brd_id"]
    ordering = ["date_time"]

class BusinessRequirementDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'project', 'date_time']
    ordering = ["date_time"]

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_time']
    ordering = ["date_time"]

admin.site.register(MasterQuestion, MasterQuestionAdmin)
admin.site.register(AskingQuestion, AskingQuestionAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
admin.site.register(BusinessRequirementDocument, BusinessRequirementDocumentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(QuestionCategory, QuestionCategoryAdmin)
