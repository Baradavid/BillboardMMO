from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Reply


@shared_task
def notify_about_reply(pk):  # оповещаем автора объявления об отклике
    reply = Reply.objects.get(pk=pk)
    html_content = render_to_string(
        'reply_created_email.html',
        {
            'reply': reply,
            'link': f'{settings.SITE_URL}/post/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{reply.author} {reply.reply_date_creation}',
        body=reply.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reply.reply_post.auhtor.email],
    )
    msg.attach_alternative(html_content, 'text/html')

    msg.send()


@shared_task
def notify_about_reply_accept(pk):  # оповещаем автора отклика о принятии
    rply = Reply.objects.get(pk=pk)
    html_content = render_to_string(
        'reply_accept.html',
        {
            'reply': rply,
            'link': f'{settings.SITE_URL}/post/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Здравствуйте, {rply.reply_user}',
        body=rply.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[rply.reply_user.email],
    )
    msg.attach_alternative(html_content, 'text/html')

    msg.send()