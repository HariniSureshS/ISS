import networkx as nx
import plotly
import plotly.graph_objs as go
import json


def generate_graph_from_relation(pairs):
    edges = []
    nodes = []
    edges_labels = {}

    for index in range(len(pairs)):
        node_a = pairs[index][0]  # subject
        node_b = pairs[index][2]  # object
        pair = (node_a, node_b)
        edges.append(pair)
        nodes.append(node_a)
        nodes.append(node_b)
        rel = {pair: pairs[index][1]}  # relation
        edges_labels.update(rel)

    nodes = list(set(nodes))
    G = nx.DiGraph()
    G.add_edges_from(edges)
    G.add_nodes_from(nodes)
    node_positions = nx.spring_layout(G, k = 1.0)
    node_x = []
    node_y = []
    node_text = []

    for node in node_positions:
        x, y = node_positions[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x = node_x,
        y = node_y,
        text = node_text,
        mode = 'markers + text',
        textposition = 'top center',
        textfont = dict(
            family = 'arial',
            size = 10,
            color = 'rgb(0,0,0)'
        ),
        hoverinfo = 'none',
        marker = go.Marker(
                showscale = False,
                color = 'rgb(200,0,0)',
                size = 14,
                line = go.Line(width = 1, color = 'rgb(0,0,0)')))

    edge_x = []
    edge_y = []
    plot_weights = []

    for edge in G.edges:
        x0, y0 = node_positions[edge[0]]
        x1, y1 = node_positions[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        ax = (x0+x1)/2
        ay = (y0+y1)/2
        plot_weights.append((edges_labels[edge], ax, ay))

    annotations_list = [
                        dict(   
                            x = plot_weight[1],
                            y = plot_weight[2],
                            xref = 'x',
                            yref = 'y',
                            text = plot_weight[0],
                            showarrow = True,
                            arrowhead = 7,
                            ax = plot_weight[1],
                            ay = plot_weight[2]
                        ) 
                        for plot_weight in plot_weights
    ]

    # The edges will be drawn as lines:
    edge_trace = go.Scatter(
        x = edge_x,
        y = edge_y,
        line = go.Line(width = 1, color = 'rgb(150, 150, 150)'),
        hoverinfo = 'none',
        mode = 'lines')

    # Create figure:
    fig = go.Figure(data = go.Data([edge_trace, node_trace]),
                    layout = go.Layout(
                    titlefont = dict(size = 16),
                    plot_bgcolor = 'rgba(0,0,0,0)',
                    showlegend = False,
                    hovermode = 'closest',
                    width = 700,
                    margin = dict(b = 30, l = 20, r = 30, t = 40),
                    annotations = annotations_list,
                    xaxis = go.XAxis(showgrid = False, zeroline = False, showticklabels = False),
                    yaxis = go.YAxis(showgrid = False, zeroline = False, showticklabels = False)))

    figM = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

    return figM
