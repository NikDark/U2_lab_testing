from datetime import datetime

from django.http.response import Http404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.fast import FastLimitOffsetPagination
from apps.core.fast.utils import get_fast_response
from apps.core.utils import format_error_response
from apps.parse.api.serializers import CHAPTER_FIELDS, MANGA_FIELDS
from apps.parse.const import CHAPTER_PARSER, DETAIL_PARSER, IMAGE_PARSER
from apps.parse.models import Manga
from apps.parse.scrapy.utils import run_parser
from apps.parse.utils import fast_annotate_manga_query, needs_update


class MangaViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = FastLimitOffsetPagination
    queryset = Manga.objects.all()

    @classmethod
    def get_fast_manga(cls, pk) -> dict:
        manga = fast_annotate_manga_query(Manga.objects.filter(pk=pk))
        if not manga.exists():
            raise Http404
        return manga.parse_values(*MANGA_FIELDS)[0]

    def retrieve(self, _, pk, *args, **kwargs):
        manga = Manga.objects.filter(pk=pk).parse_values(*MANGA_FIELDS)[0]
        try:
            criterea = manga["updated_detail"]
            if not criterea or needs_update(criterea):
                run_parser(DETAIL_PARSER, "readmanga", manga["source_url"])
                run_parser(CHAPTER_PARSER, "readmanga", manga["source_url"])
                now = datetime.now()
                Manga.objects.filter(pk=pk).update(updated_detail=now)
                manga["updated_detail"] = now
                return Response({"message": "Manga is updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return format_error_response("Errors occurred during parsing " + str(e))
        return get_fast_response(manga)

    def list(self, request):
        title: str = request.GET.get("title", None)
        if not title:
            return format_error_response("No title found")

        mangas = Manga.objects.filter(title__icontains=title).all()

        page = self.paginator.paginate_queryset(
            mangas,
            request,
            values=MANGA_FIELDS,
        )
        if page is not None:
            return self.paginator.get_paginated_response(page)

        return Response(list(mangas.parse_values(*MANGA_FIELDS)), status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<pk>[^/.]+)/chapters",
    )
    def chapters_list(self, _, pk):
        manga: Manga = Manga.objects.prefetch_related("chapters").get(pk=pk)

        try:
            criterea = manga.updated_detail
            if not criterea or needs_update(criterea.isoformat()):
                run_parser(DETAIL_PARSER, manga.source, manga.source_url)
                run_parser(CHAPTER_PARSER, manga.source, manga.source_url)
                manga.updated_detail = datetime.now()
                manga.save()
        except Exception as e:
            return format_error_response("Errors occurred during parsing " + str(e))
        return get_fast_response(
            list(manga.chapters.order_by("-volume", "-number").values(*CHAPTER_FIELDS))
        )

