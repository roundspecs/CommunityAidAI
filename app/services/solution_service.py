import json
from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_ollama import ChatOllama

from utils import NumberedListOutputParser


class SolutionService:
    def __init__(self):
        model = ChatOllama(model="llama3.2", device="mps")
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert in community problem-solving."),
                (
                    "human",
                    """You are an expert in community problem-solving.

Given the following information about a community issue:

**Image Caption**: {caption}

**User Description**: {description}

Based on the information provided, please suggest **three practical and actionable solutions** to address the issue.

Each solution should be:


- Be concise (1-2 sentences).
- Contain no new lines within each solution.
- Be feasible for community members or local authorities to implement.
- Aim at effectively improving the situation.

**Please list the solutions as follows:**

1. Solution one description

2. Solution two description

3. Solution three description

Ensure that each solution starts with the solution number followed by a period and a space, and that the descriptions are on the same line."""
                ),
            ]
        )
        self.chain = prompt_template | model | StrOutputParser() | NumberedListOutputParser()

    def generate_solution(self, caption: str, description: str) -> List[str]:
        return self.chain.invoke(
            {
                "caption": caption,
                "description": description,
            }
        )


if __name__ == "__main__":
    solution_service = SolutionService()
    caption = "There are garbage bags on the street."
    description = "The garbage bags are piling up on the street, causing a bad smell and attracting pests."
    print(solution_service.generate_solution(caption, description))
