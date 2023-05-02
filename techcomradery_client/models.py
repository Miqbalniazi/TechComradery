from django.db import models
from django.contrib.auth.models import User
import random
# from django.core.mail import send_mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



def get_referral():
    alpha = random.sample(range(65, 91), 3)
    numeric = random.randint(10000, 99999)
    alpha_ = "".join([chr(i) for i in alpha])
    return alpha_ + "-" + str(numeric)


class SocialMediaUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_media = models.CharField(verbose_name="Social Media", max_length=100, default="techcomradery")
    social_media_id = models.CharField(verbose_name="Social Media ID", max_length=500, default="")
    image_url = models.CharField(verbose_name="Profile Url", max_length=500, default="")

    def __str__(self) -> str:
        return str(self.social_media)


class SubscriptionUser(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    email = models.EmailField(verbose_name="Email", unique=True)
    whatsapp = models.CharField(verbose_name="Whatsapp Number", max_length=50)
    linkedin = models.CharField(verbose_name="LinkedIn", max_length=500)
    providing = models.CharField(verbose_name="Providing", max_length=50)
    referral = models.CharField(verbose_name="Referral ID", max_length=10, default=get_referral, editable=False, unique=True)
    referred_by = models.CharField(verbose_name="Referred by", max_length=10, default="")
        
    def send_email(self, to_address=None):
        smtp_server = 'mail.smtp2go.com'  # replace with your SMTP server hostname
        smtp_port = 2525  # replace with your SMTP server port
        smtp_username = 'support@techcomrad.com'  # replace with your SMTP server username
        smtp_password = '9FdaC1OSbFe4RyBw'  # replace with your SMTP server password

        from_address = 'support@techcomrad.com'  # replace with your email address
        to_address = to_address or self.email    # use the user's email address

        subject = 'Test Email from Python'
        body = 'This is a test email sent through Python!'
        
        

        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(from_address, to_address, msg.as_string())
        smtp_connection.quit()      
        print("Mail sent successfully to", to_address)
    def save(self, *args, **kwargs):
        if not self.id:
            self.send_email()
        super().save(*args, **kwargs)
        self.send_email()  # call send_email method again after save

    @classmethod
    def send_email_to_all_users(cls):
        to_addresses = cls.objects.exclude(email='').exclude(email__isnull=True)
        for user in to_addresses:
           if user.email:  # check if email is not empty
            try:
                user = SubscriptionUser.objects.get(email=user.email)
                # user.send_email()
                # print(f"Email sent to {user.email}")
            except SubscriptionUser.DoesNotExist:
                # handle the error here, for example, log it or skip the iteration
                print(f"User with email {user.email} does not exist")
                pass 
            

SubscriptionUser.send_email_to_all_users()


# user = SubscriptionUser.objects.get(id=1)
# user.send_email()  # will send email to the user's email address stored in the `email` field
# user.send_email("example@gmail.com")  # will send email to the provided email address "example@gmail.com"
# def send_email_to_all_users(cls):
#         to_addresses = cls.objects.values_list('email', flat=True)
#         for email in to_addresses:
#             user = cls.objects.get(email=email)
#             user.send_email(to_address=email)
#             SubscriptionUser.send_email_to_all_users()
           