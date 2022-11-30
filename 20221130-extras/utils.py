from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.app_logo import add_logo


def init():
    add_logo(
        "https://raw.githubusercontent.com/andfanilo/social-media-tutorials/master/20221130-extras/logo.png"
    )
    button(username="andfanilo", floating=True, width=222)
