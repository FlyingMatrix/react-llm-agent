import os
import re
import ast
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
        messages = [
            {
                "role": "system",
                "content": self.render_system_prompt(react_system_prompt_template),
            },
            {
                "role": "user",
                "content": f"<question>{user_input}</question>",
            },
        ]

        while True:
            content = self.call_model(messages)

            # thought
            thought_match = re.search(
                r"<thought>(.*?)</thought>", 
                content, 
                re.DOTALL
            )
            if thought_match:
                print(f"\n\n Thought: {thought_match.group(1)}")

            # final answer
            if "<final_answer>" in content:
                final_answer = re.search(
                    r"<final_answer>(.*?)</final_answer>",
                    content,
                    re.DOTALL,
                )
                return final_answer.group(1)
            
            # action
            action_match = re.search(r"<action>(.*?)</action>", content, re.DOTALL)
            if not action_match:
                raise RuntimeError(">>> The model has not yet produced any <action> output...")
            action = action_match.group(1)
            tool_name, args = self.parse_action(code_str=action)
            print(f"\n\n Action: {tool_name}({', '.join(map(str, args))})") # -> "Action: tool_name(arg1, arg2, arg3)"     

            should_continue = input("\n\n >>> Do you want to continue?（y/n）") if tool_name == "run_terminal_command" else "y"
            if should_continue.lower() != "y":
                return ">>> The operation was canceled by the user!"
            
            # observation
            try:
                observation = self.tools[tool_name](*args) # relevant tool function is executed
            except Exception as e:
                observation = f">>> An error occurred while executing the tool function: {str(e)}"
            print(f"\n\n Observation：{observation}") # here the observation is the return value of the tool function execution

            messages.append(
                {
                    "role": "user",
                    "content": f"<observation>{observation}</observation>",
                }
            )

    def parse_action(self, code_str: str) -> Tuple[str, List[str]]:
        match = re.match(r"(\w+)\((.*)\)", code_str, re.DOTALL) # regular expression: (\w+) -> function name, \((.*)\) -> everything inside parentheses
        if not match:
            raise ValueError("Invalid function call syntax")
        func_name = match.group(1)
        args_str = match.group(2).strip()
        # initialize parsing state
        args = []               # args -> list to store parsed arguments
        current_arg = ""        # current_arg -> current argument
        in_string = False       # in_string -> if inside a string literal ('...' or "...")
        string_char = None      # string_char -> whether the string is single ' or double " quotes
        paren_depth = 0         # tracks nested parentheses to avoid splitting on commas inside nested calls
        # iterate over each character in args_str
        for i, char in enumerate(args_str):
            if not in_string: # handle logic when not inside a string
                if char in ["'", '"']:
                    in_string = True
                    string_char = char
                    current_arg += char
                elif char == "(":
                    paren_depth += 1
                elif char == ")":
                    paren_depth -= 1
                elif char == "," and paren_depth == 0: # if a comma at top level (paren_depth == 0) -> end of an argument
                    args.append(self._parse_single_arg(current_arg.strip()))
                    current_arg = ""
                    continue
            else: # handle logic when inside a string
                if char == string_char and args_str[i - 1] != "\\": 
                    in_string = False 
                    string_char = None
            current_arg += char
            # handle the last argument
            if current_arg.strip(): 
                args.append(self._parse_single_arg(current_arg.strip()))

            # return function name and argument list
            return func_name, args 
        """
            for example: 
                input:  code_str = "move_to(10, 'kitchen', turn_left(90))"
                ourput: (
                            "move_to",
                            ["10", "'kitchen'", "turn_left(90)"]
                        )
        """      

    def _parse_single_arg(self, arg_str: str): # safely convert arg_str into a Python literal value
        arg_str = arg_str.strip() 
        if ((arg_str.startswith('"') and arg_str.endswith('"'))
            or (arg_str.startswith("'") and arg_str.endswith("'"))
        ):
            return bytes(arg_str[1:-1], "utf-8").decode("unicode_escape")
        
        try:
            return ast.literal_eval(arg_str)
        except Exception:
            return arg_str

    def call_model(self, messages):
        print(">>> Calling Ollama model, please wait...")
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

