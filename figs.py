import plotly.express as px
from logic import budget_summary, accounts, earn_calc, spend_calc, income_calc, expense_calc
import numpy as np

# make budegt figure

def budget_fig_gen(transactions):

    budget = budget_summary(transactions)

    # add bar plot of budgetted vs spent

    budget_fig = px.bar(budget, y='budget_head', x=['budgetted', 'debit'], barmode = "group", width=750, height=450)

    # add mean spend over six months

    budget_fig.add_scatter(y = budget['budget_head'], x=budget['mean'], mode="markers", marker=dict(symbol='x', size=5, color = 'black'), showlegend=False)

    # Add title and axis labels
    
    budget_fig.update_layout(title={"text":'Budgetted vs Spent in the current month', "xanchor":"center", "x":0.5}, yaxis_title='Budget Head', xaxis_title='Budgetted/Spent', font = {"size":18})

    # Update the legend properties
    
    budget_fig.update_layout(legend=dict(title_text='', orientation='h', yanchor='top', y=1, x=0.625))

    return budget_fig

# Bar plot for accounts

def accounts_fig_gen(transactions):

    # plot

    accounts_fig = px.bar(accounts(transactions), x=accounts(transactions).index, y='balance', title="Account Balance")

    # capitalise axis titles

    accounts_fig.update_layout(height=450, width=750, title_x=0.5, title_font_size=15, xaxis_title="Account", yaxis_title="Balance",
        font=dict(
            size=10,  # Increase the font size to 20
        ))

    # add six figure value labels

    accounts_fig.update_traces(texttemplate='%{y:.6s}', textposition='outside')

    return accounts_fig

# Create the spend-earn graph

def spend_earn_fig(transactions, budget):

    earn = earn_calc(transactions, budget)

    spend = spend_calc(transactions, budget)

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
    
    return earn_fig

# Create the box plot using Plotly Express

def income_fig_gen(transactions, budget):

    income_180 = income_calc(transactions, budget)

    income_fig = px.box(income_180, x='budget_head', y='credit', height=450, boxmode='group', width=800)

    # Add title and axis labels
    income_fig.update_layout(title='Income Distribution across Sources (Last Six Months)', xaxis_title='Source', yaxis_title='Credit')

    income_fig.update_layout(height=450, width=750, title_x=0.5, title_font_size=15,
        font=dict(
            size=10,  # Increase the font size to 20
        ))
    
    return income_fig


# Expense summary figure

def expense_fig_gen(transactions, budget):

    expense_180 = expense_calc(transactions, budget)

    # Create the box plot using Plotly Express
    
    expense_fig = px.box(expense_180, y='budget_head', x='debit', height=450, boxmode='group', width=1000)

    # Add title and axis labels
    
    expense_fig.update_layout(title='Expense Distribution across Budget Heads (Last Six Months)', yaxis_title='Budget Head', xaxis_title='Debit')

    expense_fig.update_layout(height=450, width=750, title_x=0.5, title_font_size=15,
        font=dict(
            size=10,  # Increase the font size to 20
        )
        )
    
    return expense_fig

# plot a flipped bar graph of total profit (Current-value - invested) by type in investments

def instruments_fig(investments):

    # filter latest investments

    investments = investments[investments['date'] == investments['date'].max()]

    # the investments dataframe has name, type, invested, Current-value

    # calculate profit

    investments['profit'] = investments['Current-value'] - investments['invested']

    # calculate percentage profit

    investments['percent-profit'] = investments['profit']*100/investments['invested']

    # remove infinities in percent profit

    investments = investments.replace([np.inf, -np.inf], np.nan).dropna(subset=["percent-profit"], how="all")

    # calculate mean and standard deviation of percent profit grouped by type
    grouped_investments = investments.groupby('type')['percent-profit'].agg(['mean', 'std']).reset_index()

    # plot mean and std as error bars on a bar plot
    instruments_fig = px.bar(grouped_investments, x='type', y='mean', error_y='std', width=750, height=450)

    # make consistent with other figs
    instruments_fig.update_layout(title={"text":'Mean and Standard Deviation of Percent Profit by Instrument Type', "xanchor":"center", "x":0.5}, yaxis_title='Percent Profit', xaxis_title='Instrument Type', font = {"size":16})

    return instruments_fig

def equities_fig(investments):

    # filter latest investments

    investments = investments[investments['date'] == investments['date'].max()]

    # the investments dataframe has name, type, invested, Current-value

    # select only equities

    equities = investments[investments['type'] == 'Equity']

    # plot invested and current value as side by side bars

    equities_fig = px.bar(equities, y='name', x=['invested', 'Current-value'], barmode = "group", width=750, height=450)

    # make consistent with other figs

    equities_fig.update_layout(title={"text":'Invested vs Current Value of Equities', "xanchor":"center", "x":0.5}, xaxis_title='Amount', yaxis_title='Equity', font = {"size":18})
    
    # reduce y axis font size

    equities_fig.update_yaxes(tickfont=dict(size=10))

    return equities_fig

def mutual_funds_fig(investments):

    # filter latest investments

    investments = investments[investments['date'] == investments['date'].max()]

    # the investments dataframe has name, type, invested, Current-value

    # select only mutual funds

    mutual_funds = investments[investments['type'] == 'Mutual Fund']

    # plot invested and current value as side by side bars

    mutual_funds_fig = px.bar(mutual_funds, y='name', x=['invested', 'Current-value'], barmode = "group", width=750, height=450)

    # make consistent with other figs

    mutual_funds_fig.update_layout(title={"text":'Invested vs Current Value of Mutual Funds', "xanchor":"center", "x":0.5}, xaxis_title='Amount', yaxis_title='Mutual Fund', font = {"size":18})

    # reduce y axis font size

    mutual_funds_fig.update_yaxes(tickfont=dict(size=10))

    return mutual_funds_fig

# figure to detemine change in net value of investments over time by type

def net_value_fig(investments):


    # the investments dataframe has name, type, invested, Current-value

    # get sum of current value by type and date

    net_value = investments.groupby(['date', 'type'])['Current-value'].sum().reset_index()
    
    # plot sum of current value by type over date

    net_value_fig = px.line(net_value, x='date', y='Current-value', color='type', width=750, height=450)

    # make consistent with other figs

    net_value_fig.update_layout(title={"text":'Change in Net Value of Investments over Time by Type', "xanchor":"center", "x":0.5}, xaxis_title='Date', yaxis_title='Current Value', font = {"size":16})
    
    return net_value_fig