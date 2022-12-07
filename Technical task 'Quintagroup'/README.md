# Daily CLI reporter

`Quintagroup` technical task. 

The main task was to get all the reports from the `Clockify` API and then print them in appropriate way.

### Requirements

- Python 3

### Installiation

- Clone the project from the GitHub to your local PC:

```shell
git clone https://github.com/RomanSimachenko/Python.git
cd ./Python/Technical\ task\ \'Quintagroup\'
```

- Create virtual environment and intsall all project dependencies:

```shell
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r ./requirements.txt
```

- Also create a file with environment variables `setenv.sh`:

```shell
export API_KEY="CLOCKIFY_API_KEY"
```

Don't forget to activate it `source ./setenv.sh`

### Running

- (venv)$ `python3 ./main.py`
