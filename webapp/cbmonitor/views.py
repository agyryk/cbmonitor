from django.http import Http404
from django.shortcuts import render_to_response, redirect

from cbmonitor import models
from cbmonitor.plotter import Plotter
from cbmonitor.reports import Report


def index(request):
    return render_to_response("charts.jade", {"charts": True})


def inventory(request):
    clusters = []

    for cluster in models.Cluster.objects.all():
        servers = models.Server.objects.filter(cluster=cluster).values()
        servers = [s["address"] for s in servers]
        buckets = models.Bucket.objects.filter(cluster=cluster).values()
        buckets = [b["name"] for b in buckets]
        clusters.append((
            cluster.name,
            ", ".join(servers),
            ", ".join(buckets),
            cluster.description
        ))

    return render_to_response("inventory.jade", {"clusters": clusters})


def get_plotter_and_metrics(params):
    snapshots = []
    if "all_data" in params.getlist("snapshot"):
        for cluster in params.getlist("cluster"):
            snapshots.append((
                type("snapshot", (object, ), {"name": "all_data"})(),
                cluster
            ))
    else:
        for snapshot in params.getlist("snapshot"):
            snapshot = models.Snapshot.objects.get(name=snapshot)
            snapshots.append((snapshot, snapshot.cluster))
    plotter = Plotter()
    metrics = Report(snapshots, params["report"])
    return plotter, metrics


def render_png(params):
    plotter, metrics = get_plotter_and_metrics(params)
    plotter.plot(metrics)
    id_from_url = lambda url: url.split("/")[2].split(".")[0]
    return [(id_from_url(url), title, url) for title, url in plotter.urls]


def html_report(request):
    urls = render_png(request.GET)
    if urls:
        return render_to_response("report.jade", {"urls": urls})
    else:
        raise Http404
