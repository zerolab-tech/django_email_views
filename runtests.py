import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


def run_tests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    django.setup()
    failures = test_runner.run_tests([])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
