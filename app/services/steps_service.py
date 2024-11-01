from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_ollama import ChatOllama
from utils.numbered_list_output_parser import NumberedListOutputParser


class StepsService:
    def __init__(self):
        model = ChatOllama(model="llama3.2", device="mps")
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert in community problem-solving and project planning.",
                ),
                (
                    "human",
                    """Given the following information about a community issue:

**Image Caption**: {caption}

**User Description**: {description}

**Chosen Solution**: {solution}

Based on the information provided, please outline a detailed step-by-step action plan to implement the chosen solution.

The action plan should:

- Be practical and actionable.
- There should be 3-7 steps in the plan.
- Include all necessary steps from start to finish.
- Identify any required resources, contacts, or permissions.
- Consider potential challenges and how to address them.
- Contain no new lines within each step.

**Please list the action steps as follows:**

1. Step one description

2. Step two description

3. Step three description

...

Ensure that each step starts with the step number followed by a period and a space, and that the descriptions are on the same line.

""",
                ),
            ]
        )
        self.chain = (
            prompt_template | model | StrOutputParser() | NumberedListOutputParser()
        )

    def generate_solution(
        self,
        caption: str,
        description: str,
        solution: str,
    ) -> List[str]:
        return self.chain.invoke(
            {
                "caption": caption,
                "description": description,
                "solution": solution,
            }
        )


if __name__ == "__main__":
    solution_service = StepsService()
    caption = "There are garbage bags on the street."
    description = "The garbage bags are piling up on the street, causing a bad smell and attracting pests."
    solution = "Work with the local waste management department to schedule regular trash pickups for the street, especially during periods when there is an accumulation of garbage. This would ensure that the bags are emptied regularly and prevent further accumulation."
    print(solution_service.generate_solution(caption, description, solution))
