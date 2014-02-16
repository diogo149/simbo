import nvd3
import BeautifulSoup


def js_extract(html):
    bs = BeautifulSoup.BeautifulSoup(html)
    script = bs.find("script")
    return script.contents[0]


def pie_chart(labels, data, label=""):
    chart = nvd3.pieChart(name="",
                          color_category='category20c',
                          height=450, width=450)
    chart.jquery_on_ready = True

    #Add the serie
    extra_serie = {"tooltip": {"y_start": "", "y_end": label}}
    chart.add_serie(y=data, x=labels, extra=extra_serie)
    chart.buildcontent()
    # assuming name is hardcoded to ""
    return js_extract(chart.htmlcontent).replace("# svg", "#importances_graph")


def scatter_chart(xs, ys, labels):
    chart = nvd3.scatterChart(name="", height=350, x_is_date=False)
    extra_serie = {"tooltip": {"y_start": "", "y_end": "value"}}
    for x, y, label in zip(xs, ys, labels):
        chart.add_serie(name=label, y=y, x=x, extra=extra_serie)
    chart.buildcontent()
    # assuming name is hardcoded to ""
    return js_extract(chart.htmlcontent).replace("# svg", "#results_graph")
