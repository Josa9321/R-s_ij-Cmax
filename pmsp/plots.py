import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


def gantt_chart(original_df: pd.DataFrame, setup_idx=1, consider_due_date=False):
    solution_df = original_df.copy(deep=True)
    now = datetime(year=1970, month=1, day=1)
    solution_df['Start'] = [now + timedelta(seconds=t) for t in solution_df['Start']]
    solution_df['Finish'] = [now + timedelta(seconds=t) for t in solution_df['Finish']]
    solution_df['Task'] = [txt for txt in solution_df['Task']]
    solution_df['Machine'] = [f'Machine {h}' for h in solution_df['Machine']]

    fig = px.timeline(solution_df, x_start="Start", x_end="Finish", y="Machine", color='Type', text='Task')
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    fig.update_layout(
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      xaxis=dict(tickformat = '%s'),
                      yaxis_title = r'',
                      legend=dict(
                                  yanchor="top",
                                  y=1.2,
                                  xanchor="center",
                                  orientation="h",
                                  x=0.5
                                  ))

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_traces(width=0.6, textposition='inside')

    for n in fig.data:
        n["marker"]['line']["color"]='#000000'
        n['marker']['line']['width'] = 2
        n['marker']['color']='rgba(0, 0, 0, 0)'


    if setup_idx != -1:
        fig.data[setup_idx]['marker']['color']='#D6DEE2'#'#CDDFF8'

    if not consider_due_date:
        return fig

    fig.add_scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(
            symbol="triangle-up",
            size=12,
            color="red"
        ),
        name="Due date"
    )

    for _, row in solution_df.iterrows():
        if row["Type"] != "Job":
            continue

        due_date = now + timedelta(seconds=row["Due Date"])
        machine = row["Machine"]
        job = row["Task"]
        fig.add_annotation(
            x=due_date,
            y=machine,
            text="▲",
            showarrow=False,
            yshift=14,
            font=dict(color='red', size=12)
        )
        fig.add_annotation(
            x=due_date,
            y=machine,
            text=job,
            showarrow=False,
            yshift=24,
            font=dict(color='black', size=12)
        )
    return fig
