from flask import Flask, render_template, Markup

import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8


app = Flask(__name__)


def create_figure():
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    y0 = [i ** 2 for i in x]
    y1 = [10 ** i for i in x]
    y2 = [10 ** (i ** 2) for i in x]

    p = figure(
        tools="", # pan,box_zoom,reset,save",
        y_axis_type="log", y_range=[0.001, 10 ** 11], title="log axis example",
        x_axis_label='sections', y_axis_label='particles',
        sizing_mode='stretch_both'
    )

    p.line(x, x, legend="y=x")
    p.circle(x, x, legend="y=x", fill_color="white", size=8)
    p.line(x, y0, legend="y=x^2", line_width=3)
    p.line(x, y1, legend="y=10^x", line_color="red")
    p.circle(x, y1, legend="y=10^x", fill_color="red", line_color="red", size=6)
    p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")

    return p


# Index page
@app.route('/')
def index():
    # Create the plot, and time it
    plot = create_figure()

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("index.html", script=script, div=div)

# @app.route('/')
# def index():
    # plot = figure()
    # x = np.random.randn(100)
    # y = np.random.randn(100)
    # plot.scatter(x, y, size=12, color="purple", alpha=0.5)
    #
    # script, div = components(plot, CDN)
    # script = Markup(script)
    # div = Markup(div)
    # return render_template('index.html',
    #                        plot_script=script, plot_div=div)


@app.route('/bokeh1')
def bokeh1():

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(plot_width=800, plot_height=600)
    fig.vbar(
        x=[1, 2, 3, 4],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'bokeh.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


@app.route('/bokeh2')
def bokeh2():

    # chart defaults
    color = '#FF0000'
    start = 0
    finish = 10

    # Create a polynomial line graph with those arguments
    x = list(range(start, finish + 1))
    fig = figure(title='Polynomial')
    fig.line(x, [i ** 2 for i in x], color=color, line_width=2)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'bokeh.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


if __name__ == '__main__':
    app.run(debug=True)
