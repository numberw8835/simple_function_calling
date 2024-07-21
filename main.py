# main.py
from Agent import Agent
from functions import functions
import utils  # Import the utils module


agent = Agent(llm="mistral:7b-instruct-v0.3-q8_0", available_functions=functions, verbose=True)
task = "I want to reverse  'Hello'"
llm_response = agent.execute(task)


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