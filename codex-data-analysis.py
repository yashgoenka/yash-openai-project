"""Streamlit app to analyze data with English language commands."""

# Import from standard library
import os
import textwrap

# Import from 3rd party libraries
import streamlit as st
import openai

# Assign OpenAI API key from environment variable or streamlit secrets dict
openai.api_key = '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'

def openai_call(prompt: str, stop: str = None) -> str:
    """Call OpenAI Codex with text prompt.
    Args:
        prompt: text prompt
        stop: stop sequence to interrupt further token generation
    Return: predicted response text
    """
    kwargs = {
        "engine": "code-davinci-002",
        "prompt": prompt,
        "max_tokens": 64,
        "temperature": 0,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "best_of": 1
    }
    if stop:
        kwargs["stop"] = stop
    response = openai.Completion.create(**kwargs)
    print(response)
    return response["choices"][0]["text"]


####

# Page start

st.set_page_config(page_title="English to Code", page_icon="🤖")

st.title(
    "Natural Laguage Data Analysis"
)

st.write(
    """This app translates a statement in plain English into
    [SQL](https://en.wikipedia.org/wiki/SQL) or
    [Python](https://www.python.org) [Pandas](https://pandas.pydata.org)
    using OpenAI's Codex, allowing anyone
    not familiar with those languages/libraries to perform simple data
    analysis tasks with SQL databases or Pandas DataFrames."""
)

st.markdown("""---""")

selectbox = st.selectbox(
    "Select the type of translation you would like to perform",
    ("English to SQL", "English to Pandas")
)

if selectbox == "English to SQL":
    table_name_label = "Table name"
elif selectbox == "English to Pandas":
    table_name_label = "DataFrame name"

table_name = st.text_input(label=table_name_label, value="traffic")
column_names = st.text_area(
    label="Column names (comma-separated; optionally specify data types in parentheses)",
    value="url (string), event (string), country (string)",
)
statement = st.text_area(
    label="English text prompt/query statement",
    value="Count the number of pageview events by url for urls with at least 10 pageviews"
)

if statement:
    if selectbox == "English to SQL":
        prompt = textwrap.dedent(
            f'''
            """
            The database table "{table_name}" contains the following columns: {column_names}
            """
            # {statement}
            sql = """
            '''
        )
        stop = '"""'
        result_prefix = ""
        language = "sql"

    elif selectbox == "English to Pandas":
        prompt = textwrap.dedent(
            f'''
            """
            The Pandas DataFrame "{table_name}" contains the following columns: {column_names}
            """
            # {statement}
            {table_name}.'''
        )
        stop = "\n"
        result_prefix = table_name + "."
        language = "python"

    st.markdown("""---""")
    st.header("Result")
    st.code(result_prefix + openai_call(prompt, stop), language=language)

    st.markdown("""---""")
    st.header("Prompt sent to Codex")
    st.text(prompt)