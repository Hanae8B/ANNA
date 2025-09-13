from core import neural

def execute_action(action_callable, action_description, query):
    """
    Executes reasoning or calculation via neural.py
    """
    try:
        response = action_callable(query)
        return response
    except Exception as e:
        return f"ANNA Error during '{action_description}': {str(e)}"
