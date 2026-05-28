import streamlit as st

from supabase import (
    create_client,
    Client
)

# =====================================================
# SUPABASE CONFIG
# =====================================================

SUPABASE_URL = st.secrets[
    "SUPABASE_URL"
]

SUPABASE_KEY = st.secrets[
    "SUPABASE_KEY"
]

# =====================================================
# CREATE CLIENT
# =====================================================

supabase: Client = create_client(

    SUPABASE_URL,

    SUPABASE_KEY
)