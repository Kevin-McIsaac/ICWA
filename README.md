# IBRS
A simple chat bot for IBRS data

## Setting up

1. Install the following Microsoft VScode extentions
  * Jupyter - this enables you to run the notbooks directly in VScode rather than in Colab.
  * Python - this enable you to run python in VScode

2. Clone this repo to your local machine. The easy way is to use VScode clone command. 
   ```
   CTL-SHIFT-P  
      Git: Clone
      Clone from GitHub
      https://github.com/Kevin-McIsaac/IBRS.git
   ```

3. Check that python and pip are installed. In a terminal
   ```
   python --version
   pip --version
   ```
4. Consider consider using a [python virtual environment](https://code.visualstudio.com/docs/python/environments) rather than a global installation. You can use [VSCode](https://code.visualstudio.com/docs/python/environments) using
    ```
    CTRL-SHIFT P Venv
    CTRL-SHIFT P Python: Select Interpreter
    ```
   or do this manually
   ```
   python -m venv .venv
   ```

4. If you open the terminal using VScode this will automatically activated the the local virtual venv, other wise use 'source', then install the python modules listed in requirements.txt.
   ```
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a .env file with the necessary API information or upload the version I sent you.
   ```
    # IBRS Pinecone credentials
    INDEX='ibrs'
    PINECONE_API_KEY=''
    PINECONE_ENV=''

    #IBRS OPEN API credentials
    OPENAI_API_KEY= ''

    #IBRS WordPress credentials
    IBRS_API_BEARER = ''
    ```
## How to use
The Q&A bot is called gideon.py and written in python using streamlit. You can run this using
```
streamlit run gideon.py
```
This will print a URL to the local web page to access the running application.