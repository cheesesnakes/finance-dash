# Import necessary libraries
import dash
from dash import dcc
from dash import html
from dash import dash_table

# importing data


from logic import get_transactions
from logic import get_debt
from logic import accounts
from logic import last_review_date
from logic import networth
from logic import available
from logic import budget_summary
from figs import budget_fig_gen
from figs import accounts_fig_gen
from figs import spend_earn_fig
from logic import income_high
from figs import income_fig_gen
from logic import expense_high
from figs import expense_fig_gen
from logic import reimbursement
from logic import current_debt

# Initialize the app
app = dash.Dash(__name__)
app.title = "Shawn's Financial Dashboard"

# Define the app layout
def serve_layout():

    transactions = get_transactions()
    budget = budget_summary(transactions)
    debt = get_debt()
    accounts_ = accounts(transactions)

    layout = html.Div(style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}, children=[
        html.H1("Shawn's Financial Dashboard"),
        
        html.Div(id='summary', style={'display':'flex-wrap', 'margin':'auto', 'max_width':'500px'}, children=[
            
            html.H2('Summary'),

            html.Div(id='summary-2', style={'display':'flex'},children=[


                html.Div(id='review-date',  style={'margin': '30px'}, children=[
                
                html.H3('Last Review Date'),
                
                last_review_date(transactions).strftime('%d-%m-%Y, %A')

                # Add a div for diplaying networth here

            ]),
            
            html.Div(id='networth',  style={'margin': '30px'}, children=[
                
                html.H3('Net Worth'),
                
                round(networth(accounts_, debt))
                # Add a div for diplaying networth here

            ]), 
            
                html.Div(id='available', style={'margin': '30px'}, children=[
                
                html.H3('Available'),
                
                round(available(budget))
                # Add a div for available here

            ]),

            html.Div(id='reimbursement', style={'margin': '30px'}, children=[
                
                html.H3('Reimbursement'),

                round(reimbursement(transactions))
            ]),

            # Add a div for available here

                html.Div(id='investment', style={'margin': '30px'}, children=[
                
                html.H3('Investment'),

                "TBD"
            ]),

            # Add a div for investment here


            ]),
            
        ]),

        html.Div(id='balance', children=[
            
            html.H2('Balance'),
            # Add more components for section 2 here

            # adding a flexbox for the balance section

            html.Div(id='balance-2', style={'display':'flex'},children=[

                html.Div(id='trend-graph', style={'margin': '10px'}, children=[

                    dcc.Graph(figure=spend_earn_fig(transactions, budget))
                
                ]),

                html.Div(id='balance-graph', style={'margin': '10px'}, children=[

                    dcc.Graph(figure=accounts_fig_gen(transactions))
                ]),
        ]),
        
        ]),

        html.Div(id='budget', children=[
            
            html.H2('Budget'),
            
            html.Div(id='budget-2', style={'display':'flex'},children=[
                
                html.Div(id='budget-table-div', style={'margin': '10px'}, children=[

                    dash_table.DataTable(

                        id='budget-table',
                        columns=[{"name": i, "id": i} for i in budget[['budget_head', 'goal', 'budgetted', 'debit', 'mean']].columns],
                        data=budget[['budget_head', 'goal', 'budgetted', 'debit', 'mean']].to_dict('records'),
                    )

                
                ]),

                html.Div(id='budget-graph', style={'margin': '10px'}, children=[

                    dcc.Graph(figure=budget_fig_gen(transactions))
                ]),
        ]),

        ]),

        html.Div(id='Income', children=[
            
            html.H2('Income Summary'),
            # Add more components for section 4 here

            html.Div(id='income-2', style={'display':'flex'},children=[
                
                html.Div(id='income-table-div', style={'margin': '10px'}, children=[

                    dash_table.DataTable(

                        id='income-table',
                        columns=[{"name": i, "id": i} for i in income_high(transactions, budget).columns],
                        data=income_high(transactions, budget).to_dict('records'),
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto'
                            },
                    )

                
                ]),

                html.Div(id='income-graph', style={'margin': '10px'}, children=[

                    dcc.Graph(figure=income_fig_gen(transactions, budget))
                ]),

        ]),

        ]),
        

        html.Div(id='Expense', children=[
            
            html.H2('Expense Summary'),
            # Add more components for section 4 here

            html.Div(id='expense-2', style={'display':'flex'},children=[
                
                html.Div(id='expense-table-div', style={'margin': '10px'}, children=[

                    dash_table.DataTable(

                        id='expense-table',
                        columns=[{"name": i, "id": i} for i in expense_high(transactions, budget).columns],
                        data=expense_high(transactions, budget).to_dict('records'),
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto'
                            },
                    )

                
                ]),

                html.Div(id='expense-graph', style={'margin': '10px'}, children=[

                    dcc.Graph(figure=expense_fig_gen(transactions, budget))
                ]),

        ]),

        ]),

        html.Div(id='debts', children=[
            
            html.H2('Debts'),

            html.Div(id='debts-2', style={'display':'flex'},children=[

                html.Div(id='loaned', style={'margin': '30px'}, children=[
                
                html.H3('Loaned Money'),
                
                current_debt(debt)[1]
                # Add a div for diplaying networth here

            ]),

            html.Div(id='owed', style={'margin': '30px'}, children=[
                
                html.H3('Owed Money'),
                
                current_debt(debt)[2]
                # Add a div for diplaying networth here

            ]),

            ]),
        ]),

        html.Div(id='investments', children=[

            html.H2('Investments'),
            # Add more components for section 7 here
        
        ]), 
    
    ])
    
    return layout

app.layout = serve_layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)