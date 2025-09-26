import json

import streamlit as st
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import text

USER_TABLE_NAME = "diving_users"


class UserDataModel(BaseModel):
    # name: str = Field(default="Anonymous", description="Nom dans l'application")
    # email: str = Field(
    #     default="anonymous@domain.com",
    #     description="Courriel",
    #     readOnly=True,
    # )
    rmv: int = Field(default=20, title="RMV in L/min")
    descent_speed: int = Field(default=20, title="Descent speed in m/min")


def initialize_db():
    conn = st.connection("supabase", type="sql")
    with conn.session as s:
        s.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
                    email TEXT PRIMARY KEY,
                    data  JSON
                );
                """
            )
        )
        s.commit()


def get_user(email):
    conn = st.connection("supabase", type="sql")
    with conn.session as s:
        user = s.execute(
            text(f"SELECT * FROM {USER_TABLE_NAME} WHERE email = :email"),
            {"email": email},
        ).fetchone()
    return user


def get_users():
    conn = st.connection("supabase", type="sql")
    with conn.session as s:
        users = s.execute(
            text(f"SELECT * FROM {USER_TABLE_NAME}"),
        ).fetchall()
    return users


def save_user(user_data):
    if st.user.email:
        conn = st.connection("supabase", type="sql")
        with conn.session as s:
            s.execute(
                text(
                    f"""
                    INSERT INTO {USER_TABLE_NAME} (email, data)
                    VALUES (:email, :data)
                    ON CONFLICT (email) DO UPDATE SET data = EXCLUDED.data;
                    """
                ),
                {
                    "email": st.user.email,
                    "data": json.dumps(user_data.dict()),
                },
            )
            s.commit()
        st.session_state["user_data"] = user_data
