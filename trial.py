from shiny import App, ui
from pathlib import Path

# Define path to static assets
www_dir = Path(__file__).parent / "www"

app_ui = ui.page_fluid(
    # Include JS in <head>
    ui.tags.head(
        ui.tags.script(src="script.js")  # your JS file in www/
    ),
    ui.h3("Shiny for Python - JavaScript Example"),
    
    # Button that calls JS function
    ui.input_action_button(id="btn", label="Click me!", onclick="runJS()"),
    
    # Paragraph to update via JS
    ui.p(id="prompt_text"),
    
    # Example image from www folder
    ui.tags.img(src="pic_1.png", width="300px")  # your image in www/
)

def server(input, output, session):
    pass

# Create the app and serve static assets from www_dir
app = App(ui=app_ui, server=server, static_assets=www_dir)


