# Import necessary libraries and modules
from shiny import App, ui, reactive  # For building the Shiny application
from maplibre import (
    Map,
    MapOptions,
    MapContext,
    Layer,
    LayerType,
    output_maplibregl,
    render_maplibregl,
)  # MapLibre library for map rendering and interaction
from maplibre.basemaps import Carto  # Predefined basemap styles
from maplibre.controls import (
    NavigationControl,
    ControlPosition,
)  # Navigation controls for the map

# Define the user interface with a sidebar and map output
app_ui = ui.page_sidebar(
    ui.sidebar(
        # Add a slider input for filtering data by year
        ui.input_slider(
            "year_slider",
            "Filter by Year:",
            min=1980,  # Minimum year value
            max=2020,  # Maximum year value
            value=[1980, 2020],  # Default range for the slider
            step=1,  # Increment step for the slider
            sep="",  # No comma separator in numbers
        ),
    ),
    # Add the map output element with a full height
    output_maplibregl("map", height="100%"),
    # Include custom CSS for additional styling
    ui.include_css("./styles.css"),
    # Set the page title and enable fillable layout
    title="Canadian National Fire Database (CNFDB)",
    fillable=True,
)


# Define the server-side logic for the application
def server(input, output, session):
    # Define the rendering function for the MapLibre map
    @render_maplibregl
    def map():
        # Create a Map object with specified basemap, center, and zoom level
        m = Map(MapOptions(style=Carto.POSITRON, center=(-125, 55), zoom=4))

        # Add navigation controls to the map at the top-right corner
        m.add_control(NavigationControl(), ControlPosition.TOP_RIGHT)

        # Define and add a vector tile layer for the NFDB dataset
        tile_layer = Layer(
            type=LayerType.FILL,  # Define the layer type (fill layer)
            id="nfdb",  # Unique identifier for the layer
            source={
                "type": "vector",  # Source type: vector tiles
                "url": "http://127.0.0.1:3000/nfdb",  # URL to the vector tile source
            },
            paint={
                "fill-color": "#B30000",  # Fill color for the polygons
                "fill-opacity": 0.5,  # Transparency level of the fill
            },
            source_layer="nfdb",  # Specify the source layer name
        )
        m.add_layer(tile_layer)  # Add the layer to the map
        m.add_tooltip("nfdb")  # Enable tooltips for the layer

        return m  # Return the configured map

    # Reactive effect triggered by changes in the year slider input
    @reactive.Effect
    @reactive.event(input.year_slider)
    async def filter_map():
        # Update the map filter dynamically based on the year slider range
        async with MapContext("map") as m:
            m.set_filter(
                "nfdb",  # Apply the filter to the "nfdb" layer
                [
                    "all",  # Combine multiple conditions
                    [
                        ">=",
                        ["get", "YEAR"],
                        input.year_slider()[0],
                    ],  # YEAR >= start of slider range
                    [
                        "<=",
                        ["get", "YEAR"],
                        input.year_slider()[1],
                    ],  # YEAR <= end of slider range
                ],
            )


# Create the Shiny app by combining the UI and server logic
app = App(app_ui, server)
