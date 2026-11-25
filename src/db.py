import streamlit as st
from pydantic import BaseModel
from sqlalchemy import text

USER_TABLE_NAME = "diving_users"


class UserPreferences(BaseModel):
    rmv: int = 20
    descent_speed: int = 20


def get_connection():
    return st.connection("db", type="sql")


@st.cache_resource
def initialize_db():
    with get_connection().session as s:
        s.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
                    email       TEXT PRIMARY KEY,
                    preferences JSONB NOT NULL DEFAULT '{{}}',
                    first_seen  TIMESTAMPTZ NOT NULL DEFAULT now(),
                    last_seen   TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )
        )
        s.commit()


def record_visit(email) -> UserPreferences:
    with get_connection().session as s:
        preferences = s.execute(
            text(
                f"""
                INSERT INTO {USER_TABLE_NAME} (email) VALUES (:email)
                ON CONFLICT (email) DO UPDATE SET last_seen = now()
                RETURNING preferences;
                """
            ),
            {"email": email},
        ).scalar_one()
        s.commit()
    return UserPreferences.model_validate(preferences)


def save_preferences(email, preferences: UserPreferences):
    with get_connection().session as s:
        s.execute(
            text(f"UPDATE {USER_TABLE_NAME} SET preferences = CAST(:preferences AS JSONB) WHERE email = :email"),
            {"email": email, "preferences": preferences.model_dump_json()},
        )
        s.commit()


def get_users():
    with get_connection().session as s:
        return s.execute(
            text(f"SELECT email, first_seen, last_seen, preferences FROM {USER_TABLE_NAME} ORDER BY last_seen DESC"),
        ).fetchall()
