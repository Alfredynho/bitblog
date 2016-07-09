from colour_runner.django_runner import ColourRunnerMixin
from django.test.runner import DiscoverRunner


class WarpTestRunner(ColourRunnerMixin, DiscoverRunner):
    pass
