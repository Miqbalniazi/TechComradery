from django.db import models
from techcomradery_client.models import SocialMediaUser
import uuid
from datetime import datetime
from django.utils.timezone import make_aware


class QuestionCategory(models.Model):
    category = models.CharField(verbose_name="Category Name", max_length=100, default="")

    def __str__(self) -> str:
        return self.category
    

class MasterQuestion(models.Model):
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, verbose_name="Category")
    question = models.CharField("Master Question", max_length=200)
    named_id = models.CharField(verbose_name="Question ID", max_length=10, default="0")

    def __str__(self) -> str:
        return self.question


class AskingQuestion(models.Model):
    master_question = models.ForeignKey(MasterQuestion, on_delete=models.CASCADE, verbose_name="Parent Question")
    asking_question = models.CharField(verbose_name="Asking Question", max_length=500)
    named_id = models.CharField(verbose_name="Question ID", max_length=10, default="0")

    def __str__(self) -> str:
        return self.asking_question
    

class Project(models.Model):
    id = models.UUIDField(verbose_name="Project ID", default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name = models.CharField(verbose_name="Project Name", default="", max_length=100)
    date_time = models.DateTimeField(verbose_name="Created Date Time", default=make_aware(datetime.now()), editable=False)

    def __str__(self) -> str:
        return self.name


class BusinessRequirementDocument(models.Model):
    id = models.UUIDField(verbose_name="BRD ID", default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project Name", default="")
    name = models.CharField(verbose_name="BRD Name", default="", max_length=100)
    date_time = models.DateTimeField(verbose_name="Created Date Time", default=make_aware(datetime.now()), editable=False)

    def __str__(self) -> str:
        return str(self.name)


class UserResponse(models.Model):
    id = models.UUIDField(verbose_name="Response ID", default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    brd_id = models.ForeignKey(BusinessRequirementDocument, on_delete=models.CASCADE, verbose_name="BRD_ID", default="")
    social_media_user = models.ForeignKey(SocialMediaUser, on_delete=models.CASCADE, verbose_name="Social Media User")
    question = models.ForeignKey(AskingQuestion, verbose_name="Asking Question", on_delete=models.CASCADE)
    answer = models.CharField(verbose_name="User Answer", max_length=1000)
    rectify_answer = models.CharField(verbose_name="Rectify Answer", max_length=1000)
    date_time = models.DateTimeField(verbose_name="Response Time", default=make_aware(datetime.now()), editable=False)

    def __str__(self) -> str:
        return self.answer