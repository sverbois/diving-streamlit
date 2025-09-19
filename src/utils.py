import json

import streamlit as st
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import text

# Voir https://www.sqlitetutorial.net/sqlite-json/ pour l'utilisation de JSON avec SQLite
# Voir https://st-pydantic.streamlit.app/ pour des exemples de streamlit-pydantic


class UserDataModel(BaseModel):
    # name: str = Field(default="Anonymous", description="Nom dans l'application")
    # email: str = Field(
    #     default="anonymous@domain.com",
    #     description="Courriel",
    #     readOnly=True,
    # )
    rmv: int = Field(default=20, title="RMV en L/min")


def initialize_session():
    if "user_data" not in st.session_state:
        if st.user.is_logged_in:
            conn = st.connection("sqlite", type="sql")
            with conn.session as s:
                s.execute(
                    text(
                        """
                    CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        data  JSON CHECK (json_valid(data))
                    );
                    """
                    )
                )
                s.commit()

            with conn.session as s:
                sqlite_current_user = s.execute(
                    text("SELECT data FROM users WHERE email = :email"),
                    {"email": st.user.email},
                ).fetchone()

            if sqlite_current_user:  # existing user
                user_data = UserDataModel.parse_raw(sqlite_current_user._mapping["data"])
            else:  # new user
                user_data = UserDataModel(name=st.user.name, email=st.user.email)
        else:  # anonymous user
            user_data = UserDataModel()
        st.session_state["user_data"] = user_data


def save_user_data(user_data):
    if st.user.is_logged_in:
        conn = st.connection("sqlite", type="sql")
        with conn.session as s:
            s.execute(
                text(
                    """
                    INSERT OR REPLACE INTO users (email, data)
                    VALUES (:email, :data);
                    """
                ),
                {
                    "email": st.user.email,
                    "data": json.dumps(user_data.dict()),
                },
            )
            s.commit()
        st.session_state["user_data"] = user_data


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
