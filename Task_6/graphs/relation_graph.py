import networkx as nx
import plotly
import plotly.graph_objs as go
import json


def generate_graph_from_relation(pairs):
    edges = []
    nodes = []

    for index in range(len(pairs)):
        node_a = pairs[index][0]  # subject
        node_b = pairs[index][2]  # object
        pair = (node_a, node_b)
        edges.append(pair)
        nodes.append(node_a)
        nodes.append(node_b)

    nodes = list(set(nodes))
    G = nx.DiGraph()
    G.add_edges_from(edges)
    G.add_nodes_from(nodes)
    node_positions = nx.spring_layout(G)
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

    for edge in G.edges:
        x0, y0 = node_positions[edge[0]]
        x1, y1 = node_positions[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

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
                    showlegend = False,
                    hovermode = 'closest',
                    margin = dict(b = 20, l = 5, r = 5, t = 40),
                    xaxis = go.XAxis(showgrid = False, zeroline = False, showticklabels = False),
                    yaxis = go.YAxis(showgrid = False, zeroline = False, showticklabels = False)))

    figM = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

    return figM
