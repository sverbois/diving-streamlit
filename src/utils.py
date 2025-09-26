import streamlit as st

from db import UserDataModel
from db import get_user

# Voir https://st-pydantic.streamlit.app/ pour des exemples de streamlit-pydantic

PPO2_VALUES = (0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6)
DEFAULT_PPO2_INDEX = 6
CYLINDER_VOLUMES = (10, 12, 14, 15, 16, 17, 18, 20, 24)
DEFAULT_CYLINDER_VOLUME_INDEX = 3


def get_user_data():
    if "user_data" not in st.session_state:
        if st.user.is_logged_in:  # authenticated user
            user = get_user(st.user.email)
            if user:  # existing user
                user_data = UserDataModel.parse_obj(user.data)
            else:  # new user
                user_data = UserDataModel(name=st.user.name, email=st.user.email)
        else:  # anonymous user
            user_data = UserDataModel()
        st.session_state["user_data"] = user_data
    return st.session_state["user_data"]


def get_missing_gases_pressures(
    cylinder_volume,
    start_pressure,
    end_pressure,
    start_he_percentage,
    end_he_percentage,
    start_o2_percentage,
    end_o2_percentage,
):
    gas_missing = (end_pressure - start_pressure) * cylinder_volume
    start_n2_percentage = 100 - start_he_percentage - start_o2_percentage
    end_n2_percentage = 100 - end_he_percentage - end_o2_percentage
    missing_he = (
        end_he_percentage / 100.0 * end_pressure * cylinder_volume
        - start_he_percentage / 100.0 * start_pressure * cylinder_volume
    )
    missing_n2 = (
        end_n2_percentage / 100.0 * end_pressure * cylinder_volume
        - start_n2_percentage / 100.0 * start_pressure * cylinder_volume
    )
    missing_air = missing_n2 / 0.79
    missing_o2 = gas_missing - (missing_he + missing_air)

    return {
        "he": missing_he,
        "air": missing_air,
        "o2": missing_o2,
    }
