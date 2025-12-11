from shiny import App, render, ui, reactive
import pandas as pd
from pathlib import Path

# load the data
df=pd.read_csv(".gitignore\pishori.csv")
# clean the Name column for reliable matching
df["Name_Clean"] = df["Name"].str.strip().str.lower()  
# load shipping options
shipping_df=pd.read_csv(".gitignore\shipping.csv")
#convert to dictionary for easy access
shipping_options= dict(zip(shipping_df['option'], shipping_df['shipping_cost_in_ksh']))

# Define path to static assets
www_dir = Path(__file__).parent / "www"

### define ui

app_ui= ui.page_fluid(
    ui.h2( 'Pishori Pride' ),
    ui.layout_columns(
        ui.card(
        ui.h3("Pishori Rice"),
        ui.img(src="pic_1.png", height="200px"),
        ui.p("Pishori rice is a fragrant, long-grain rice grown in East Africa. "
            "It is known for its aroma, fluffy texture, and is often used for special occasions. "
            "Rich in nutrients, it cooks beautifully and is ideal for pilau or plain steamed rice.")
            ), #end of card 
        ui.card(ui.h4('Order'),
               ui.input_select('product','slect Rice Type:', df['Name'].to_list()),
               ui.input_numeric('quantity', 'Quantity in Kgs:', value=1, min=1),
               ui.hr(),
               ui.h4('Total Price:'),
               ui.output_text('total')
           ),   #end of card
        ui.card(
            ui.h3("Shipping Options"),
            ui.input_select('shipping_option', 'Select Shipping Option:', list(shipping_options.keys())),
            ui.output_text('shipping_cost'))   #end of card
           
    ),#end of layout columns

)##end of fluid page

###define server
def server(input,output, session):
    @output
    @render.table
    def rice_table():
     return df

    @reactive.calc
    def selected_price():
        #normalize input
        product=input.product().strip().lower()
        row= df[df['Name_Clean']==product]
        if row.empty:
            return 0
        return pd.to_numeric(row['Price'].iloc[0], errors='coerce')
    
    @reactive.Calc
    def selected_shipping():
        return shipping_options.get(input.shipping_option(), 0)
    
    @output
    @render.text
    def shipping_cost():
        cost = selected_shipping()
        return f"KES {cost}"

    @output
    @render.text
    def total():
        price = selected_price()
        qty = input.quantity()
        shipping_fee = selected_shipping()
        if price == 0:
            return "Price not found"
        total_cost = price * qty + shipping_fee
        return f"KES {total_cost} (including shipping: KES {shipping_fee})"
    
### run the app
app = App(app_ui, server, static_assets=www_dir)