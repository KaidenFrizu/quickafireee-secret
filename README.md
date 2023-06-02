# QuickAfireee - The Tournament Registration System for Quickfire LAN tourney

QuickAfireee is a flexible tournament registration system designed for use in the Quickfire ConQUEST 2023 Event, but is
also configurable for other osu! tournaments.

The system is designed primarily to work with Google sheets, but can also be configured to work with other data sources.

## Deploying

QuickAfireee was designed to use Google Service Accounts to access the sheets API. To deploy the system, you will need
to create a service account and download the credentials file. You can find the instructions on how to do this
[here](https://developers.google.com/identity/protocols/oauth2/service-account).

Once you have the credentials file, you will need to set the needed variables in `secrets.toml`, which a template exists
in the repo as `example.secrets.toml`. Set other configuration settings as you see fit.

When done, you will need to install pipenv:

```bash
    $ pip install pipenv
```

Then, install the dependencies:

```bash
    $ pipenv install
```

Finally, run the application:

```bash
    $ pipenv run streamlit run registration_app.py
```
Your application is accessible in `localhost:8501` but can be configured to run on other ports, consult the Streamlit
documentation for more information.
## Contributing

You will need Python 3.8 and above. Dependencies are installed using pipenv, but we highly recommend you to use a
virtual environment.

```bash
    $ pip install pipenv
    $ python -m venv .venv
    $ source .venv/bin/activate
```

If you're in Windows:

```powershell
    # This is applicable to Command Prompt too
    PS> pip install pipenv
    PS> python -m venv .venv
    PS> .venv\Scripts\activate
```
Then, install the dependencies:

```bash
    $ pipenv install
```

To run the applications, simply use `streamlit run` command.

```bash
    $ streamlit run registration_app.py
```
