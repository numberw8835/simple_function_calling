import readline
import subprocess
from halo import Halo
from Agent import Agent
from functions import functions
import utils  # Import the utils module


class Console:
    def __init__(self, pwd=None):
        self.history = []
        self.username = self._get_username()
        self.machine_name = self._get_machine_name()

    def start_interactive_loop(self):
        """Starts an interactive loop for the console."""
        readline.parse_and_bind("tab: complete")  # Enable tab completion (basic)
        while True:
            prompt = f"<{self.username.upper()}@{self.machine_name.upper()}> "  # Customized prompt
            user_input = input(prompt)
            if user_input.lower() in ["exit", "quit", "stop", "q"]:
                break

            self.execute(user_input)
            self.history.append(user_input)  # Store command in history

    def _get_username(self):
        """Retrieves the current username."""
        return subprocess.run(['whoami'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    
    def show_history(self):
        """Prints the command history."""
        if not self.history:
            print("No commands in history.")
        else:
            for i, cmd in enumerate(self.history):
                print(f"{i+1}. {cmd}")

    def _get_machine_name(self):
        """Retrieves the machine name."""
        return subprocess.run(['uname', '-n'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    def execute(self, user_input):
        agent = Agent(llm="mistral:7b-instruct-v0.3-q8_0", available_functions=functions)
        context = None  # Initialize context here for clarity

        for command, context in self._parse_input(user_input):
            if command == "show_history":
                self.show_history()
                return

            spinner = Halo(text='Processing...', spinner='dots')
            spinner.start()

            llm_response = agent.execute(command, context)

            if llm_response:
                function_name, parameters = llm_response["name"], llm_response["parameters"]
                try:
                    result = getattr(utils, function_name)(**parameters)
                    spinner.succeed(f"✅ Done! Result: {result}")
                except (AttributeError, TypeError) as e:
                    spinner.fail(f"❌ Error: {e}")
            else:
                spinner.fail("❌ I don't have enough information to do that. Please try another query.")

    def _parse_input(self, user_input):
        """Parse user input into (command, context) pairs, making context optional."""
        for tuple_str in user_input.split(';'):
            tuple_str = tuple_str.strip()

            parts = tuple_str.split(':', 1)  # Split at most once
            command = parts[0].strip()

            # Context is optional, set to None if not provided
            context = parts[1].strip() if len(parts) > 1 else None  
            yield command, context