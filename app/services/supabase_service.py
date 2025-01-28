from flask import current_app


def insert_data(table, data):
    try:
        response = current_app.supabase_client.table(table).insert(data).execute()
        return response.get("data", [])
    except Exception as e:
        return {"error": str(e)}

def update_data(table, condition, updates):
    try:
        response = current_app.supabase_client.table(table).update(updates).eq(**condition).execute()
        return response.get("data", [])
    except Exception as e:
        return {"error": str(e)}

def delete_data(table, condition):
    try:
        response = current_app.supabase_client.table(table).delete().eq(**condition).execute()
        return response.get("data", [])
    except Exception as e:
        return {"error": str(e)}

def fetch_data(table, condition=None):
    try:
        query = current_app.supabase_client.table(table).select("*")
        if condition:
            query = query.eq(**condition)
        response = query.execute()
        return response.get("data", [])
    except Exception as e:
        return {"error": str(e)}
