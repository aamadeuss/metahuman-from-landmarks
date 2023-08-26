import streamlit as st
from src.pylivelinkface import FaceBlendShape
import plotly.graph_objects as graph

state = st.session_state
if 'computed' not in state:
    state.computed = False
if state.computed:
    output = state.save
    blend_name = st.selectbox(label='Select blendshape to plot:',
                 options=[str(x)[15:] for x in list(FaceBlendShape)])
    blend_values = [x.get_blendshape(FaceBlendShape[blend_name]) for x in output]
    fig = graph.Figure(data=graph.Scatter(y=blend_values), layout=graph.Layout(title=blend_name, colorway=['#23f43e']))
    st.plotly_chart(fig, use_container_width=True)
    # plt.show()
else:
    st.write('# No data to plot yet.\nPlease submit the JSONs folder and the conversion model for computing blendshapes.')