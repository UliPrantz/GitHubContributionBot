# GitHubContributionBot
## But why???
<img align="right" alt="Seems like the link is broken *imagine BUT WHY? GIF here" src="https://media.giphy.com/media/1M9fmo1WAFVK0/giphy.gif" width="190"/>

>This bot isn't actually meant to be used to make your git contributions look nice and green ;) It was a speed run coding to get back on track with some python syntax, get confident with python configuration and logging and trying out the new python3.9 typing system (or at least if VS Code Pylance gives some nice code completion - short answer: currently it isn't supported but at least now I know the return type of methods... even a couple months later). To challenge myself I also wanted to learn the GitHub Api v3 (which toke me the most time to be honest) but I still manged it to write and debug this code in about **1:30h**.



## Functionality
>This bot makes one or none automated commit every time it is run. Whether a commit is made will be determined by probability. This probability is calculated by the bot based on the config file.

## Configuration
>For the configuration copy the file `config-example.yaml` to `config.yaml` and past you personal config into it. And make sure to install the packages via:

```
pip3 install -r requirements.txt
```

- `git: Section`
  - `token:` this is the GitHub Api token which needs the Repo privileges
  - `repo-name:` this is the repo the bot makes commits to. Be aware that this repo needs a dir named **working_dir**!
- `contributions: Section` 
  - `runEvery:` this is the time interval in minutes the bot will be run by e.g a cron job
  - `contributionsPerDay:` this is the amount of contributions the bot should made in a day (be aware that it can be more or less since it's based on probability)