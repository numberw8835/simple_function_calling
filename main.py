from Agent import Agent


functions = [
    {
        "name": "check_ram_size",
        "description": "Returns the ram size",
        "parameters": {},
    },

    {
        "name": "change_dir",
        "description": "changes the dir to the given path, WORKS ONLY ON LOCAL filesystem.",
        "parameters": {
            "path": "string"
        },
    },

    {
        "name": "check_disk_size",
        "description": "Returns the disk size",
        "parameters": {},
    },

]

agent = Agent(available_functions=functions, verbose=True)
task = "start the server on the ip 192.168.1.10"
context = """
"""
print(agent.execute(task, context))