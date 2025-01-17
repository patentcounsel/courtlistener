"""
    Hopefully this makes slicing out production data simpler.
"""
import calendar
import random
import time
import traceback

from django.core import serializers
from django.db.models.query_utils import Q

from cl.lib.command_utils import VerboseCommand
from cl.search.models import Docket, Opinion, OpinionCluster, OpinionsCited

SUPPORTED_MODELS = (Docket, OpinionCluster, Opinion, OpinionsCited)


class Command(VerboseCommand):
    help = "CL-specific data dumper for making fixtures from production"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", type=int, default=10, help="Number of items in the export"
        )
        parser.add_argument(
            "--format",
            type=str,
            default="json",
            help="Serialization format [json, xml, yaml]",
        )

    def handle(self, *args, **options):
        super().handle(*args, **options)
        n = options["n"]
        fmt = options["format"]

        self.stdout.write(
            f"Generating dump of up to {n} randomly selected Opinions..."
        )

        pks, cluster_pks = self._select_pks(n)
        if n > len(pks):
            self.stdout.write(
                f" n > number of Opinions, serializing all (n={len(pks)})"
            )

        try:
            self._serialize(Opinion, fmt, Q(id__in=pks))

            self._serialize(
                OpinionsCited,
                fmt,
                Q(citing_opinion__in=pks) | Q(cited_opinion__in=pks),
            )

            self._serialize(OpinionCluster, fmt, Q(id__in=cluster_pks))
            self._serialize(Docket, fmt, Q(clusters__in=cluster_pks))

            self.stdout.write("Done!")

        except Exception as e:
            self.stderr.write(f"Failed to serialize: {e}")
            if options["traceback"]:
                traceback.print_exc()

    @staticmethod
    def _select_pks(sample_size: int):
        """
        Select a random sampling of Opinions from the database.

        Attributes:
            sample_size -- number of Opinions to sample
        """
        n = sample_size
        pk_qs = Opinion.objects.values_list("id", flat=True)
        if pk_qs.count() < sample_size:
            n = pk_qs.count()

        random.seed(calendar.timegm(time.gmtime()))
        pks = random.sample(pk_qs, n)
        cluster_pks = OpinionCluster.objects.filter(
            sub_opinions__in=pks
        ).values_list("id", flat=True)

        return pks, cluster_pks

    def _serialize(self, model, format, filter):
        """
        Helper method for performing the serialization to file of CL models.

        Attributes:
            model -- supported CourtListener model class
            format -- supported Django serizliation format ('json', 'xml'...)
            filter -- Django QuerySet filter
        """
        if model not in SUPPORTED_MODELS:
            raise ModelTypeError(model)

        modelname = model.__name__
        filename = f"{modelname}.{format}"
        self.stdout.write(f" writing {modelname}s to {filename}...")

        with open(filename, "w") as stream:
            serializers.serialize(
                format, model.objects.filter(filter), stream=stream
            )


class ModelTypeError(TypeError):
    """
    Exception for providing invalid CourtListener model types when serializing
    """

    def __init__(self, model):
        self.model = model

    def __str__(self) -> str:
        return f"{self.model} is not a valid CourtListnener model"
