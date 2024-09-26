import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf


#  Fetch the stock data with additional parameters
def get_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)  # Fetch data within the specified date range
    return data


#  Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "font-family": "Arial, sans-serif",
        "margin": "10px auto",
        "max-width-left": "880px",  # Set the maximum width of the content container
        "text-align": "center",
        "padding-left": "0",
        "padding-right": "0",
        "background-color": "lightgreen",
        "margin-top": "0px",
        "padding-bottom": "5px",
    },
    children=[
        html.Nav(
            style={
                "background-color": "lightgray",
                "padding": "10px",
                "margin-bottom": "10px",
            },
            children=[
              

                html.A("Home", href="/", style={"margin-right": "10px"}),
                html.A("About", href="/about", id="about-link", style={"margin-right": "10px"}),
                html.A("Contact", href="/contact"),
            ]
        ),
       
        html.H1("Stock Visualization and Forecasting"),
        html.Div(
            style={
                "margin-bottom": "20px",
            },
            children=[
                html.Div(
                    style={"display": "flex", "justify-content": "center"},
                    children=[
                        html.Div(
                            style={"margin-right": "10px"},
                            children=[
                                html.Label("Stock Symbol "),
                                dcc.Input(
                                    id="input-symbol",
                                    type="text",
                                    placeholder="Enter a stock symbol",
                                    style={
                                        "padding": "5px",
                                        "font-size": "16px",
                                        "width": "200px",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            style={"margin-right": "10px"},
                            children=[
                                html.Label("Start Date "),
                                dcc.Input(
                                    id="input-start-date",
                                    type="text",
                                    placeholder="Enter a start date (YYYY-MM-DD)",
                                    style={
                                        "padding": "5px",
                                        "font-size": "16px",
                                        "width": "200px",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            children=[
                                html.Label("End Date "),
                                dcc.Input(
                                    id="input-end-date",
                                    type="text",
                                    placeholder="Enter an end date (YYYY-MM-DD)",
                                    style={
                                        "padding": "5px",
                                        "font-size": "16px",
                                        "width": "200px",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={"margin-top": "10px"},
                    children=[
                        html.Label("Indicators"),
                        dcc.Dropdown(
                            id="input-indicators",
                            options=[
                                {"label": "Open", "value": "Open"},
                                {"label": "High", "value": "High"},
                                {"label": "Low", "value": "Low"},
                                {"label": "Close", "value": "Close"},
                                {"label": "Volume", "value": "Volume"},
                            ],
                            value=["Close"],
                            multi=True,
                            style={
                                "font-size": "16px",
                                "width": "400px",
                                "margin": "auto",
                            },
                        ),
                    ],
                ),
                html.Button(
                    "Submit",
                    id="submit-button",
                    n_clicks=0,
                    style={
                        "margin-top": "10px",
                        "padding": "5px 10px",
                        "font-size": "16px",
                        "background-color": "green",
                        "color": "white",
                    },
                ),
            ],
        ),
        dcc.Graph(id="output-graph"),
        html.Div(id="output-info"),

        html.Footer(
            style={
                "background-color": "white",
                "padding": "10px",
                "color": "black",
                "border-top": "1px solid #ccc",
                "margin-height": "-5px",
            },
            children=[
                html.P("Powered by SVF"),
                html.P(
                    "Our cutting-edge platform empowers investors with advanced stock visualization and forecasting tools, revolutionizing the way you analyze and predict market trends. With our intuitive interface and powerful algorithms, you'll gain valuable insights to make informed investment decisions."
                ),
                html.P("© 2023 SVF. All rights reserved."),
            ],
        ),
    ],
)

#  Define the callback functions
@app.callback(
    Output(component_id="output-graph", component_property="figure"),
    Output(component_id="output-info", component_property="children"),
    [
        Input(component_id="submit-button", component_property="n_clicks"),
        Input(component_id="input-symbol", component_property="value"),
        Input(component_id="input-start-date", component_property="value"),
        Input(component_id="input-end-date", component_property="value"),
        Input(component_id="input-indicators", component_property="value"),
    ],
)
def update_graph(n_clicks, stock_symbol, start_date, end_date, indicators):
    if n_clicks is None:
        # Initial load or no button click yet
        return go.Figure(), ""

    if n_clicks > 0 and stock_symbol and start_date and end_date:
        data = get_stock_data(stock_symbol, start_date, end_date)

        # Create subplots with shared x-axis
        fig = make_subplots(shared_xaxes=True)

        # Add line plots for each selected indicator
        for indicator in indicators:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[indicator],
                    name=indicator,
                    mode="lines",
                ),
                secondary_y=False,
            )

        fig.update_layout(
            title="Stock Analysis and Visualization Suite:",
            xaxis_title="Date",
            yaxis_title="Price",
        )

        # Fetch company logo and information
        stock = yf.Ticker(stock_symbol)
        company_info = stock.info.get(
            "longBusinessSummary", "No information available."
        )
        logo_url = stock.info.get("logo_url", "")

        info_html = html.Div(
            style={"margin-top": "20px", "font-size": "18px", "padding-right": "0", "padding-left": "0"},
            children=[
                html.P(company_info),
                html.Img(src=logo_url, style={"max-width": "100px"}),
            ],
        )

        return fig, info_html
    else:
        return go.Figure(), ""


#  Define the routes for the About and Contact pages
@app.server.route("/about")
def render_about_page():
    about_content = """
    <div style="padding: 20px;">
                    <a href="/" style="text-decoration: none; color: #000; font-size: 16px; margin-bottom: 10px;">  ←Go Back </a>

        <h1>ABOUT US:</h1>
        <h2>Stock Visualization and Forecasting</h2>
        <p>
            Stock Visualization and Forecasting (SVF) is a cutting-edge platform that empowers investors with advanced tools to analyze and predict market trends. With our intuitive interface and powerful algorithms, SVF provides valuable insights for making informed investment decisions.
        </p>
        <p>
            Our platform combines the power of data visualization with forecasting techniques to help investors understand stock price movements, identify patterns, and uncover potential opportunities. By visualizing stock data on interactive graphs and leveraging predictive models, SVF enables users to gain a deeper understanding of the market dynamics.
        </p>
        <p>
            Whether you are a seasoned investor or just starting, SVF equips you with the tools to explore historical stock data, analyze key indicators, and forecast future price movements. Make smarter investment decisions and stay ahead in the ever-changing market with SVF.
        </p>
        
         <h3>Benefits of Stock Visualization:</h3>
         <p>
         1) Pattern Recognition: Visualizing stock data can reveal patterns such as trends, cycles, and chart formations, which can aid in making informed trading decisions.</br>
         2) Market Analysis: Interactive graphs and charts allow investors to analyze historical price movements, volume patterns, and technical indicators to assess the market conditions and identify potential opportunities.</br>
         3) Risk Management: Visualizing risk metrics, such as volatility or drawdowns, can assist in managing risk and optimizing portfolio allocation.</br>
         4) Communication and Reporting: Visual representations make it easier to communicate insights and findings to stakeholders, clients, or team members.</br>

         </p>
        </div>    
        
        <div style="background-color: white; padding: 20px; text-align: center;">
                        <hr style="border: 1px solid #ccc; margin-bottom: 20px auto; width: 100%;">

            <p>Powered by SVF</p>
            <p>
                Our cutting-edge platform empowers investors with advanced stock visualization and forecasting tools, revolutionizing the way you analyze and predict market trends. With our intuitive interface and powerful algorithms, you'll gain valuable insights to make informed investment decisions.
            </p>
            <p>© 2023 SVF. All rights reserved.</p>
        </div>
    </div>
    
    """
    return about_content




@app.server.route("/contact")
def render_contact_page():
    contact_content = """
    <div style="display: flex; flex-direction: column; min-height: 100vh;">
        <div style="padding: 20px;">
            <a href="/" style="text-decoration: none; color: #000; font-size: 16px; margin-bottom: 10px;"> ←Go Back</a>
        </div>
        
        <div style="flex: 1; padding: 20px;">
            <h1>Contact Us:</h1>
            <p>
                We'd love to hear from you! If you have any questions, feedback, or inquiries, please feel free to reach out to us using the contact details below:
            </p>
            <p>
                Email: contact@svf.com
            </p>
            <p>
                Phone: +1 323-453-5860
            </p>
            <p>
                Address: 134 Elm Street, Cityville, Countryland
            </p>
            
        </div>
        
        <div style="background-color: white; padding: 20px; text-align: center;">
                        <hr style="border: 1px solid #ccc; margin-bottom: 20px auto; width: 100%;">

            <p>Powered by SVF</p>
            <p>
                Our cutting-edge platform empowers investors with advanced stock visualization and forecasting tools, revolutionizing the way you analyze and predict market trends. With our intuitive interface and powerful algorithms, you'll gain valuable insights to make informed investment decisions.
            </p>
            <p>© 2023 SVF. All rights reserved.</p>
        </div>
    </div>
    """
    return contact_content



#  Run the app
if __name__ == "__main__":
    app.run_server(debug=True)



   
git branch -M main
git push -u origin main

