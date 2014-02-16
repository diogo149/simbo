import nvd3
import BeautifulSoup

"""
from nvd3 import pieChart

type = 'pieChart'
chart = pieChart(name=type, color_category='category20c', height=450, width=450)
chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")

#Create the keys
xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
ydata = [3, 4, 0, 1, 5, 7, 3]

#Add the serie
extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
chart.buildcontent()
chart.htmlcontent

"""


def js_extract(html):
    bs = BeautifulSoup.BeautifulSoup(html)
    script = bs.find("script")
    # assuming name is hardcoded to ""
    return script.contents[0].replace("# svg", "#chart")


def pie_chart(labels, data, label=""):
    chart = nvd3.pieChart(name="",
                          color_category='category20c',
                          height=450, width=450)
    chart.jquery_on_ready = True

    #Add the serie
    extra_serie = {"tooltip": {"y_start": "", "y_end": label}}
    chart.add_serie(y=data, x=labels, extra=extra_serie)
    chart.buildcontent()
    return js_extract(chart.htmlcontent)


def scatter_chart(x, y, label=""):
    chart = nvd3.scatterChart(name="", height=350, x_is_date=False)
    extra_serie = {"tooltip": {"y_start": "", "y_end": label}}
    chart.add_serie(name="serie 1", y=y, x=x, extra=extra_serie)
    chart.buildcontent()
    return js_extract(chart.htmlcontent)
