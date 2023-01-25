from copy import deepcopy
from typing import Optional

import plotly.graph_objects as go


def format_pct(v):
    return int(round(v * 100))
def format_round(v, dec=2):
    return round(v*(10**dec))/(10**dec)

def define_label(v: float, cuts: list, labs: list):
    
    assert len(labs) == len(cuts) + 1
    
    if v < cuts[0]:
        return labs[0]
    for i in range(0, len(cuts)-1):
        if v >= cuts[i] and v <= cuts[i+1]:
            return labs[i+1]
    if v > cuts[-1]:
        return labs[-1]


def get_tx_from_nb(likert_nb):
    likert_tx = deepcopy(likert_nb)
    for mes in likert_tx.keys():
        for mod in likert_tx[mes].keys():
            l = likert_tx[mes][mod]
            likert_tx[mes][mod] = [round(v/sum(l)*100) for v in l]
    return likert_tx



def highlight_corr(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    if val > 0.6 and val < 1:
        return 'color: black; background-color: yellow'
    if val >= 0.5 and val <= 0.6:
        return 'color: black; background-color: pink'
    if val <= -0.2:
        return 'color: white; background-color: red' 
    return ''


def plot_horizontal_barchart(categories: list[str], values: dict, top_labels: list[str], 
                            inv_values: bool=False, inv_cats: bool = False, inv_labels: bool = False, pct: bool = False, title: Optional[str]=None):
    
    # top_labels = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree',
    #           'Strongly<br>disagree']

    # x_data = [[21, 30, 21, 16, 12],
    #         [24, 31, 19, 15, 11],
    #         [27, 26, 23, 11, 13],
    #         [29, 24, 15, 18, 14]]

    # y_data = ['The course was effectively<br>organized',
    #         'The course developed my<br>abilities and skills ' +
    #         'for<br>the subject', 'The course developed ' +
    #         'my<br>ability to think critically about<br>the subject',
    #         'I would recommend this<br>course to a friend']

    categories = categories[::-1] if inv_cats else categories
    top_labels = top_labels[::-1] if inv_labels else top_labels
    x_data = [values[c][::-1] for c in categories] if inv_values else [values[c] for c in categories]
    y_data = categories
    

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
            'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
            'rgba(190, 192, 213, 1)']


    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                        color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%'*pct,
                                font=dict(family='Arial', size=14,
                                        color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=14,
                                            color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i]/2), y=yd,
                                        text=str(xd[i]) + '%'*pct,
                                        font=dict(family='Arial', size=14,
                                                color='rgb(248, 248, 255)'),
                                        showarrow=False))
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(dict(xref='x', yref='paper',
                                            x=space + (xd[i]/2), y=1.1,
                                            text=top_labels[i],
                                            font=dict(family='Arial', size=14,
                                                    color='rgb(67, 67, 67)'),
                                            showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)
    if title is not None:
        fig.update_layout(title=title)

    fig.show()
