from pathlib import Path
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured
from html2text import html2text


class HTMLEmailTemplate(object):
    subject = ''
    template_name = None

    def __init__(self, from_email=None, to=None, bcc=None, attachments=None, headers=None,
                 alternatives=None, cc=None, reply_to=None, context=None):
        self.from_email = from_email
        self.to = to
        self.bcc = bcc
        if attachments:
            self.attachments = attachments
        else:
            self.attachments = []
        self.headers = headers
        self.alternatives = alternatives
        self.cc = cc
        self.reply_to = reply_to
        self.context = context

    def get_subject(self):
        return self.subject

    def get_template_name(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "HTMLMessage requires a definitions of 'template_name'"
                "or an implementation of 'get_template_name()'"
            )
        return self.template_name

    def attach_file(self, path, mimetype=None):
        path = Path(path)
        with path.open('rb') as f:
            content = f.read()
            self.attachments.append((path.name, content, mimetype))

    def get_html_body(self):
        return render_to_string(self.get_template_name(), self.context)

    def get_mail(self):
        html_body = self.get_html_body()
        mail = EmailMultiAlternatives(
            subject=self.get_subject(),
            body=html2text(html_body),
            from_email=self.from_email,
            to=self.to,
            attachments=self.attachments
        )
        mail.attach_alternative(html_body, 'text/html')
        return mail

    def send(self, fail_silently=False):
        return self.get_mail().send(fail_silently=fail_silently)

