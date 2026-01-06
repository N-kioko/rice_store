from shiny import App, render, ui, reactive
from shiny.ui import tags   
import pandas as pd
from pathlib import Path

# load the data
df=pd.read_csv(".gitignore/pishori.csv")
# clean the Name column for reliable matching
df["Name_Clean"] = df["Name"].str.strip().str.lower()  
# load shipping options
shipping_df=pd.read_csv(".gitignore/shipping.csv")
#convert to dictionary for easy access
shipping_options= dict(zip(shipping_df['option'], shipping_df['shipping_cost_in_ksh']))

# Define path to static assets
www_dir = Path(__file__).parent / "www"

### define ui

app_ui= ui.page_fluid(
    ui.h2('Pishori Pride', style="text-align: center; margin-bottom: 30px;background-color: #8B4513;  /* brown color */",
       ),
    ui.layout_columns(
#product info card
        ui.card(
        ui.h3("Pishori Rice"),
        ui.img(src="pic_1.png", height="400px"),
        ui.p("Pishori rice is a fragrant, long-grain rice grown in East Africa. "
            "It is known for its aroma, fluffy texture, and is often used for special occasions. "
            "Rich in nutrients, it cooks beautifully and is ideal for pilau or plain steamed rice.")
            ), #end of card 
#order card
        ui.card(
            ui.h4("Order"),
            ui.input_select("product", "Select Rice Type:", df["Name"].to_list()),
            ui.input_numeric("quantity", "Quantity in Kgs:", value=1, min=1),
            ui.input_select("shipping_option", "Shipping Option:", list(shipping_options.keys())),
            ui.hr(),
            ui.input_action_button("add_to_cart", "Add to Cart", class_="btn btn-success"),
            ui.hr(),
            ui.h4("Total Price:"),
            ui.output_text("total")
           ),   #end of card
#cart card with checkout button
        ui.card(
            ui.h3("🛒 Shopping Cart"),
            ui.output_ui("cart_table"),
            ui.h4(ui.output_text("cart_total")),
            ui.hr(),
            ui.input_action_button("checkout", "Checkout with M-Pesa", class_="btn btn-warning"),
            ui.output_text("checkout_status"),
            )  #end of card
           
    ),#end of layout columns
## extra contact card
    ui.card(
        ui.h3("Reach Pishori Pride Kenya"),
        ui.h4("Phone: +254741462886"),
        ui.h4("Address: Kerugoya Twn, Kirinyaga"),
        ui.h4("Email: pishoripride@gmail.com"),
        style="""
        margin-top: 30px; 
        background-color: #8B4513;  /* brown color */
        color: white;               /* text color white for readability */
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    """
    )
)##end of fluid page

########################################################################################################

###define server

def server(input,output, session):
   ## added add to cart functionality

    cart = reactive.Value(
        pd.DataFrame(columns=["Product", "Quantity (Kg)", "Price per Kg", "Shipping", "Subtotal"])
    )


# calculate selected product price
    @reactive.calc
    def selected_price():
        product = input.product().strip().lower()
        row = df[df["Name_Clean"] == product]
        if row.empty:
            return 0
        return pd.to_numeric(row["Price"].iloc[0], errors="coerce")

    
# calculate shipping cost based on selection
    @reactive.calc
    def selected_shipping():
        return shipping_options.get(input.shipping_option(), 0)
    
## display shipping cost
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

#Add or update items in cart
    @reactive.effect
    @reactive.event(input.add_to_cart)
    def add_to_cart():
        current_cart = cart.get().copy()
        product_name = input.product().strip()
        qty = input.quantity()
        price_per_kg = selected_price()
        shipping_fee = selected_shipping()
        if price_per_kg == 0:
            return

        subtotal = price_per_kg * qty + shipping_fee

# Update existing row if product exists
        existing_index = current_cart[current_cart["Product"] == product_name].index
        if len(existing_index) > 0:
            i = existing_index[0]
            current_cart.loc[i, "Quantity (Kg)"] += qty
            current_cart.loc[i, "Subtotal"] = current_cart.loc[i, "Quantity (Kg)"] * price_per_kg + shipping_fee
        else:
            new_item = pd.DataFrame([{
                "Product": product_name,
                "Quantity (Kg)": qty,
                "Price per Kg": price_per_kg,
                "Shipping": shipping_fee,
                "Subtotal": subtotal
            }])
            current_cart = pd.concat([current_cart, new_item], ignore_index=True)

        cart.set(current_cart)

# Render cart table with remove buttons
    @output
    @render.ui
    def cart_table():
        df_cart = cart.get()
        if df_cart.empty:
            return ui.p("Your cart is empty.")

        header = tags.tr(
            tags.th("Product"),
            tags.th("Quantity (Kg)"),
            tags.th("Price per Kg"),
            tags.th("Shipping"),
            tags.th("Subtotal"),
            tags.th("Remove"),
        )

        rows = []
        for i, row in df_cart.iterrows():
            rows.append(
                tags.tr(
                    tags.td(row["Product"]),
                    tags.td(row["Quantity (Kg)"]),
                    tags.td(f"KES {row['Price per Kg']}"),
                    tags.td(f"KES {row['Shipping']}"),
                    tags.td(f"KES {row['Subtotal']}"),
                    tags.td(
                        ui.input_action_button(f"remove_{i}", "Remove", class_="btn btn-danger btn-sm")
                    ),
                )
            )

        return tags.table(header, tags.tbody(*rows), class_="table table-striped")
    
# Handle remove button clicks
    @reactive.effect
    def remove_item():
        df_cart = cart.get().copy()
        updated = False
        for i in range(len(df_cart)):
            btn_id = f"remove_{i}"
            if btn_id in input and input[btn_id]() > 0:
                df_cart = df_cart.drop(index=i)
                updated = True
        if updated:
            cart.set(df_cart.reset_index(drop=True))

# Total cart value
    @output
    @render.text
    def cart_total():
        df_cart = cart.get()
        if df_cart.empty:
            return "Total: KES 0"
        return f"Total Cart Value: KES {df_cart['Subtotal'].sum()}"

# Checkout with M-Pesa prompt
    @reactive.effect
    @reactive.event(input.checkout)
    def checkout():
        df_cart = cart.get()
        if df_cart.empty:
            session.flash("Cart is empty! Add some items before checking out.")
            return
        session.send_message("checkout_status", "💳 M-Pesa payment ready! Please complete the payment. 😄")

    # Default checkout status
    @output
    @render.text
    def checkout_status():
        return ""
    
### run the app
app = App(app_ui, server, static_assets=www_dir)