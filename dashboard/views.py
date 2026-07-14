import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import get_kpis, get_chart_data


@login_required
def index(request):
    kpis = get_kpis()
    charts = get_chart_data()
    return render(request, "dashboard/index.html", {
        "kpis": kpis,
        "charts_json": json.dumps(charts),
    })
