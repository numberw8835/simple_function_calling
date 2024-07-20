# main.py
from Agent import Agent
from functions import functions
import utils  # Import the utils module


agent = Agent(available_functions=functions, verbose=False)
task = "What's the weather in Egypt?"
context = ""
llm_response = agent.execute(task, context)

if llm_response:
    function_name = llm_response["name"]
    parameters = llm_response["parameters"]
    try:
        # Now, call the functions directly from the utils module
        result = getattr(utils, function_name)(**parameters)
        print(result)
    except AttributeError:  # Handle cases where the function is not found in utils
        print(f"Function '{function_name}' not found in utils module.")
    except TypeError as e:
        print(f"Error calling function '{function_name}': {e}")
else:
    print("I don't have enough information to do that. Please try another query.")