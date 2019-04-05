import os
from django.test import TestCase, override_settings
from django.core import mail
from django.conf import settings
from email_views.emails import HTMLEmailTemplate


class TestMessage(HTMLEmailTemplate):
    subject = 'test subject'
    template_name = 'dummy.html'


class TestCore(TestCase):
    def setUp(self):
        pass

    def test_sending(self):
        message = TestMessage(from_email='test@domain.tld', to=['to@domain.tld'], context={'var': 'world'})
        result = message.send()
        self.assertEqual(result, 1)
        self.assertEqual(len(mail.outbox), 1)
        email_message = mail.outbox[0]
        self.assertEqual(email_message.subject, 'test subject')
        self.assertEqual(len(email_message.alternatives), 1)
        self.assertEqual(email_message.alternatives[0][1], 'text/html')
        html = email_message.alternatives[0][0]
        self.assertEqual(html, 'hello_world')
        self.assertEqual(email_message.body, 'hello_world\n\n')
        self.assertEqual(email_message.to, ['to@domain.tld'])
        self.assertEqual(email_message.from_email, 'test@domain.tld')

    def test_attach_file(self):
        message = TestMessage(to=['to@domain.tld'])
        message.attach_file(os.path.join(settings.BASE_DIR, 'tests/templates/dummy_attachment'), 'text/plain')
        message.send()
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        attachment = mail.outbox[0].attachments[0]
        self.assertEqual(attachment[0], 'dummy_attachment')
        self.assertEqual(attachment[1], 'dummy text')
        self.assertEqual(attachment[2], 'text/plain')
