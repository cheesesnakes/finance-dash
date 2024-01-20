# import libraries

import pandas as pd
from datetime import datetime, timedelta
from data import get_data

# import data

transactions = get_data("transactions")
budget = get_data("budget")
debt = get_data("debt")

transactions.head()

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

debt.rename(columns={
  'Date':'date',
  'Loans':'loans',
  'Debt':'debt'
},
            inplace=True)

budget.rename(columns={
  'BudgetHead':'budget_head',
  'Goal':'goal',
  'Budgetted':'budgetted',
  'Memo':'memo'
},
            inplace=True)

# set date type

transactions['date'] = pd.to_datetime(transactions['date'], format='%Y-%m-%d')
transactions['credit'] = pd.to_numeric(transactions['credit'])
transactions['debit'] = pd.to_numeric(transactions['debit'])

# Account summaries

accounts = pd.DataFrame()

accounts['credit'] = transactions.groupby('account')['credit'].sum()

accounts['debit'] = transactions.groupby('account')['debit'].sum()

accounts['balance'] = accounts['credit'] - accounts['debit']


# Loan and debt summaries

current_debt = debt.iloc[-1]

pd.DataFrame(current_debt)

## only display loans and debt

current_debt = current_debt[1:3]

# Work expenses

work_expense = transactions[transactions['budget_head'] == 'Work Expense']

reimbursement = -work_expense['credit'].sum() + work_expense['debit'].sum()


# Budget summary

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
spent_avg = spent_avg.groupby(['budget_head', pd.Grouper(key='date', freq='M')])['debit'].sum().reset_index()
spent_avg = spent_avg.groupby('budget_head')['debit'].mean().reset_index()

spent_avg.rename(columns={'debit':'mean'}, inplace=True)

## merge monthly budgetted with spent

budget = pd.merge(budget, spent_avg, on="budget_head", how="left")

# spend over time

## assign data from data.py to spend variable

spend = transactions

## set date type

spend['date'] = pd.to_datetime(spend['date'], format='%Y-%m-%d')

## filter out accounts

account_list = accounts.index.tolist()

account_list.append('Work Expense')

spend = spend[~spend['budget_head'].isin(account_list)]

## filter out expenditure budget_heads

budget_head_list = budget['budget_head'].tolist()

spend = spend[spend['budget_head'].isin(budget_head_list)]

## Group the data by month
spend = spend.groupby(pd.Grouper(key='date', freq='M'))['debit'].sum().reset_index()

## Calculate the moving average and standard deviation for the 'debit' column
spend['Moving Average'] = spend['debit'].rolling(window=6, min_periods=1).mean()
spend['Standard Deviation'] = spend['debit'].rolling(window=6, min_periods=1).std()

## Compute the upper and lower bounds for the 95% confidence interval
spend['Lower Bound'] = spend['Moving Average'] - spend['Standard Deviation'] #*1.96
spend['Upper Bound'] = spend['Moving Average'] + spend['Standard Deviation'] #*1.96

# Earnings data

earn = transactions

## set type for date

earn['date'] = pd.to_datetime(earn['date'], format='%Y-%m-%d')

## filter out accounts

account_list = accounts.index.tolist()

earn = earn[~earn['budget_head'].isin(account_list)]

## filter out expenditure budget_heads

budget_head_list = budget['budget_head'].tolist()

budget_head_list.append('Work Expense')

earn = earn[~earn['budget_head'].isin(budget_head_list)]

## Group the earn by month
earn = earn.groupby(pd.Grouper(key='date', freq='M'))['credit'].sum().reset_index()

## Calculate the moving average and standard deviation for the 'credit' column
earn['Moving Average'] = earn['credit'].rolling(window=6, min_periods=1).mean()
earn['Standard Deviation'] = earn['credit'].rolling(window=6, min_periods=1).std()

## Compute the upper and lower bounds for the 95% confidence interval
earn['Lower Bound'] = earn['Moving Average'] - earn['Standard Deviation'] #*1.96
earn['Upper Bound'] = earn['Moving Average'] + earn['Standard Deviation'] #*1.96


# Networth

networth = accounts['balance'].sum() + list(debt.iloc[-1])[1] - list(debt.iloc[-1])[2]