import os
import click
import inspect
import platform
import ollama
from string import Template
from typing import List, Callable, Tuple
from prompt_template import react_system_prompt_template


class ReActAgent():
    def __init__(self, tools: List[Callable], model: str, project_directory: str):
        self.tools = {func.__name__: func for func in tools}
        self.model = model
        self.project_directory = project_directory

    def run(self, user_input: str):
        pass

    def parse_action(self, code_str: str) -> Tuple[str, List[str]]:
        pass

    def parse_single_arg(self, arg_str: str):
        pass

    def call_model(self, messages):
        print(">>> Calling Ollama model, please wait ...")
        response = ollama.chat(model=self.model, messages=messages, options={"temperature": 0.2})
        content = response["message"]["content"]
        messages.append({"role": "assistant", "content": content})
        return content

    def render_system_prompt(self, system_prompt_template: str) -> str:
        tool_list = self.get_tool_list()
        file_list = ", ".join(
            os.path.abspath(os.path.join(self.project_directory, file))
            for file in os.listdir(self.project_directory)
        )
        return Template(system_prompt_template).substitute(
            tool_list = tool_list,
            file_list = file_list,
            operating_system = self.get_operating_system()
        )

    def get_tool_list(self) -> str:
        tool_descriptions = []
        for func in self.tools.values():
            name = func.__name__
            signature = str(inspect.signature(func))
            doc = inspect.getdoc(func)
            tool_descriptions.append(f"- {name}{signature}: {doc}")
        return "\n".join(tool_descriptions)
    
    def get_operating_system(self):
        return {
            "Darwin": "macOS",
            "Windows": "Windows",
            "Linux": "Linux",
        }.get(platform.system(), "Unknown")

# tool functions
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
def write_to_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.replace("\\n", "\n"))
    return "Write successfully"

def run_terminal_command(command):
    import subprocess
    run_result = subprocess.run(
        command,                # the command string to run
        shell=True,             # run the command through the shell
        capture_output=True,    # capture stdout and stderr
        text=True               # return stdout/stderr as strings instead of bytes
    )
    return "Run successfully" if run_result.returncode == 0 else run_result.stderr

# create command-line interfaces
@click.command()
@click.argument('project_directory',
                type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(project_directory):
    project_dir = os.path.abspath(project_directory)
    tools = [read_file, write_to_file, run_terminal_command]
    agent = ReActAgent(
        tools=tools,
        model="codellama13b",
        project_directory=project_dir
    )
    task = input(">>> Please input your task: ")
    final_answer = agent.run(task)
    print(f">>> Final Answer: {final_answer}")

if __name__ == "__main__":
    main()