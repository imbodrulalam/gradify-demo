# supabase_service.py
import supabase

def init_supabase_client(app):
    # Extract Supabase credentials from config
    supabase_url = app.config['SUPABASE_URL']
    supabase_key = app.config['SUPABASE_KEY']


    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and Key must be set in the environment variables.")

    # Initialize Supabase client
    supabase_client = supabase.create_client(supabase_url, supabase_key)
    
    # Store the Supabase client in the app context
    app.supabase_client = supabase_client
