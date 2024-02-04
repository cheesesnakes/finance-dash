# import libraries

import pandas as pd
from datetime import datetime, timedelta
from data import get_data
from dash import dash_table

# import data

## Function for transactions

def get_transactions():
    
    transactions = get_data("transactions")
    
    # rename cols

    transactions.rename(columns={
        'Date':'date',
        'Description':'description',
        'Credit':'credit',
        'Debit':'debit',
        'BudgetHead':'budget_head',
        'Account':'account',
        'Reviewed':'reviewed',
        'Memo':'memo',
        'Settlement':'settlement'
        }, 
                        inplace=True)
    
    # set date type

    transactions['date'] = pd.to_datetime(transactions['date'], format='%Y-%m-%d')
    transactions['credit'] = pd.to_numeric(transactions['credit'])
    transactions['debit'] = pd.to_numeric(transactions['debit'])
    
    print("got transactions")

    return transactions

def get_budget():
   budget = get_data("budget")
   budget.rename(columns={
    'BudgetHead':'budget_head',
    'Goal':'goal',
    'Budgetted':'budgetted',
    'Memo':'memo'
  },
            inplace=True)
   
   print("got budget")
   
   return budget

def get_debt():

  debt = get_data("debt")

  debt.rename(columns={
  'Date':'date',
  'Loans':'loans',
  'Debt':'debt'
  },
            inplace=True)
  
  print("got debt")
  
  return debt

def get_investments():

  investments = get_data("investments")
  investments['Current-value'] = pd.to_numeric(investments['Current-value'])
  investments['invested'] = pd.to_numeric(investments['invested'])
  investments['date'] = pd.to_datetime(investments['date'], format='%Y-%m-%d')
  return investments

# last review date

def last_review_date(transactions):
    last_review_date = transactions[(transactions["reviewed"] == "Yes")]['date'].max()
    print("Calculated last review date")
    return last_review_date

# Account summaries

def accounts(transactions):
  
  accounts = pd.DataFrame()

  accounts['credit'] = transactions.groupby('account')['credit'].sum()

  accounts['debit'] = transactions.groupby('account')['debit'].sum()

  accounts['balance'] = accounts['credit'] - accounts['debit']

  print("Calculated accounts")

  return accounts

# Convert the accounts list into a Dash datatable

def accounts_table(transactions):
  
  dat = accounts(transactions)

  accounts_table = dash_table.DataTable(
      data=accounts(transactions),
      columns=[{"name": i, "id": i} for i in dat.columns],
  )

  print("Plotted accounts table")

  return accounts_table

# Networth

def networth(accounts, debt, investments):
  # filter latest investments
  investments = investments[investments['date'] == investments['date'].max()]
  print("Caclulated networth")
  return accounts['balance'].sum() + list(debt.iloc[-1])[1] - list(debt.iloc[-1])[2] + investments['Current-value'].sum()

# Loan and debt summaries

def current_debt(debt):

  print("Retrieved current debt")
  
  return debt.iloc[-1]

# Work expenses

def reimbursement(transactions):
  
  work_expense = transactions[transactions['budget_head'] == 'Work Expense']

  print("Calculated reimbursement")

  return -work_expense['credit'].sum() + work_expense['debit'].sum()

# calculate current investment value

def net_value(investment):
  
  #filter only latest investment

  investment = investment[investment['date'] == investment['date'].max()]

  return investment['Current-value'].sum()
# Budget summary

def budget_summary(transactions):

  budget = get_budget()

  ## calculate spent amount over the last month

  ### filter transactions in the last month

  end_date = datetime.now()
  start_date = datetime(end_date.year, end_date.month, 1)

  spend_current = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]

  ### group by budget head

  spend_current = spend_current.groupby('budget_head')['debit'].sum().reset_index()

  spend_current = spend_current[['budget_head', 'debit']]

  ## merge monthly budgetted with spent

  budget = pd.merge(budget, spend_current, on="budget_head", how="left")

  ## calculate average spent per budget head over the past six months

  ## Calculate the start date for six months ago from today
  end_date = datetime.now()
  start_date = end_date - timedelta(days=6*30)  # Assuming each month has 30 days for simplicity

  ## Filter transactions for the past six months
  spent_avg = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]

  ## Group by 'Budget.Head' and calculate the mean spend for each budget head
  spent_avg = spent_avg.groupby(['budget_head', pd.Grouper(key='date', freq='ME')])['debit'].sum().reset_index()
  spent_avg = spent_avg.groupby('budget_head')['debit'].mean().reset_index()

  spent_avg.rename(columns={'debit':'mean'}, inplace=True)

  ## merge monthly budgetted with spent

  budget = pd.merge(budget, spent_avg, on="budget_head", how="left")

  print("Caclulated budget summary")

  return budget

# Calculate available to spend this month

def available(budget):
  print("Calculated available to spend")
  return budget['budgetted'].sum() - budget['debit'].sum()

# spend over time

def spend_calc(transactions, budget):

  ## assign data from data.py to spend variable

  spend = transactions
  
  ## filter out accounts

  account_list = accounts(transactions).index.tolist()

  account_list.append('Work Expense')

  spend = spend[~spend['budget_head'].isin(account_list)]

  ## filter out expenditure budget_heads

  budget_head_list = budget['budget_head'].tolist()

  spend = spend[spend['budget_head'].isin(budget_head_list)]

  ## Group the data by month

  spend = spend.groupby(pd.Grouper(key='date', freq='ME'))['debit'].sum().reset_index()

  ## Calculate the moving average and standard deviation for the 'debit' column

  spend['Moving Average'] = spend['debit'].rolling(window=6, min_periods=1).mean()
  spend['Standard Deviation'] = spend['debit'].rolling(window=6, min_periods=1).std()

  ## Compute the upper and lower bounds for the 95% confidence interval

  spend['Lower Bound'] = spend['Moving Average'] - spend['Standard Deviation'] #*1.96
  spend['Upper Bound'] = spend['Moving Average'] + spend['Standard Deviation'] #*1.96

  print("Calculated spend")

  return spend

# Earnings data

def earn_calc(transactions, budget):

  earn = transactions
  
  ## filter out accounts

  account_list = accounts(transactions).index.tolist()

  earn = earn[~earn['budget_head'].isin(account_list)]

  ## filter out expenditure budget_heads

  budget_head_list = budget['budget_head'].tolist()

  budget_head_list.append('Work Expense')

  earn = earn[~earn['budget_head'].isin(budget_head_list)]

  ## Group the earn by month
  
  earn = earn.groupby(pd.Grouper(key='date', freq='ME'))['credit'].sum().reset_index()

  ## Calculate the moving average and standard deviation for the 'credit' column
  
  earn['Moving Average'] = earn['credit'].rolling(window=6, min_periods=1).mean()
  earn['Standard Deviation'] = earn['credit'].rolling(window=6, min_periods=1).std()

  ## Compute the upper and lower bounds for the 95% confidence interval
  earn['Lower Bound'] = earn['Moving Average'] - earn['Standard Deviation'] #*1.96
  earn['Upper Bound'] = earn['Moving Average'] + earn['Standard Deviation'] #*1.96

  print("Caclulated earnings")

  return earn

def income_calc(transactions, budget):

  # Calculate the start date for six months ago from today

  end_date = datetime.now()
  start_date = end_date - timedelta(days=6*30)  # Assuming each month has 30 days for simplicity

  # Filter income data for the last six months
  income_180 = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]

  # filter out accounts

  account_list = accounts(transactions).index.tolist()

  income_180 = income_180[~income_180['budget_head'].isin(account_list)]

  # remove cigaratte expenses

  income_180 = income_180[income_180['budget_head'] != 'Cigarettes']

  # filter out expenditure budget_heads

  budget_head_list = budget['budget_head'].tolist()

  income_180 = income_180[~income_180['budget_head'].isin(budget_head_list)]

  # fixing remibursements

  income_180['budget_head'] = income_180['budget_head'].replace('Work Expense', 'Reimbursement')

  print("Calculated last six months income")
  return income_180

# Highest income sources ovr the last six months

def income_high(transactions, budget):
  
  income_180 = income_calc(transactions, budget)

  return income_180.sort_values(by='credit', ascending=False).head(5)[['date', 'description', 'credit']]

def expense_calc(transactions, budget):

  # Calculate the start date for six months ago from today

  end_date = datetime.now()
  start_date = end_date - timedelta(days=6*30)  # Assuming each month has 30 days for simplicity

  # Filter income data for the last six months

  expense_180 = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]

  # filter out accounts

  account_list = accounts(transactions).index.tolist()

  expense_180 = expense_180[~expense_180['budget_head'].isin(account_list)]

  # filter out expenditure budget_heads

  budget_head_list = budget['budget_head'].tolist()

  expense_180 = expense_180[expense_180['budget_head'].isin(budget_head_list)]

  # fixing remibursements

  expense_180['budget_head'] = expense_180['budget_head'].replace('Work Expense', 'Reimbursement')

  print("Caclulated last six months expenses")

  return expense_180

# largest expenses over the last six months

def expense_high(transactions, budget): 
  
  expense_180 = expense_calc(transactions, budget)

  return expense_180.sort_values(by='debit', ascending=False).head(5)[['date', 'description', 'debit']]

# get total debit for all investments with description "ACH D- LIC OF INDIA-9115721030522"

def lic_debit(transactions):
  return transactions[(transactions['description'].str.contains('ACH D- LIC OF INDIA-9115721030522')) & (transactions['debit'] > 0)]['debit'].sum()