import pandas as pd
import pymongo as pm
from dash import Dash, dcc, html
import plotly.express as px
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

app = Dash(__name__)
server = app.server 

client = pm.MongoClient(MONGO_URL)
db = client["project"]
approval_collection = db["covid_approval_polls"]
concern_collection = db["covid_concern_polls"]

df = pd.DataFrame(list(approval_collection.find({})))
df.fillna(value=0, inplace=True)
df['end_date'] = pd.to_datetime(df['end_date'])

df_concern = pd.DataFrame(list(concern_collection.find({})))
df_concern.fillna(value=0, inplace=True)
df_concern['end_date'] = pd.to_datetime(df_concern['end_date'])

group_color = {"Trump": '#ec8273', "Biden": '#6f7af9',
               'D': 'blue', 'R': 'red', 'I': 'green'}

group_color_trump = {"approve": 'red', "disapprove": 'green'}

group_color_biden = {"approve": 'blue', "disapprove": 'orange'}

line_trump_graph = px.scatter(df[df['subject'] == 'Trump'], x="end_date", y=[
                              "approve", "disapprove"], trendline="lowess", trendline_options=dict(frac=0.1), color_discrete_map=group_color_trump, opacity=0.1)

line_trump_graph.add_vline(x=datetime.datetime(2020, 3, 1).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="First U.S death reported", annotation_position="top top")

line_trump_graph.add_vline(x=datetime.datetime(2020, 5, 28).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="U.S deaths surpass 100.000", annotation_position="top top")
line_trump_graph.add_vline(x=datetime.datetime(2020, 11, 7).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="Biden declared election winner", annotation_position="top top")
line_trump_graph.add_vline(x=datetime.datetime(2021, 1, 20).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="Biden sworn into office", annotation_position="top top")
line_trump_graph.add_vline(x=datetime.datetime(2020, 12, 14).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="The first American COVID-19 vaccine outside of clinical trials is received", annotation_position="bottom left")


line_trump_graph.update_layout(
    title="Comparison of Trump's approval and disapproval ratings",
    xaxis_title="Date of the poll",
    yaxis_title="Approval",
    legend_title="Category"
)

trump_republicans_approval = df[(df['party'] == 'R') & (
    df['subject'] == 'Trump')]['approve'].mean()
trump_republicans_disapprove = df[(df['party'] == 'R') & (
    df['subject'] == 'Trump')]['disapprove'].mean()

bar_republicans_graph = px.bar(x=["approve", "disapprove"], y=[
    trump_republicans_approval, trump_republicans_disapprove], color=["approve", "disapprove"], color_discrete_map=group_color_trump)

bar_republicans_graph.update_layout(
    title="Comparison between trump's approval and disapproval by republican party supporters",
    xaxis_title="Aprove or Disapprove",
    yaxis_title="Approval",
    legend_title="Category"
)

line_biden_graph = px.scatter(df[df['subject'] == 'Biden'], x="end_date", y=[
    "approve", "disapprove"], trendline="lowess", trendline_options=dict(frac=0.1), color_discrete_map=group_color_biden, opacity=0.1)


line_biden_graph.add_vline(x=datetime.datetime(2021, 1, 20).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="Biden sworn into office", annotation_position="bottom right")
line_biden_graph.add_vline(x=datetime.datetime(2021, 2, 16).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="U.S deaths surpass 500.000", annotation_position="top top")
line_biden_graph.add_vline(x=datetime.datetime(2021, 12, 15).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="U.S deaths surpass 800.000", annotation_position="top top")
line_biden_graph.add_vline(x=datetime.datetime(2022, 5, 12).timestamp() * 1000, line_width=2,
                           line_dash="dash", line_color="black", annotation_text="U.S deaths surpass 1.000.000", annotation_position="bottom right")

line_biden_graph.update_layout(
    title="Comparison of Biden's approval and disapproval ratings",
    xaxis_title="Date of the poll",
    yaxis_title="Approval",
    legend_title="Category"
)

biden_democrats_approval = df[(df['party'] == 'D') & (
    df['subject'] == 'Biden')]['approve'].mean()
biden_democrats_disapprove = df[(df['party'] == 'D') & (
    df['subject'] == 'Biden')]['disapprove'].mean()

bar_democrats_graph = px.bar(x=["approve", "disapprove"], y=[
    biden_democrats_approval, biden_democrats_disapprove], color=["approve", "disapprove"], color_discrete_map=group_color_biden)

bar_democrats_graph.update_layout(
    title="Comparison between biden's approval and disapproval by democratic party supporters",
    xaxis_title="Aprove or Disapprove",
    yaxis_title="Approval",
    legend_title="Category"
)

approval_graph = px.scatter(df, x="end_date", y="approve", size="approve",
                            color="subject", trendline="lowess", trendline_options=dict(frac=0.1), trendline_color_override="black", color_discrete_map=group_color)

approval_graph.add_vrect(x0=datetime.datetime(2021, 2, 1).timestamp() * 1000, x1=datetime.datetime(2021, 2, 25).timestamp() * 1000,
                         line_width=0, fillcolor="red", opacity=0.25, annotation_text="B 1", annotation_position="top top")
approval_graph.add_vrect(x0=datetime.datetime(2022, 1, 1).timestamp() * 1000, x1=datetime.datetime(2022, 1, 30).timestamp() * 1000,
                         line_width=0, fillcolor="red", opacity=0.25, annotation_text="B 4", annotation_position="top top")

approval_graph.add_vline(x=datetime.datetime(2021, 3, 11).timestamp() * 1000, line_width=1.5,
                         line_dash="dash", line_color="red", annotation_text="B 2", annotation_position="top top")

approval_graph.add_vline(x=datetime.datetime(2021, 9, 18).timestamp() * 1000, line_width=1.5,
                         line_dash="dash", line_color="red", annotation_text="B 4", annotation_position="top top")


approval_graph.add_vline(x=datetime.datetime(2020, 3, 13).timestamp() * 1000, line_width=1.5,
                         line_dash="dash", line_color="red", annotation_text="T 1", annotation_position="top top")

approval_graph.add_vrect(x0=datetime.datetime(2020, 3, 25).timestamp() * 1000, x1=datetime.datetime(2020, 4, 30).timestamp() * 1000,
                         fillcolor="red", opacity=0.25, line_width=0, annotation_text="T 2", annotation_position="top top")

approval_graph.add_vrect(x0=datetime.datetime(2020, 11, 1).timestamp() * 1000, x1=datetime.datetime(2020, 11, 30).timestamp() * 1000,
                         fillcolor="red", opacity=0.25, line_width=0, annotation_text="T 3", annotation_position="top top")


approval_graph.update_layout(
    title="Trump and Biden approval rating comparison",
    xaxis_title="Date of the poll",
    yaxis_title="Approval",
    legend_title="Subject"

)

disapprove_graph = px.scatter(df, x="end_date", y="disapprove", size="disapprove",
                              color="subject", trendline="lowess", trendline_options=dict(frac=0.1), trendline_color_override="black", color_discrete_map=group_color)

disapprove_graph.add_vrect(x0=datetime.datetime(2021, 2, 1).timestamp() * 1000, x1=datetime.datetime(2021, 2, 25).timestamp() * 1000,
                           line_width=0, fillcolor="red", opacity=0.25, annotation_text="B 1", annotation_position="top top")
disapprove_graph.add_vrect(x0=datetime.datetime(2022, 1, 1).timestamp() * 1000, x1=datetime.datetime(2022, 1, 30).timestamp() * 1000,
                           line_width=0, fillcolor="red", opacity=0.25, annotation_text="B 4", annotation_position="top top")
disapprove_graph.add_vline(x=datetime.datetime(2021, 3, 11).timestamp() * 1000, line_width=1.5,
                           line_dash="dash", line_color="red", annotation_text="B 2", annotation_position="top top")

disapprove_graph.add_vline(x=datetime.datetime(2021, 9, 18).timestamp() * 1000, line_width=1.5,
                           line_dash="dash", line_color="red", annotation_text="B 3", annotation_position="top top")

disapprove_graph.add_vline(x=datetime.datetime(2020, 3, 13).timestamp() * 1000, line_width=1.5,
                           line_dash="dash", line_color="red", annotation_text="T 1", annotation_position="top top")

disapprove_graph.add_vrect(x0=datetime.datetime(2020, 3, 25).timestamp() * 1000, x1=datetime.datetime(2020, 4, 30).timestamp() * 1000,
                           fillcolor="red", opacity=0.25, line_width=0, annotation_text="T 2", annotation_position="top top")

disapprove_graph.add_vrect(x0=datetime.datetime(2020, 11, 1).timestamp() * 1000, x1=datetime.datetime(2020, 11, 30).timestamp() * 1000,
                           fillcolor="red", opacity=0.25, line_width=0, annotation_text="T 3", annotation_position="top top")

disapprove_graph.update_layout(
    title="Trump and Biden disapproval rating comparison",
    xaxis_title="Date of the poll",
    yaxis_title="Disapproval",
    legend_title="Subject"
)

trump_approval = df[df['subject'] == 'Trump']['approve'].mean()
biden_approval = df[df['subject'] == 'Biden']['approve'].mean()

average_approval_bar = px.bar(x=["Trump", "Biden"], y=[
    trump_approval, biden_approval], color=["Trump", "Biden"], color_discrete_map=group_color)

average_approval_bar.update_layout(
    title="Trump and Biden approval rating average",
    xaxis_title="Candidate",
    yaxis_title="Approval average",
    legend_title="Candidate",

)

trump_disapprove = df[df['subject'] == 'Trump']['disapprove'].mean()
biden_disapprove = df[df['subject'] == 'Biden']['disapprove'].mean()

average_disapprove_bar = px.bar(x=["Trump", "Biden"], y=[
    trump_disapprove, biden_disapprove], color=["Trump", "Biden"], color_discrete_map=group_color)

average_disapprove_bar.update_layout(
    title="Trump and Biden disapproval rating average",
    xaxis_title="Candidate",
    yaxis_title="Disapproval average",
    legend_title="Candidate",

)

parties_comparison_graph_biden = px.scatter(df[(df['party'] != 'all') & (df['subject'] == 'Biden')], x="end_date", y="approve", size="approve",
                                            color="party",  trendline="rolling", trendline_options=dict(window=5), color_discrete_map=group_color, opacity=0.1)


parties_comparison_graph_biden.add_vrect(x0=datetime.datetime(2021, 2, 1).timestamp() * 1000, x1=datetime.datetime(2021, 2, 25).timestamp() * 1000,
                                         line_width=0, fillcolor="red", opacity=0.25, annotation_text="B 1", annotation_position="top top")
parties_comparison_graph_biden.add_vrect(x0=datetime.datetime(2022, 1, 1).timestamp() * 1000, x1=datetime.datetime(2022, 1, 30).timestamp() * 1000,
                                         line_width=0, fillcolor="red", opacity=0.25, annotation_text="B 4", annotation_position="top top")
parties_comparison_graph_biden.add_vline(x=datetime.datetime(2021, 3, 11).timestamp() * 1000, line_width=1.5,
                                         line_dash="dash", line_color="red", annotation_text="B 2", annotation_position="top top")

parties_comparison_graph_biden.add_vline(x=datetime.datetime(2021, 9, 18).timestamp() * 1000, line_width=1.5,
                                         line_dash="dash", line_color="red", annotation_text="B 3", annotation_position="top top")


parties_comparison_graph_biden.update_layout(
    title="Comparison of Biden's approval by all parties",
    xaxis_title="Date of the poll",
    yaxis_title="Approval",
    legend_title="Party"

)

parties_comparison_graph_trump = px.scatter(df[(df['party'] != 'all') & (df['subject'] == 'Trump')], x="end_date", y="approve", size="approve",
                                            color="party",  trendline="rolling", trendline_options=dict(window=5), color_discrete_map=group_color, opacity=0.1)


parties_comparison_graph_trump.add_vline(x=datetime.datetime(2020, 3, 13).timestamp() * 1000, line_width=1.5,
                                         line_dash="dash", line_color="red", annotation_text="T 1", annotation_position="top right")

parties_comparison_graph_trump.add_vrect(x0=datetime.datetime(2020, 3, 25).timestamp() * 1000, x1=datetime.datetime(2020, 4, 30).timestamp() * 1000,
                                         fillcolor="red", opacity=0.25, line_width=0, annotation_text="T 2", annotation_position="top top")

parties_comparison_graph_trump.add_vrect(x0=datetime.datetime(2020, 11, 1).timestamp() * 1000, x1=datetime.datetime(2020, 11, 30).timestamp() * 1000,
                                         fillcolor="red", opacity=0.25, line_width=0, annotation_text="T 3", annotation_position="top top")


parties_comparison_graph_trump.update_layout(
    title="Comparison of Trump's approval by all parties",
    xaxis_title="Date of the poll",
    yaxis_title="Approval",
    legend_title="Party"

)

americans_concern_graph = px.scatter(df_concern[df_concern['subject'] == 'concern-infected'], x="end_date", y=[
                                     'very', 'somewhat', 'not_very', 'not_at_all'], trendline="lowess", trendline_options=dict(frac=0.1), opacity=0.1)

americans_concern_graph.update_layout(
    title="Americans' concern about being infected by coronavirus",
    xaxis_title="Date of the poll",
    yaxis_title="Concern",
    legend_title="Category"

)


app.layout = html.Div(children=[
    html.H1(children='''How Americans view Biden and Trump's response to coronavirus crisis'''),
    html.Div(children='''
        Big Data Study Case.
    '''),
    dcc.Graph(figure=line_trump_graph),
    dcc.Graph(figure=bar_republicans_graph),
    dcc.Graph(figure=line_biden_graph),
    dcc.Graph(figure=bar_democrats_graph),
    dcc.Graph(figure=approval_graph),
    dcc.Graph(figure=disapprove_graph),
    dcc.Graph(figure=average_approval_bar),
    dcc.Graph(figure=average_disapprove_bar),
    dcc.Graph(figure=parties_comparison_graph_biden),
    dcc.Graph(figure=parties_comparison_graph_trump),
    dcc.Graph(figure=americans_concern_graph),
], style={'textAlign': 'center', 'font-family': 'arial', 'color': 'black'})

