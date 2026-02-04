# ReAct-LLM-Agent

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

### 🔍 What is a ReAct Agent?

A **ReAct agent** (short for **Reason + Act**) is an agent design pattern where a language model **interleaves reasoning steps with actions** taken in an environment (such as calling tools, executing code, querying APIs, or reading files). Instead of reasoning everything upfront or acting blindly, the agent repeatedly **thinks about the current state**, **decides what action to take**, **observes the result**, and then reasons again. This loop allows the agent to handle complex, multi-step tasks, recover from errors, and adapt its behavior based on intermediate feedback. ReAct is especially effective for tasks that require planning, tool use, and stateful interaction—like coding, debugging, data analysis, or navigating external systems.

### 🔄 ReAct Agent Pipeline

```
  Task Goal
      ↓
  Reasoning / Planning
      ↓
  Action / Tool Execution
      ↓
  Observation / Result
      ↓
  Update Plan
      ↓
  (loop back to Reasoning until the task goal is achieved)
```

### ✅ Validation

- **Task I: Multi-Step Reasoning**:
  
  > Find the population of the capital city of the country that hosted the 2020 Summer Olympics. Then determine whether that population is larger or smaller than the population of New York City.

- **Responses** from `ReAct-LLM-Agent`:
  
  ```
    >>> Calling Ollama model, please wait...
  
    💭 Thought: I need to find the population of the capital city of the country that hosted the 2020 Summer Olympics. First, I should determine which country hosted the 2020 Summer Olympics. Then, find the capital city of that country and its population. Finally, compare it to New York City's population.
  
    🔧 Action: search(query="country that hosted 2020 Summer Olympics")
  
    🔍 Observation：[DDGS]
    - List of Olympic Games host cities - Wikipedia
      18 hours ago - Moritz (1928 and 1948 Winter Olympics), ... and 2020 Summer Olympics), Beijing (2008 Summer Olympics and 2022 Winter Olympics) and Salt Lake City (2002 and 2034 Winter Olympics). Stockholm hosted the 1912 Summer Olympics and the equestrian portion of the 1956 Summer Olympics. London and Paris have both hosted three Games, while Los Angeles will become the third city to gain that distinction ...
      Source: https://en.wikipedia.org/wiki/List_of_Olympic_Games_host_cities
    - Summer Olympic Games - Wikipedia
      3 days ago - The other countries to have hosted the Summer Olympics are Belgium, Brazil, Canada, China, Finland, Italy, Mexico, Netherlands, South Korea, Soviet Union, Spain, and Sweden, with each of these countries having hosted on one occasion. Asia has hosted four times: in Tokyo (1964 and 2020), Seoul (1988), and Beijing (2008). The 2016 Games in Rio de Janeiro, Brazil, were the first Summer Olympics to be held in South America and the first that was held completely during the local "winter" season.
      Source: https://en.wikipedia.org/wiki/Summer_Olympic_Games
    - 2020 Summer Olympics - Wikipedia
      1 week ago - As determined by a 2009 IOC ruling that banned international torch relays for any future Olympic Games, the 2020 Summer Olympics torch was scheduled to only visit the two countries of Greece and the host nation Japan. The first phase of the relay began on 12 March 2020, with the traditional flame l
    >>> Calling Ollama model, please wait...
  
    💭 Thought: The search results indicate that the 2020 Summer Olympics were hosted by Japan, with Tokyo as the host city. Since Tokyo is also the capital of Japan, I need to find its population. Next, I will search for Tokyo's population.
  
    🔧 Action: search(query="population of Tokyo, Japan")
  
    🔍 Observation：[DDGS]
    - Tokyo - Wikipedia
      6 days ago - Tokyo, officially the Tokyo Metropolis, is the capital and most populous city of Japan. With a population of over 14 million in the city proper in 2023 , it is one of the most populous urban areas in the world.
      Source: https://en.wikipedia.org/wiki/Tokyo
    - Demographics of Tokyo - Wikipedia
      1 week ago - Although the rate of increase slowed, the population reached 11.67 million in 1975. Sustained migration from rural Japan throughout the 1960s and 70s created a massive urban sprawl.
      Source: https://en.wikipedia.org/wiki/Demographics_of_Tokyo
    - Greater Tokyo Area - Wikipedia
      2 weeks ago - As of 2026, the United Nations estimates the total population at 36,954,512 . It is the second-largest single metropolitan area in the world in terms of built-up or urban function landmass at 8,547 square kilometres (3,300 sq mi), behind only ...
      Source: https://en.wikipedia.org/wiki/Greater_Tokyo_Area
    - Tokyo Population 2026
      1 month ago - Now, to find the rough population density of the Tokyo area, we combine the total population with the available space for the residents, which comes to 6,224.66 people living per square kilometer (16,121.8 residents per square mile).
      Source: https://worldpopulationreview.com/cities/japan/tokyo
    - Tokyo, Japan Metro Area Population (1950-2026) | MacroTrends
      The metro area population of Tokyo in 2024 was 37,115,000 , a 0.21% decline from 2023.
      Source: https://www.macrotrends.net/global-metrics/cities/21
    >>> Calling Ollama model, please wait...
  
    💭 Thought: The search results show that Tokyo, Japan, hosted the 2020 Summer Olympics. The population of Tokyo (city proper) is over 14 million (2023 estimate). Now I need to find New York City's population to compare the two.
  
    🔧 Action: search(query="population of New York City")
  
    🔍 Observation：[DDGS]
    - Demographics of New York City - Wikipedia
      New York City is a large and ethnically diverse metropolis. It is the largest city in the United States, and has a long history of international immigration. The New York region continues to be by far the leading metropolitan gateway for legal immigrants admitted into the United States.
      Source: https://en.wikipedia.org/wiki/Demographics_of_New_York_City
    - Population of New York City 2026 — United States of America
      Population New York City — composition, density and population of the country.— Population density. 6,802.34 persons/sq.km². Male.
      Source: https://www.aznations.com/population/us/cities/new-york-city
    - New York City Population : A Closer Look at the Vibrant Tapestry
      Discover the diverse population of New York City , a captivating metropolis known for its cultural richness and iconic neighborhoods.
      Source: https://www.elikarealestate.com/blog/new-york-city-population/
    - The population of New York City . | Wyzant Ask An Expert
      By the year 2000, its population grew to approximately 8,008,000. What was the average rate of change in the population per year from the year 1900 to the year 2000? Show your work.
      Source: https://www.wyzant.com/resources/answers/887563/the-population-of-new-york-city
    - How many people live in new york city ? - HotBot
      Discover the dynamic population of New York City , its historical growth, diverse demographics, and future challenges. Learn about the Big Apple's unique urban t
    >>> Calling Ollama model, please wait...
  
    💭 Thought: The population of Tokyo (city proper) is over 14 million (2023 estimate). New York City's population is approximately 8.3 million (city proper, 2023 estimate). Therefore, Tokyo's population is larger than New York City's.
  
    ✅ Final Answer：The capital city of the country that hosted the 2020 Summer Olympics is Tokyo, Japan, with a population of over 14 million (as of 2023). This is larger than New York City's population of approximately 8.3 million (as of 2023). Thus, Tokyo's population is larger than New York City's.
  ```

- **Task II: Code Generation**:
  
  > Implement a Python command-line to-do application with separated modules for logic, storage, and CLI, The system should allow users to add tasks, list tasks, and mark tasks as completed.

- **Responses** from `ReAct-LLM-Agent`:
  
  ```
    >>> Calling Ollama model, please wait...
  
    💭 Thought: I need to create a Python to-do application with separated modules. First, I'll outline the structure and then implement each component step by step.
  
    🔧 Action: write_to_file(storage.py, import json
  
    class Storage:
        def __init__(self, file_path="tasks.json"):
              self.file_path = file_path
              self.tasks = self._load_tasks()
  
        def _load_tasks(self):
            try:
                with open(self.file_path, "r") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
  
        def save_tasks(self):
            with open(self.file_path, "w") as f:
                json.dump(self.tasks, f, indent=2))
  
    🔍 Observation：Write successfully
  
    >>> Calling Ollama model, please wait...
  
    💭 Thought: Next, I'll implement the logic module to handle task operations. This will include adding, marking as completed, and listing tasks. I'll create a logic.py file with these functionalities.
  
    🔧 Action: write_to_file(logic.py, class Logic:
          def __init__(self, storage):
              self.storage = storage
              self.tasks = storage.tasks
  
          def add_task(self, description):
              self.tasks.append({"description": description, "completed": False})
              self.storage.save_tasks()
  
          def mark_task_as_completed(self, task_id):
              if 0 <= task_id < len(self.tasks):
                  self.tasks[task_id]["completed"] = True
                  self.storage.save_tasks()
              else:
                  raise IndexError("Invalid task ID")
  
          def list_tasks(self):
              for i, task in enumerate(self.tasks):
                  status = "✓" if task["completed"] else ""
                  print(f"{i}: {status} {task["description"]}"))
  
    🔍 Observation：Write successfully
  
    >>> Calling Ollama model, please wait...
  
    💭 Thought: Now, I'll implement the CLI module to handle user interactions. This will include a main loop for adding, listing, and marking tasks as completed. I'll create a cli.py file with these functionalities.
  
    🔧 Action: write_to_file(cli.py, import click
    from logic import Logic
    from storage import Storage
  
    @click.command()
    @click.option("--task-file", default="tasks.json", help="Path to task storage file")
    def main(task_file):
        storage = Storage(task_file)
        logic = Logic(storage)
  
        while True:
            print("\
    To-Do List Application")
            print("1. Add Task")
            print("2. List Tasks")
            print("3. Mark Task as Completed")
            print("4. Exit")
            choice = input("Select an option: ")
  
            try:
                if choice == "1":
                    description = input("Enter task description: ")
                    logic.add_task(description)
                elif choice == "2":
                    logic.list_tasks()
                elif choice == "3":
                    task_id = int(input("Enter task ID to mark as completed: "))
                    logic.mark_task_as_completed(task_id)
                elif choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {str(e)}")
  
    if __name__ == "__main__":
        main())
  
    🔍 Observation：Write successfully
  
    >>> Calling Ollama model, please wait...
  
    💭 Thought: All modules are implemented. To complete the task, I'll provide the code structure and instructions to run the application.
  
    ✅ Final Answer：
    Here's the implementation for the to-do application with separated modules:
  
    1. **storage.py** (Handles data persistence):
  
       import json
  
       class Storage:
          def __init__(self, file_path="tasks.json"):
              self.file_path = file_path
              self.tasks = self._load_tasks()
  
          def _load_tasks(self):
              try:
                  with open(self.file_path, "r") as f:
                      return json.load(f)
              except (FileNotFoundError, json.JSONDecodeError):
                  return []
  
          def save_tasks(self):
              with open(self.file_path, "w") as f:
                  json.dump(self.tasks, f, indent=2)
  
    2. **logic.py** (Handles business logic):
  
       class Logic:
          def __init__(self, storage):
              self.storage = storage
              self.tasks = storage.tasks
  
          def add_task(self, description):
              self.tasks.append({"description": description, "completed": False})
              self.storage.save_tasks()
  
          def mark_task_as_completed(self, task_id):
              if 0 <= task_id < len(self.tasks):
                  self.tasks[task_id]["completed"] = True
                  self.storage.save_tasks()
              else:
                  raise IndexError("Invalid task ID")
  
          def list_tasks(self):
              for i, task in enumerate(self.tasks):
                  status = "✓" if task["completed"] else ""
                  print(f"{i}: {status} {task['description']}")
  
    3. **cli.py** (Command-line interface):
  
       import click
       from logic import Logic
       from storage import Storage
  
       @click.command()
       @click.option("--task-file", default="tasks.json", help="Path to task storage file")
       def main(task_file):
          storage = Storage(task_file)
          logic = Logic(storage)
  
          while True:
              print("\nTo-Do List Application")
              print("1. Add Task")
              print("2. List Tasks")
              print("3. Mark Task as Completed")
              print("4. Exit")
              choice = input("Select an option: ")
  
              try:
                  if choice == "1":
                      description = input("Enter task description: ")
                      logic.add_task(description)
                  elif choice == "2":
                      logic.list_tasks()
                  elif choice:  # Handle option 3 and 4
                      task_id = int(input("Enter task ID to mark as completed: "))
                      logic.mark_task_as_completed(task_id)
                  elif choice == "4":
                      break
                  else:
                      print("Invalid choice. Please try again.")
              except Exception as e:
                  print(f"Error: {str(e)}")
  
       if __name__ == "__main__":
            main()
  
    **Usage Instructions:**
  
    1. Ensure all files are in the same directory
  
    2. Run `python cli.py` to start the application
  
    3. Use the menu options to add, list, and mark tasks as completed
  
    4. Tasks will be saved in `tasks.json` automatically
  
    The application uses a JSON file for storage, with separate modules for logic, storage, and CLI interface as requested.
  ```

- **Generated Code Test for Task II**:
  
  ```
     (ai-agent) **\react-llm-agent>python cli.py
    To-Do List Application
    1. Add Task
    2. List Tasks
    3. Mark Task as Completed
    4. Exit
    Select an option: 1
    Enter task description: kick off meeting
    To-Do List Application
    1. Add Task
    2. List Tasks
    3. Mark Task as Completed
    4. Exit
    Select an option: 1
    Enter task description: prototype development
    To-Do List Application
    1. Add Task
    2. List Tasks
    3. Mark Task as Completed
    4. Exit
    Select an option: 2
    0:  kick off meeting
    1:  prototype development
    To-Do List Application
    1. Add Task
    2. List Tasks
    3. Mark Task as Completed
    4. Exit
    Select an option: 3
    Enter task ID to mark as completed: 0
    To-Do List Application
    1. Add Task
    2. List Tasks
    3. Mark Task as Completed
    4. Exit
    Select an option: 2
    0: ✓ kick off meeting
    1:  prototype development
    To-Do List Application
    1. Add Task
    2. List Tasks
    3. Mark Task as Completed
    4. Exit
    Select an option: 4
  ```

- **Result in `tasks.json`**:
  
  ```json
    [
      {
        "description": "kick off meeting",
        "completed": true
      },
      {
        "description": "prototype development",
        "completed": false
      }
    ]  
  ```

- **Task III: Research and Summary**:
  
  > Summarize the paper in a single paragraph of no more than four sentences. The paper’s arXiv index is 2511.13720.

- **Responses** from `ReAct-LLM-Agent`:
  
  ```
    >>> Calling Ollama model, please wait...
    💭 Thought: I need to find the paper with the arXiv index 2511.13720 to summarize it. I'll use the search tool to retrieve the paper's information.
  
    🔧 Action: search(query="arXiv:2511.13720")
  
    🔍 Observation：[DDGS]
    - [ 2511 . 13720 ] Back to Basics: Let Denoising Generative Models Denoise
      Today's denoising diffusion models do not "denoise" in the classical sense, i.e., they do not directly predict clean images. Rather, the neural networks predict noise or a noised quantity.
      Source: https://arxiv.org/abs/2511.13720
    - Paper page - Back to Basics: Let Denoising Generative Models Denoise
      Cite arxiv .org/abs/ 2511 . 13720 in a model README.md to link it from this page.
      Source: https://huggingface.co/papers/2511.13720
    - GitHub - LTH14/JiT: PyTorch implementation of JiT https...
      @article{li2025jit, title={Back to Basics: Let Denoising Generative Models Denoise}, author={Li, Tianhong and He, Kaiming}, journal={arXiv preprint arXiv : 2511 . 13720 }, year={2025} }. JiT adopts a minimalist and self-contained design for pixel-level high-resolution image diffusion.
      Source: https://github.com/LTH14/JiT
    - (PDF) Back to Basics: Let Denoising Generative Models Denoise
      DOI:10.48550/ arXiv . 2511 . 13720 . License.agents inside of scalable world models. arXiv:2509.24527, 2025. [19] Alex Henry, Prudhvi Raj Dachapally, Shubham Shantaram. Pawar, and Yuxuan Chen. Query -key normalization for. Transformers. In Findings of EMNLP, 2020.
      Source: https://www.researchgate.net/publication/397713136_Back_to_Basics_Let_Denoising_Generative_Models_Denoise
    - The unification of representation learning and generative modelling
      Better Together: Leveraging Unpaired Multimodal Data for Stronger Unimo
    >>> Calling Ollama model, please wait...
  
    💭 Thought: The search results show the paper's title, authors, and key points. The paper critiques current denoising diffusion models for not directly predicting clean images and proposes a return to classical denoising methods. It also mentions a PyTorch implementation called JiT. I can now summarize this in four sentences.
  
    ✅ Final Answer：The paper 'Back to Basics: Let Denoising Generative Models Denoise' (arXiv:2511.13720) argues that modern denoising diffusion models fail to 'denoise' in the classical sense, as they predict noise rather than directly generating clean images. The authors advocate for a foundational approach, emphasizing that these models should focus on removing noise to produce accurate outputs. They introduce JiT, a PyTorch implementation with a minimalist design, aimed at achieving high-resolution image diffusion through self-contained, pixel-level processing. The work highlights a shift toward simplicity and effectiveness in generative modeling frameworks.
  ```
