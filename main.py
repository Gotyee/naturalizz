import streamlit as st
from pyinstrument import Profiler

from naturalizz.app_actions import (
    init_session,
)
from naturalizz.display import (
    display_image_and_result,
    display_selection_bar_and_launch_button,
)

prof = Profiler()
prof.start()
init_session()

st.title("Naturalizz", anchor=False)

display_selection_bar_and_launch_button()

try:
    display_image_and_result()
except Exception as e:
    st.exception(e)
    launch_pic = False

prof.stop()
# prof.print()
