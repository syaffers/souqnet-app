import random
from math import pi

from numpy import squeeze
from bokeh.models import HoverTool
from bokeh.embed import components
from bokeh.plotting import figure

LETTER_SET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
IMAGE_LABELS = ['Headphone', 'Mouse', 'Camera', 'Smartphone',
                'Glasses', 'Shoes', 'Watch', 'Laptop']

def random_name(filename):
    """Generate a random name for an uploaded file."""
    ext = filename.split('.')[-1]
    rns = [random.randint(0, len(LETTER_SET)) for _ in range(3)]
    name = ''.join([LETTER_SET[rn] for rn in rns])
    return "{new_fn}.{ext}".format(new_fn=name, ext=ext)


def generate_barplot(predictions):
    """Generates script and `div` element of bar plot of predictions using
    bokeh
    """
    # TODO: Add hover functionality
    plot = figure(x_range=IMAGE_LABELS, plot_height=300, plot_width=400)
    plot.vbar(x=IMAGE_LABELS, top=squeeze(predictions), width=0.8, bottom=0)
    plot.xaxis.major_label_orientation = pi / 2.

    return components(plot)
