# Building a "Living" Data System: The Agentic Pipeline

A traditional data pipeline (ETL: Extract, Transform, Load) is like an assembly line: predictable, linear, and honestly, a bit boring. It does exactly what you tell it to do and nothing more.

To stand out in front of a university-level jury, we're going to flip this concept. Rather than writing a script that passively processes data, **you are going to build an AI Research Lab**. We will use a **Multi-Agent System** where each agent is an AI with a specific personality, role, and set of tools. They will talk to each other, argue about data quality, and generate insights autonomously.

This approach — "code-vibing" meets rigorous statistics — elevates your project from a standard high school notebook to a bleeding-edge prototype. 

---

## 1. The Cast of Characters: Redefining the Pipeline

Instead of boring pipeline stages, we will configure four distinct AI agents. They will share a global state (your `pandas` DataFrames), but they will execute their specific goals iteratively.

*   **🕵️ The Scout (El Explorador):** Connects to the OECD/Eurostat/INE APIs. Its job is to hunt for the right datasets. It doesn't just download; it asks, *“Is this data fresh? Is this the right table?”*
*   **🧹 The Cleaner (El Purista):** A heavily customized Pandas agent. It hates messy data. It will clean nulls, standardize columns, and generate a "Data Quality Report" critiquing the source.
*   **⚖️ The Skeptic (El Crítico):** **[The WOW Factor]** This agent acts as a university professor. You feed it your cleaned data and your the logic of your *Index IBTG*, and its prompt is literally: *"Find the statistical bias in this data. Are there confounding variables? Does correlation equal causation?"*
*   **🗣️ The Storyteller (El Narrador):** Takes the mathematical outputs and translates them into punchy, compelling natural language suited for your frontend dashboard or your final conclusions.

> [!NOTE] 
> **Why it matters (Scientific Strategy):** Juries see hundreds of static charts. Showing a system that *thinks* about the data proves you understand the scientific method: observation, hypothesis, testing, and critical review.

---

## 2. Architecture & Tech Stack

We will use **Python**, **Pandas**, and a lightweight agent framework like **LangChain** (specifically with `LangGraph` for agent communication, or just simple sequential chains). You can run this directly in Google Colab (as mentioned in your Annex A).

### The Technology:
*   `pandas` & `requests`: For the raw statistical manipulation and API calls.
*   `langchain` & `langchain-experimental`: For LLM orchestration and the Pandas Agent.
*   **LLM API:** Google Gemini (or OpenAI) to power the "brains" of the agents.

---

## 3. Step-by-Step Implementation Guide

### Step 1: Initialize the Environment & the LLM Setup

First, we set the stage. We need to instantiate our core LLM that will give our agents their thinking capabilities.

```python
# pip install langchain langchain-google-genai langchain-experimental pandas requests

import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Initialize the "brain"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)
llm_creative = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7) # For The Skeptic & Storyteller
```

### Step 2: Build "The Scout" (Dynamic Extraction)

Instead of hardcoding a CSV download, The Scout uses a Python function to ping the Eurostat or INE API and reports back what it found.

```python
def fetch_eurostat_data(dataset_code):
    # Logic to fetch from Eurostat API via JSONstat
    print(f"🕵️ The Scout: 'I went to Eurostat looking for {dataset_code}.'")
    print("🕵️ The Scout: 'The response looks solid, but I see missing years. Passing to The Cleaner.'")
    # For this example, let's assume we load a dataframe
    return pd.DataFrame({"Country": ["ES", "FR", "DE"], "Women_in_Tech": [18, 20, 22], "Year": [2021, None, 2021]})

raw_df = fetch_eurostat_data("isoc_sks_itsps")
```

> [!TIP]
> **Pro Tip:** Give The Scout the ability to search metadata. If an API call fails, ask the LLM agent to suggest a different dataset code. This creates a self-healing pipeline!

### Step 3: Build "The Cleaner" (Data Wrangling with Attitude)

We leverage LangChain's DataFrame Agent. We give it a strict persona.

```python
cleaner_prompt = """
You are 'The Cleaner', a strict data engineer. You are looking at a pandas dataframe about the gender gap in tech.
Your tasks:
1. Identify any missing data or nulls.
2. Fix them by doing forward fills or dropping useless rows.
3. Return the Python code you used AND a harsh critique of the dataset's quality.
"""

cleaner_agent = create_pandas_dataframe_agent(
    llm, 
    raw_df, 
    verbose=True, 
    prefix=cleaner_prompt,
    allow_dangerous_code=True # Since we are in Colab, we allow Pandas execution
)

cleaner_response = cleaner_agent.invoke("Clean the loaded data and tell me what was wrong with it.")
print("🧹 The Cleaner says:", cleaner_response['output'])
# Example Output: "The dataset was sloppy. France had a missing year, so I removed it. The clean dataframe is ready."
```

### Step 4: The Innovation — "The Skeptic"

This is the **WOW Idea**. Traditional pipelines stop when the data is clean. Ours starts fighting itself. Let's pass the mathematical logic of your **Index IBTG** to the Skeptic.

```python
skeptic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the 'The Skeptic'. You are a ruthless, brilliant university statistics professor. Your job is to find methodological flaws in the user's data approach."),
    ("user", """
    Here is a summary of the data I have collected to build the Index IBTG (measuring tech creation and tech exclusion for older women):
    Columns: {columns}
    My hypothesis: The same communities that exclude older women digitally also show fewer women creating technology.
    
    Tear this apart. 
    1. What confounding variables (like income, rurality) am I missing?
    2. Are there any hidden biases in how this is measured?
    3. Generate one unexpected new research question based on this that I haven't thought of.
    """)
])

skeptic_chain = skeptic_prompt | llm_creative
skeptic_critique = skeptic_chain.invoke({"columns": str(list(raw_df.columns))})

print("⚖️ The Skeptic critique:\n", skeptic_critique.content)
```

> [!IMPORTANT]
> **WOW Idea Implementation:** Put the output of *The Skeptic* directly into your project document in a section called `"AI Limitations Analysis"`. The jury will be blown away. You don't hide your flaws; you built an AI to spot them for you, and then you discuss them in your "Limitacions" (Section 8 of your outline).

### Step 5: The Feedback Loop (Making it Alive)

A living system has loops. If *The Skeptic* decides the data is fundamentally flawed (e.g., "You can't prove this without data on the average age per Autonomous Community"), it can programmatically trigger *The Scout* to go fetch a new dataset from the INE (e.g., `Población por edades y CCAA`).

```python
# Pseudo-code for the loop:
if "rurality" in skeptic_critique.content.lower():
    print("🔄 Feedback Loop Triggered!")
    new_data = fetch_eurostat_data("rural_population_stats")
    # Feed this new data back to The Cleaner...
```

### Step 6: "The Storyteller"

Finally, we translate tables into impact.

```python
storyteller_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are 'The Storyteller'. Write a 2-sentence journalistic hook based on the data."),
    ("user", "Data shows: Women in tech is 18%. Digital gap for over 65 women is 40%.")
])

hook = (storyteller_prompt | llm_creative).invoke({}).content
print("🗣️ The Storyteller:\n", hook)
```

---

## 4. How to Pitch This to the Jury

When defending your project, do not say: *"I downloaded CSVs and put them in Python."*

Say this: *"Traditional statistics uses static pipelines. Because the gender gap in technology is a dynamic and deeply biased issue, I built an active agentic AI pipeline. I deployed specialized AI agents to fetch the data, critique my methodology for bias, and iteratively improve the Index IBTG. It’s an exploratory system that treats data as a conversation, not just a spreadsheet."*

By structuring your methodology this way, you merge sociological analysis with advanced software architectural paradigms, placing your work firmly at an undergraduate/research lab level.
