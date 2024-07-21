from langchain_community.llms import Ollama
from textwrap import dedent
import json


class Agent:
    def __init__(self, llm="mistral", available_functions=None, verbose=False):
        self.verbose = verbose
        self.available_functions = available_functions or []  # Default to empty list
        self.validator = Ollama(
            model="llama3",
            # temperature=0.0,  # Set temperature based on desired determinism
            format='json',
        )
        self.chat_agent = Ollama(
            model=llm,
        )
        self.agent = Ollama(
            model=llm,
            # temperature=0.0,  # Set temperature based on desired determinism
            format='json',
        )

    def execute(self, task, context=None, check=False):
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

            It's very IMPORTANT that IF THERE IS NO APPLICABLE FUNCTIONS
            YOU MUST RETURN THIS:
            {json.dumps(null_schema, indent=2)}
            
            ONLY!!!!!!!!!
        """)

        if self.verbose:
            print("Prompt:", prompt)

        response = self.validator.invoke(prompt)

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
        validation_response = self._validate(task, response_json, context)

        if check:
            if validation_response:
                return response_json
            else:
                return None
        else:
            return response_json

    def _validate(self, task, llm_response, context=None):
        validation_schema = {
            "answer": "string",
        }

        prompt = dedent(f"""
            Context: {context if context else "None"}
            User's request: {task}
            Response: {llm_response}

            You are a FUNCTION VALIDATOR, ALL YOU MUST DO IS CHECK IF THE RESPONSE IS RELEVANT TO THE TASK OR NOT!!!!

            Answer using this schema:
            {json.dumps(validation_schema, indent=2)}

            ONLY provide "yes" or "no" as the answer.
        """)

        if self.verbose:
            print("Validation Prompt:\n", prompt)  # Print the prompt before invoking the model

        response = self.agent.invoke(prompt)

        try:
            validation_result = json.loads(response)
            answer = validation_result["answer"].lower()  # Convert to lowercase

            if answer not in ["yes", "no"]:
                raise ValueError("Invalid validation answer. Must be 'yes' or 'no'.")

            if self.verbose:
                print("Validation Result:", answer)

            return answer == "yes"

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from validation: {e}")

    def prompt(self, prompt):
        return self.chat_agent.invoke(prompt)