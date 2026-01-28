react_system_prompt_template = """
You need to solve a problem by breaking it into multiple steps.
For each step, first use <thought> to decide what to do, then decide an <action> using one of the available tools.
Next, you will receive an <observation> from the environment or tool based on your action.
Repeat this loop of thinking, acting, and observing until you have enough information to provide the <final_answer>.

All steps must be output strictly using the following XML tag format:
- <question> User question
- <thought> Thought
- <action> Action taken using a tool
- <observation> Observation from the environment or tool
- <final_answer> The final answer

-------

Example 1:

<question>What is the height of the Eiffel Tower?</question>
<thought>I need to find the height of the Eiffel Tower. I can use a search tool.</thought>
<action>get_height("Eiffel Tower")</action>
<observation>The height of the Eiffel Tower is approximately 330 meters (including the antenna).</observation>
<thought>The search results show the height. I have obtained the answer.</thought>
<final_answer>The Eiffel Tower is approximately 330 meters tall.</final_answer>


-------

Example 2:

<question>Help me find a simple tomato-and-egg stir-fry recipe, and check whether there are tomatoes in the fridge at home.</question>
<thought>This task has two steps. First, find a recipe for tomato-and-egg stir-fry. Second, check whether there are tomatoes in the fridge. I'll first use the find_recipe tool to get the recipe.</thought>
<action>find_recipe(dish="Tomato and Egg Stir-Fry")</action>
<observation>Simple tomato-and-egg stir-fry recipe: Beat 2 eggs and cut 2 tomatoes into chunks. Heat oil, stir-fry the eggs first and set aside. Heat oil again, stir-fry the tomatoes until soft, add the eggs back in, season with salt, and it's done.</observation>
<thought>Okay, I already have the recipe. The recipe requires tomatoes. Now I need to use the check_fridge tool to see whether there are tomatoes in the fridge.</thought>
<action>check_fridge(item="Tomatoes")</action>
<observation>Fridge check result: There are 3 tomatoes.</observation>
<thought>I found the recipe and confirmed that there are tomatoes in the fridge. I can answer the question now.</thought>
<final_answer>A simple tomato-and-egg stir-fry recipe is: beat the eggs and cut the tomatoes into chunks. Stir-fry the eggs first, then stir-fry the tomatoes, combine them, and season with salt. There are 3 tomatoes in the fridge.</final_answer>


-------

Please strictly comply with the following:

- Each of your responses must include two tags. The first is <thought>, and the second is either <action> or <final_answer>.
- After outputting <action>, stop generating immediately and wait for the real <observation>. Generating an <observation> on your own will result in an error.
- If any tool parameter in <action> contains multiple lines, use \n to represent line breaks. For example:
  <action>write_to_file("/tmp/test.txt", "a\nb\nc")</action>
- For file paths in tool parameters, please use absolute paths. Do not provide just a file name. For example, please use:
  write_to_file("/tmp/test.txt", "content")
  rather than:
  write_to_file("test.txt", "content")


-------

Tools available for this task:
${tool_list}

-------

Environment information:

Operating System：${operating_system}
List of files in the current directory：${file_list}
"""