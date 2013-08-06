/*jshint jquery: true, browser: true*/
/*global Spinner: true*/

/*
 * Name space
 */
var CBMONITOR = CBMONITOR || {};


CBMONITOR.Snapshots = function () {
    "use strict";

    this.spinner = new Spinner({width: 4, top: "210px"});

    var that = this;
    $("#add").click(function() {
        that.add();
    });
};

CBMONITOR.Snapshots.prototype.getSnapshots = function () {
    "use strict";

    var that = this;
    $.ajax({url: "/cbmonitor/get_snapshots/", dataType: "json",
        success: function(snapshots){
            var sel = $("#snapshot");
            sel.empty();
            if (snapshots.length) {
                snapshots.forEach(function(snapshot) {
                    var o = new Option(snapshot, snapshot);
                    sel.append(o);
                });
                $("#plot").click(function() {
                    that.plot();
                });
                $("#pdf").click(function() {
                    that.pdf();
                });
            } else {
                $("#plot").addClass("disabled");
                $("#pdf").addClass("disabled");
                var o = new Option("None", "");
                sel.append(o);
            }
        }
    });
};

CBMONITOR.Snapshots.prototype.getReportTypes = function () {
    "use strict";

    $.ajax({url: "/cbmonitor/get_report_types/", dataType: "json",
        success: function(types){
            types.forEach(function(type) {
                var o = new Option(type, type);
                $("#report").append(o);
            });
        }
    });
};

CBMONITOR.Snapshots.prototype.add = function () {
    "use strict";

    $("#add_new_snapshot").dialog("open");
};

CBMONITOR.Snapshots.prototype.pdf = function () {
    "use strict";

    var snapshot = $("#snapshot").find(":selected").text(),
        report = $("#report").find(":selected").text();

    this.spinner.spin(document.getElementById("spinner"));

    var that = this;
    $.ajax({url: "/cbmonitor/pdf/", type: "POST",
        data: {snapshot: snapshot, report: report},
        success: function(url) {
            that.spinner.stop();
            window.location = url;
        },
        error: function() {
            that.spinner.stop();
            window.alert("Fail to export snapshot");
        }
    });
};

CBMONITOR.Snapshots.prototype.plot = function (snapshot) {
    "use strict";

    if (snapshot === undefined) {
        snapshot = $("#snapshot").find(":selected").text();
    }
    var report = $("#report").find(":selected").text();

    this.spinner.spin(document.getElementById("spinner"));

    $(".carousel").css("display", "none");
    $(".titles").css("display", "none");
    var that = this;
    $.ajax({url: "/cbmonitor/plot/", dataType: "json", type: "POST",
        data: {snapshot: snapshot, report: report},
        success: function(images) {
            that.spinner.stop();
            $("#titles").empty();
            if (images.length) {
                $.each(images, function(index, value) {
                    that.addLink(index, value[0]);
                    that.addIndicator(index);
                    that.addItem(index, value[1]);
                });
                $("#carousel-indicator0").addClass("active");
                $("#carousel-item0").addClass("active");
                $('.carousel').carousel({
                    interval: false
                });
                $(".carousel").css("display", "block");
                $(".titles").css("display", "block");
            }
        },
        error: function() {
            that.spinner.stop();
            window.alert("Fail to export snapshot");
        }
    });
};

CBMONITOR.Snapshots.prototype.addLink = function (index, title) {
    "use strict";

    $("#titles").append(
        $("<a>")
            .append(title)
            .attr("href", "#")
            .click(function() {
                $('.carousel').carousel(index);
            })
    ).append("<br>");
};

CBMONITOR.Snapshots.prototype.addIndicator = function (index) {
    "use strict";

    $(".carousel-indicators").append(
        $("<li>")
            .attr("id", "carousel-indicator" + index)
            .attr("data-target", "#carousel")
            .attr("data-slide-to", index.toString())
    );
};

CBMONITOR.Snapshots.prototype.addItem = function (index, url) {
    "use strict";

    $(".carousel-inner").append(
        $("<div>")
            .addClass("item")
            .attr("id", "carousel-item" + index)
            .append($("<img>").attr("src", url))
    );
};

CBMONITOR.Snapshots.prototype.autoPlot = function () {
    "use strict";

    var snapshot = this.getSnapshotFromURL();
    if (snapshot !== null) {
        this.plot(snapshot);
    }
};


CBMONITOR.Snapshots.prototype.getSnapshotFromURL = function() {
    "use strict";

    var query = document.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0; i<vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] === "snapshot") {
            return pair[1];
        }
    }
    return null;
};

$(document).ready(function(){
    "use strict";

    CBMONITOR.snapshots = new CBMONITOR.Snapshots();
    CBMONITOR.snapshots.getSnapshots();
    CBMONITOR.snapshots.getReportTypes();
    CBMONITOR.snapshots.autoPlot();

    CBMONITOR.dialogs = new CBMONITOR.Dialogs();
    CBMONITOR.dialogs.configureAddNewSnapshot();
});