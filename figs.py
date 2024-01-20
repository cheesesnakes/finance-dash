import pandas as pd
import plotly.express as px
from logic import transactions, budget, debt, accounts, earn, spend, income_180
from logic import expense_180

# add bar plot of budgetted vs spent

budget_fig = px.bar(budget, y='budget_head', x=['budgetted', 'debit'], barmode = "group", width=750, height=450)

# add mean spend over six months

budget_fig.add_scatter(y = budget['budget_head'], x=budget['mean'], mode="markers", marker=dict(symbol='x', size=5, color = 'black'), showlegend=False)

# Add title and axis labels
budget_fig.update_layout(title={"text":'Budgetted vs Spent in the current month', "xanchor":"center", "x":0.5}, yaxis_title='Budget Head', xaxis_title='Budgetted/Spent', font = {"size":18})

# Update the legend properties
budget_fig.update_layout(legend=dict(title_text='', orientation='h', yanchor='top', y=1, x=0.625))

# Bar plot for accounts

# plot

accounts_fig = px.bar(accounts, x=accounts.index, y='balance', title="Account Balance")

# capitalise axis titles

accounts_fig.update_layout(height=450, width=750, title_x=0.5, title_font_size=15, xaxis_title="Account", yaxis_title="Balance",
    font=dict(
        size=10,  # Increase the font size to 20
    ))

# add six figure value labels

accounts_fig.update_traces(texttemplate='%{y:.6s}', textposition='outside')

# Create the spend-earn graph
earn_fig = px.scatter(earn, x='date', y='credit', width=750, height=450, color_discrete_sequence=['green'])

earn_fig.add_scatter(x=spend['date'], y=spend['debit'], showlegend=False, mode='markers', marker=dict(color='red'))

# Add the moving average line with thicker red line
earn_fig.add_scatter(x=earn['date'], y=earn['Moving Average'], mode='lines', line=dict(color='green', width=3, dash = "dot"), showlegend=False)
earn_fig.add_scatter(x=spend['date'], y=spend['Moving Average'], mode='lines', line=dict(color='red', width=3, dash = "dot"), showlegend=False)

# Add the upper and lower bounds as a semitransparent blue ribbon
#earn_fig.add_scatter(x=earn['date'], y=earn['Lower Bound'], mode='lines', line=dict(color='green', width=1, dash = "dot"), showlegend=False, fill='tonexty')
#earn_fig.add_scatter(x=earn['date'], y=earn['Upper Bound'], mode='lines', line=dict(color='green', width=1, dash = "dot"), showlegend=False, fill='tonexty')
#earn_fig.add_scatter(x=spend['date'], y=spend['Lower Bound'], mode='lines', line=dict(color='red', width=1, dash = "dot"), showlegend=False, fill='tonexty')
#earn_fig.add_scatter(x=spend['date'], y=spend['Upper Bound'], mode='lines', line=dict(color='red', width=1, dash = "dot"), showlegend=False, fill='tonexty')

earn_fig.update_yaxes(range=[0, 250000])  # Set y limit from 0 to 250k

# Add title and axis labels
earn_fig.update_layout(title='Amount Earned vs Spent per Month', xaxis_title='Date', yaxis_title='Credit', title_x=0.5, title_font_size=15,font=dict(
        size=10,  # Increase the font size to 20
    ))

# Create the box plot using Plotly Express
income_fig = px.box(income_180, x='budget_head', y='credit', height=450, boxmode='group', width=800)

# Add title and axis labels
income_fig.update_layout(title='Income Distribution across Sources (Last Six Months)', xaxis_title='Source', yaxis_title='Credit')

income_fig.update_layout(height=450, width=750, title_x=0.5, title_font_size=15,
    font=dict(
        size=10,  # Increase the font size to 20
    ))

# Table for highest income sources in last 180 days
income_high = income_180.sort_values(by='credit', ascending=False).head(5)[['date', 'description', 'credit']]

# Expense summary figure

# Create the box plot using Plotly Express
expense_fig = px.box(expense_180, y='budget_head', x='debit', height=450, boxmode='group', width=1000)

# Add title and axis labels
expense_fig.update_layout(title='Expense Distribution across Budget Heads (Last Six Months)', yaxis_title='Budget Head', xaxis_title='Debit')

expense_fig.update_layout(height=450, width=750, title_x=0.5, title_font_size=15,
    font=dict(
        size=10,  # Increase the font size to 20
    ))
