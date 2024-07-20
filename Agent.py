from langchain_community.llms import Ollama
from textwrap import dedent
import json


class Agent:
    def __init__(self, llm="mistral", available_functions=None, verbose=False):
        self.verbose = verbose
        self.available_functions = available_functions or []  # Default to empty list
        self.agent = Ollama(
            model=llm,
            temperature=0.0,  # Set temperature based on desired determinism
            format='json',
        )

    def execute(self, task, context=None):
        schema = {
            "name": "string",
            "description": "string",
            "parameters": {},  # Initialize as empty dict
        }
        null_schema = {
            "name": "NULL",
            "description": "NULL",
            "parameters": {},
        }

        # Construct a clear prompt with better formatting
        prompt = dedent(f"""
            Context: {context if context else "None"}
            Task: {task}

            Available functions:
            {json.dumps(self.available_functions, indent=2)}  # Format for readability

            Select the most suitable function and its parameters using the following schema:
            {json.dumps(schema, indent=2)}

            If no function applies, return:
            {json.dumps(null_schema, indent=2)}
        """)

        if self.verbose:
            print("Prompt:", prompt)

        response = self.agent.invoke(prompt)

        if self.verbose:
            print("Raw Response:", response)  # Show unprocessed output for debugging

        try:
            response_json = json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")

        if response_json["name"] == "NULL":
            if self.verbose:
                print("No suitable function found.")
            return None

        # Robust parameter validation
        if not all(key in response_json for key in schema):
            raise ValueError("Missing keys in the response.")

        if not isinstance(response_json["parameters"], dict):
            raise ValueError("Invalid parameter type.")

        # Optionally, validate parameters against the chosen function's expected schema here
        # ...

        return response_json

    def _validate(self, task, llm_response, context=None):
        validation_schema = {
            "answer": "yes"  # Default to assume relevance
        }

        prompt = dedent(f"""
            Context: {context if context else "None"}
            Task: {task}
            LLM Response: {llm_response}

            Was the LLM response relevant and appropriate for the task?

            Answer using this schema:
            {json.dumps(validation_schema, indent=2)}

            Only provide "yes" or "no" as the answer.
        """)

        if self.verbose:
            print("Validation Prompt:", prompt)

        response = self.agent.invoke(prompt)

        try:
            validation_result = json.loads(response)["answer"].lower()  # Convert to lowercase
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid validation response: {e}")

        if validation_result not in ["yes", "no"]:
            raise ValueError("Invalid validation answer. Must be 'yes' or 'no'.")

        if self.verbose:
            print("Validation Result:", validation_result)

        return validation_result == "yes"  # True if relevant, False otherwise
