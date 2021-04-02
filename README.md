# stock_dash
Link to site: https://stockdashpy.herokuapp.com/


Dashboard that 'incorporates interesting option market order flow, price charts, chatter and fundamentals' following Eric Kleppen's guide on Medium at https://medium.com/swlh/how-to-create-a-dashboard-to-dominate-the-stock-market-using-python-and-dash-c35a12108c93!

After following the Kleppen's initial guide on Medium, I made some additional modifications to the code. UI changes include replacing components on the page, restricting the size of datatables, and adding whitespace between components. Additionally I made changes to the underlying structure of the dashboard, changing the source of the 'Fin table' section from webscraping Marketwatch.com to utilizing IEX Cloud's api for data. I also added a database table for the reddit data, similar to the original twitter database table. Following the Medium guide also required bugfixing of the chart feature as well as the "Financial cards" feature.
