from django.db import connection
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FootballField
from .serializers import FootballFieldSerializer


class FootballFieldViewSet(viewsets.ModelViewSet):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff and user.role != "manager":
            return FootballField.objects.filter(is_active=True)
        return FootballField.objects.all()


class CustomFieldViewSet(APIView):

    def get(self, request, format=None):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            start_time = request.query_params.get('start_time')
            end_time = request.query_params.get('end_time')

            filter_query = []
            if start_time:
                filter_query.append(f" f.start_time < '{start_time}'")
            if end_time:
                filter_query.append(f" f.end_time < '{end_time}'")

            filter_clause = " WHERE " + " AND ".join(filter_query) if filter_query else ""

            raw_query = f"""
                SELECT * FROM (
                    SELECT COUNT(*) as count_group, group_id 
                    FROM football_field f
                    {filter_clause}
                    GROUP BY group_id
                ) q
                WHERE q.count_group > 15
                LIMIT {page_size} OFFSET {page_size} * ({page} - 1)
            """

            result = []
            with connection.cursor() as cursor:
                cursor.execute(raw_query)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]

            total_count = len(result)  # `cursor.rowcount` o‘rniga
            total_pages = (total_count + page_size - 1) // page_size

            res = {
                "page": page,
                "page_size": page_size,
                "count": total_count,
                "results": result,
                "total_pages": total_pages,
                "total_count": total_count,
            }
            return Response(res, status=200)

        except Exception as e:
            line = e.__traceback__.tb_lineno
            return Response({"error": f"An error occurred at line {line}. {str(e)}"}, status=500)
