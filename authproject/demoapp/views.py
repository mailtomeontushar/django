from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# imports related to html emails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string # send data from view to template
from django.utils.html import strip_tags # to process the html

# Create your views here.
def main(request):
    return render(
        request,
        "base.html",
        {
            'home':"This is Home Page",
            'title':'Home-Page'
        }
    )

def createaccount(request):
    if request.method == "GET":
        return render(
            request,
            "createaccount.html",
            {
                'title':'Create-Account'
            }
        )
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = email
        )

        obj.set_password(password)
        obj.save()
        # SIMPLE EMAIL
        # # send the email
        # send_mail(
        #     # subject
        #     "Welcome Mail",
        #     # msg
        #     "Welcome to the world of Python and Django",
        #     # from email
        #     settings.EMAIL_HOST_USER,
        #     # list of to emails
        #     [email]
        # )

        # HTML EMAIL
        html_content = render_to_string(
            # template name
            "myemail.html",
            # context
            {
                "name":first_name + " " + last_name
            }
        )
        text_content = strip_tags(html_content)
        mail = EmailMultiAlternatives(
            #subject
            "Welcome Mail",
            # msg
            text_content,
            # from email
            settings.EMAIL_HOST_USER,
            # to email
            [email]
        )
        mail.attach_alternative(html_content,"text/html")
        mail.send()
        return render(
            request,
            "createaccount.html",
            {
                'title':'Create-Account',
                'msg':'Account Created'
            }
        )
@login_required
def securepage(request):
    return render(
        request,
        "securepage.html",
        {
            'title':'secure page'
        }
    )