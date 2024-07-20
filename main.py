from Agent import Agent


functions = [
    {
        "name": "check_ram_size",
        "description": "Returns the ram size",
        "parameters": {},
    },

    {
        "name": "goto_dir",
        "description": "Given the full path to the directory, it will change the dir to the path.",
        "parameters": {
            "path": "string"
        },
    },

]

agent = Agent(available_functions=functions, verbose=True)
task = "Update my server"
context = """
"""
print(agent.execute(task, context))