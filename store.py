from shiny import App, render, ui, reactive
import pandas as pd

# load the data
df=pd.read_csv("pishori.csv")

### define ui

app_ui= ui.page_fluid(
    ui.h2( 'Pishori Pride' ),
    ui.layout_columns(
        ui.card(
        ui.h3("Pishori Rice"),
        ui.p(
            "Pishori rice is a fragrant, long-grain rice grown in East Africa. "
            "It is known for its aroma, fluffy texture, and is often used for special occasions. "
            "Rich in nutrients, it cooks beautifully and is ideal for pilau or plain steamed rice."
        )
    ),
        ui.card(ui.h4('Available Rice'),
                ui.output_table('rice_table')
                ),#end of card
           ui.card(ui.h4('Order'),
               ui.input_select('product','slect Rice Type:', df['Name'].to_list()),
               ui.input_numeric('quantity', 'Quantity in Kgs:', value=1, min=1),
               ui.hr(),
               ui.h4('Total Price:'),
               ui.output_text('total')
           )   #end of card

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
        df['Name_Clean']=df['Name'].str.strip().str.lower()
        row= df[df['Name_Clean']==product]
        if row.empty:
            return 0
        price= pd.to_numeric(row['Price'].iloc[0], errors='coerce')
        return price

    @output
    @render.text
    def total():
        Price= selected_price() 
        qty= input.quantity()
        if Price == 0:
            return "price not found"
        total_cost= Price * qty
        return f"KES {total_cost}"

### run the app
app = App(app_ui, server)