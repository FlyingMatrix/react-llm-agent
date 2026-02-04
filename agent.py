import os
import re
import ast
import click
import inspect
import platform
import ollama
import wikipedia
from ddgs import DDGS
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
            {"role": "system", "content": self.render_system_prompt(react_system_prompt_template)},
            {"role": "user", "content": f"<question>{user_input}</question>"}
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
                thought = thought_match.group(1)
                print(f"\n\n💭 Thought: {thought}")

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
            tool_name, args = self.parse_action(action)
            print(f"\n\n🔧 Action: {tool_name}({', '.join(args)})") # -> "Action: tool_name(arg1, arg2, arg3)"     

            should_continue = input("\n\n >>> Do you want to continue?（y/n）") if tool_name == "run_terminal_command" else "y"
            if should_continue.lower() != "y":
                print("\n\n>>> The operation was cancelled...")
                return "The operation was cancelled by the user!"
            
            # observation
            try:
                observation = self.tools[tool_name](*args) # relevant tool function is executed
            except Exception as e:
                observation = f">>> An error occurred while executing the tool function: {str(e)}"
            print(f"\n\n🔍 Observation：{observation}") # here the observation is the return value of the tool function execution

            obs_msg = f"<observation>{observation}</observation>"
            messages.append({"role": "user", "content": obs_msg})

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
        i = 0
        while i < len(args_str):
            char = args_str[i]
            if not in_string: # handle logic when not inside a string
                if char in ["'", '"']:
                    in_string = True
                    string_char = char
                    current_arg += char
                elif char == "(":
                    paren_depth += 1
                    current_arg += char
                elif char == ")":
                    paren_depth -= 1
                    current_arg += char
                elif char == "," and paren_depth == 0: # if a comma at top level (paren_depth == 0) -> end of an argument
                    args.append(self._parse_single_arg(current_arg.strip()))
                    current_arg = ""
                else:
                    current_arg += char
            else: # handle logic when inside a string
                current_arg += char
                if char == string_char and (i == 0 or args_str[i-1] != '\\'): 
                    in_string = False 
                    string_char = None
            i += 1

        # handle the last argument
        if current_arg.strip(): 
            args.append(self._parse_single_arg(current_arg.strip()))
        # return function name and argument list
        return func_name, args  

    def _parse_single_arg(self, arg_str: str): # safely convert arg_str into a Python literal value
        arg_str = arg_str.strip() 
        if((arg_str.startswith('"') and arg_str.endswith('"')) or (arg_str.startswith("'") and arg_str.endswith("'"))):
            inner_str = arg_str[1:-1]
            inner_str = inner_str.replace('\\"', '"').replace("\\'", "'")
            inner_str = inner_str.replace('\\n', '\n').replace('\\t', '\t')
            inner_str = inner_str.replace('\\r', '\r').replace('\\\\', '\\')
            return inner_str
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
        os_map = {
            "Darwin": "macOS",
            "Windows": "Windows",
            "Linux": "Linux"
        }
        return os_map.get(platform.system(), "Unknown")

# tool functions
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
def list_files(path="."):
    try:
        return os.listdir(path)
    except Exception as e:
        return f">>> Error listing directory: {e}"
    
def write_to_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.replace("\\n", "\n"))
    return "Write successfully"

def run_terminal_command(command):
    import subprocess
    run_result = subprocess.run(
        command,                    # the command string to run
        shell=True,                 # run the command through the shell
        capture_output=True,        # capture stdout and stderr
        text=True                   # return stdout/stderr as strings instead of bytes
    )
    return "Run successfully" if run_result.returncode == 0 else run_result.stderr

def search_on_wikipedia(query: str, max_chars: int = 1500) -> str:
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=6)
        return f"[Wikipedia]\n{summary}"[:max_chars]
    except Exception as e:
        return f"[Wikipedia]\nNo reliable result found. Error: {str(e)}"
    
def search_on_DDGS(query: str, max_chars: int = 1500) -> str:
    try:
        with DDGS() as ddgs:
            results = ddgs.text(
                query,
                max_results=5,
                safesearch="moderate"
            )

            snippets = []
            for r in results:
                title = r.get("title", "")
                body = r.get("body", "")
                href = r.get("href", "")
                snippets.append(f"- {title}\n  {body}\n  Source: {href}")

            text = "[DDGS]\n" + "\n".join(snippets)
            return text[:max_chars]

    except Exception as e:
        return f"[DDGS]\nNo reliable result found. Error: {str(e)}"
    
def search(query: str) -> str:
    # try Wikipedia first
    wiki_result = search_on_wikipedia(query)
    if "No reliable result" not in wiki_result:
        return wiki_result
    
    # fallback to DDGS
    return search_on_DDGS(query)

# create command-line interfaces
@click.command()
@click.argument('project_directory',
                type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(project_directory):
    project_dir = os.path.abspath(project_directory)
    tools = [read_file, list_files, write_to_file, run_terminal_command, search]
    agent = ReActAgent(tools=tools, model="qwen3:8b", project_directory=project_dir)
    task = input(">>> Please input your task: ")
    final_answer = agent.run(task)
    print(f"\n\n✅ Final Answer：{final_answer}")

if __name__ == "__main__":
    main()
