import serial
import time
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash_daq import DarkThemeProvider as DarkThemeProvider
from dash.dependencies import State, Input, Output


app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True


def rgb_convert_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

# Set COM Port Here:
ser = serial.Serial("COM8")
ser.flush()

# CSS Imports
external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://rawgit.com/matthewchan15/dash-spark-icon-sheet/master/css/Dash-Sparki.css"]


for css in external_css:
    app.css.append_css({"external_url": css})

# root_layout = html.Div(
#     [
#         dcc.Location(id='url', refresh=False),
#         html.Div(
#             [
#                 daq.ToggleSwitch(
#                     id='toggleTheme',
#                     style={
#                         'position': 'absolute',
#                         'transform': 'translate(-50%, 20%)'
#                     },
#                     size=25
#                 ),
#             ], id="toggleDiv",
#             style={
#                 'width': 'fit-content',
#                 'margin': '0 auto'
#             }
#         ),
#         html.Div(id='page-content'),
#     ]
# )

app.layout = html.Div(
    [
        html.Div(
            id="container",
            style={"background-color": "#20304C"},

            children=[
               html.H2(
                   "Dash DAQ: Sparki Control Panel",
               ),
                html.A(
                   html.Img(
                       src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png",
                   ),
                   href="http://www.dashdaq.io"
               )

            ],
            className="banner"
        ),
        html.Div(
            [
                html.Div(   
                    [    
                        html.H5("LED Color",
                        id="led-title",
                        style={"textAlign":"center"}
                        ),
                        html.Div(
                            [
                            daq.ColorPicker(
                            id="led-control",
                            label=" ",
                            size=130,
                            value={'rgb':{'r':151, 'g':215, 'b':244, 'a':1}}
                            )
                            ]
                    )    
                    ], className="two columns offset-by-one"
                ),
                html.Div(
                    [
                           html.H5("Motion",
                                            id="motion-title",
                                            style={"textAlign": "center"}
                                            ),
                                    daq.StopButton(
                                        id="move-up",
                                            buttonText="Up",
                                            style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center"}
                                    ),
                                    daq.StopButton(
                                        id="move-down",
                                            buttonText="Down",
                                            style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center"}
                                    ),
                                    daq.StopButton(
                                        id="move-left",
                                            buttonText="Left",
                                            style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center"}
                                    ),
                                     daq.StopButton(
                                        id="move-right",
                                            buttonText="Right",
                                            style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center"}
                                    ),
                                     html.H7(
                                                "Gripper",
                                                style={"textAlign":"center"}
                                            ),
                                    html.Div(
                                        [
                                            daq.StopButton(
                                                id="start-grip",
                                                buttonText="Start",
                                                style={"display": "flex",
                                                       "justify-content": "center",
                                                       "align-items": "center"},
                                                className="three columns",
                                                size=65
                                            ),
                                            daq.StopButton(
                                                id="close-grip",
                                                buttonText="Close",
                                                style={"display": "flex",
                                                       "justify-content": "center",
                                                       "align-items": "center"},
                                                className="three columns",
                                                size=65
                                            ),
                                            daq.StopButton(
                                                id="stop-grip",
                                                buttonText="Stop",
                                                style={"display": "flex",
                                                       "justify-content": "center",
                                                       "align-items": "center"},
                                                className="three columns",
                                                size=65
                                            )
                                        ], className="row",
                                           style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center"}
                                    )
                    ], className="four columns"
                ),
                html.Div(
                    [
                        html.H5(
                            " ",
                            id="sparki-icon",
                            style={"paddingLeft": "",
                                   "paddingTop": "","font-size":"30px",
                                   "color":""},
                            className="icon-sparki"
                        ),
                    ], className="five columns", style={"border-width": "5px",
                                                        "border": "1px solid black",
                                                        "border-radius": "5px",
                                                        "height": "350px",
                                                        "width": "350px"}
                ),
            ], className='row', style={"marginTop": "5%"}
        ),
        html.Div(
            [   
                html.Div(
                                [
                                    html.H5("Ultrasonic Data",
                                            id="data-title",
                                            style={"textAlign": "center"}
                                            ),
                                    html.Div(
                                        [
                                    daq.LEDDisplay(
                                        id="ultra-sonic-data",
                                        label=" ",
                                        value="0.00",
                                        size=35,
                                    ),
                                            html.Div([
                                                html.H5(
                                                "cm",
                                                id="unit-holder",
                                                style={"border-radius": "3px",
                                                       "border-width": "5px",
                                                       "border": "1px solid rgb(216, 216, 216)",
                                                       "font-size": "46px",
                                                       "color": "#2a3f5f",
                                                       "display": "flex",
                                                       "justify-content": "center",
                                                       "align-items": "center",
                                                       "width": "110%",
                                                       "marginRight":"2%"
                                                       }
                                            ),
                                        ], style= {"paddingTop":"2.5%",
                                                   "paddingLeft":"1%",
                                                   "width":"22%"}
                                    )
                                        ], className="row",
                                        style={"display": "flex",
                                               "justify-content": "center",
                                               "align-items": "center",
                                               "paddingRight":"3%"
                                               }
                                    ),
                                    daq.Indicator(
                                        id="ultrasonic-light",
                                        color="#EF553B",
                                        label="Object Detected",
                                        value=True,
                                        style={"marginTop":"10%"}
                                    )
                                ], className = "four columns"
                            ),
                            html.Div(
                                [   
                                    html.Div(
                            [   html.H5("Noise",
                                id="noise-title",
                                style={"textAlign": "center"}
                                ),
                                html.Div(
                                    [
                                        daq.Knob(
                                            id="knob-pitch",
                                            label=" ",
                                            size=100,
                                            value=261,
                                            color="#FF5E5E",
                                            max=440,
                                            min=261,
                                            scale={"custom":{'440':"A", "415":"G#", "392":"G", "370":"F#", "349":"F", "330":"E","311":"D#","294":"D", "277":"C#", "261":"C" }}
                                        ),
                                        daq.StopButton(
                                            id="stop-beep",
                                            buttonText="Beep",
                                            style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center"}
                                        )
                                    ]
                                ),
                            ]
                        )
                                ], className = "two columns"
                            ),
                html.Div(
                    [
                        dcc.Textarea(
                            id="object-detection",
                            placeholder='Enter a value...',
                            value='This is a TextArea component',
                            style={'width': '89%', "marginTop": "2%"}
                        )
                    ], className="four columns offset-by-one"
                )
            ], className='row'
        ),
        html.Div(
            [
                html.Div(id="command-string"),
                html.Div(id="color-hold"),
                html.Div(id="beep-hold"),
                html.Div(id="grip-hold"),
                html.Div(id="motor-hold"),
                html.Div(id="case-hold"),
                html.Div(id="grip-start"),
                html.Div(id="grip-close"),
                html.Div(id="grip-stop"),
                html.Div(id="up-move"),
                html.Div(id="down-move"),
                html.Div(id="left-move"),
                html.Div(id="right-move"),
                html.Div(id="ultrasonic-hold"),
                dcc.Interval(
                            id="ultra-measure",
                            interval=1000,
                            n_intervals=0,
                        )

            ], style={"visibility": "hidden"}
        )
    ], style={'padding': '0px 10px 0px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "1100",
              'height': "1000",
              'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
)

# app.layout = root_layout
# Color Picker 
# @app.callback(
#     Output("sparki-icon", "style"),
#     [Input("led-control", "value")]
# )
# def color_picker(color):
#     r = RGB_color['rgb']['r']
#     g = RGB_color['rgb']['g']
#     b = RGB_color['rgb']['b']

#     hex_color = rgb_convert_hex(r, g, b)
#     print(hex_color)
#     return color[hex_color]
# Command String
@app.callback(
    Output("grip-start", "children"),
    [Input("start-grip", "n_clicks")]
)
def grip_start(grip):
    return time.time()
@app.callback(
    Output("grip-close", "children"),
    [Input("close-grip", "n_clicks")]
)
def grip_close(grip):
    return time.time()
@app.callback(
    Output("grip-stop", "children"),
    [Input("stop-grip", "n_clicks")]
)
def grip_close(grip):
    return time.time()    
@app.callback(
    Output("up-move", "children"),
    [Input("move-up", "n_clicks")]
)
def move_up(move):
    return time.time()
@app.callback(
    Output("down-move", "children"),
    [Input("move-down", "n_clicks")]
)
def move_down(move):
    return time.time()   
@app.callback(
    Output("left-move", "children"),
    [Input("move-left", "n_clicks")]
)
def move_left(move):
    return time.time()   
@app.callback(
    Output("right-move", "children"),
    [Input("move-right", "n_clicks")]
)
def move_right(move):
    return time.time()    

@app.callback(
    Output("command-string", "children"),
    [Input("up-move", "children"),
     Input("left-move", "children"),
     Input("down-move", "children"),
     Input("right-move", "children"),
     Input("grip-start", "children"),
     Input("grip-close", "children"),
     Input("grip-stop", "children"),
     Input("color-hold", "children"),
     Input("beep-hold", "children")]
)
def command_string(move_up, move_left, move_down, move_right, grip_open, grip_close, grip_stop, color_hold, beep_hold):

    master_command = {"UP": move_up,"LEFT": move_left, "RIGHT": move_right, "DOWN": move_down, "OPEN": grip_open, "CLOSE": grip_close, "STOP": grip_stop, "LED": color_hold, "BEEP": beep_hold}
    recent_command = max(master_command, key=master_command.get)
    print(recent_command)
    return recent_command

# Case Select
@app.callback(
    Output("motor-hold", "children"),
    [Input("move-up", "n_clicks"),
     Input("move-down", "n_clicks"),
     Input("move-left", "n_clicks"),
     Input("move-right", "n_clicks")]
)
def case_motor(motor_case_up, motor_case_down, motor_case_left, motor_case_right):
    return time.time()

@app.callback(
    Output("grip-hold", "children"),
    [Input("start-grip", "n_clicks"),
     Input("close-grip", "n_clicks"),
     Input("stop-grip", "n_clicks"),]
)
def case_gripper(grip_case, close_case, stop_case):
    return time.time()
    
@app.callback(
    Output("color-hold", "children"),
    [Input("led-control", "value")]
)
def case_LED(color_case):
    return time.time()

@app.callback(
    Output("beep-hold", "children"),
    [Input("stop-beep", "n_clicks")]
)
def case_beep(beep_case):
    return time.time()

@app.callback(
    Output("case-hold", "children"),
    [Input("beep-hold", "children"),
    Input("grip-hold", "children"),
    Input("color-hold", "children"),
    Input("motor-hold", "children")]
)
def case_master(beep_case, grip_case, color_case, motor_case):
    
    master_case = {"1": motor_case,"2": grip_case, "3": color_case, "4": beep_case}
    recent_case = max(master_case, key=master_case.get)
    return recent_case

# Ultrasonic Response
@app.callback(
    Output("ultrasonic-hold", "children"),
    [Input("ultra-measure", "n_intervals")]
)

def ultrasonic_response(interval_rate):
    response = ser.readline().decode("ASCII")
    response = response.split("\r\n")[0]
    print(response)
    
    return response

# Ultrasonic Response
@app.callback(
    Output("ultra-sonic-data", "value"),
    [Input("ultrasonic-hold", "children")]
)

def ultrasonic_display(response):
    
    if response == "-1":
        return "999"
    elif int(response) >= 100:
        return int(response)
    response = float(response)
    response = "%.2f" % response
    print(response)
    response = (f"{response:{4}.{4}}")
    print(response)
    response = str(response)
    return response

# Ultrasonic Response
@app.callback(
    Output("ultrasonic-light", "color"),
    [Input("ultrasonic-hold", "children")]
)

def ultrasonic_display(response):
    if response == "-1":
        return "#EF553B"
    return "#00cc96"

# Output to Sparki
@app.callback(
    Output("object-detection", "value"),
    [Input("command-string", "children")],
    [State("case-hold", "children"),
     State("knob-pitch", "value"),
     State("led-control", "value")]
     
)
def central_command(command, case_master, beep_freq, RGB_color):
    print(RGB_color)
    R = RGB_color['rgb']['r']
    G = RGB_color['rgb']['g']
    B = RGB_color['rgb']['b']

    beep_freq = int(beep_freq)

    command = "<{},{},{},{},{},{}>".format(command, case_master, beep_freq, R, G, B)
    send = command.encode("ASCII")
    ser.write(send)
    print(command)
    return "Command: " + command



if __name__ == '__main__':

    app.run_server(debug=False)