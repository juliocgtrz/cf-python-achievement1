<h2>Install Python</h2>
<p>
  The first step is to install Python version 3.8.7 on your system. Check your Python version by using the command `python --version` from your terminal.
</p>

<h2>Set Up a Virtual Environment</h2>
<p>
  Set up a new virtual environment named “cf-python-base”.
</p>

<h2>Create a Python Script</h2>
<p>
  Install Visual Studio Code or another text editor of your choice and create a Python script named “add.py”. This script will take two numbers from user input, add them, and print the result. Here's the template for your Python script:
  <ul>
    <li>a = int(input("enter a number"))</li>
    <li>b = int(input("enter another number"))</li>
    <li>c = a + b</li>
    <li>print(c)</li>
  </ul>
</p>

<h2>Set up Ipython Shell</h2>
<p>
  Set up an ipython shell in the virtual environment "cf-python-base". An ipython shell is similar to the regular Python REPL with additional features like syntax highlighting, auto-indentation, and robust auto-complete features. Install it using pip.
</p>

<h2>Export a Requirements.txt File</h2>
<p>
  Generate a “requirements.txt” file from your source environment `pip freeze > requirements.txt`. Next, create a new environment called “cf-python-copy”. In this new environment, install packages from the “requirements.txt” file using `pip install -r requirements.txt`.
</p>
