from typing import final
import yaml
import logging
import random
from datetime import date, datetime
from github import Github, Repository
from github.GithubException import BadCredentialsException, UnknownObjectException

WORKING_DIR_PATH = "working_dir"
WORKING_FILE_NAME = "commit_history.yaml"
WORKING_FILE_PATH = WORKING_DIR_PATH+'/'+WORKING_FILE_NAME


def loadConfig() -> dict:
    '''
        Load the configuration file and add the config to a new
        `configDict` which is then returned.
        Also we have some error handling for the config file parsing.
    '''

    configDict = {}

    try:
        with open("config.yaml", "r") as configYaml:
            config = yaml.safe_load(configYaml)
    except FileNotFoundError:
        logging.error("The config file is missing! Copy 'config-example.yaml' to 'config.yaml'!")
        exit()

    try:
        configDict['token'] = config['git']['token']
        configDict['repoName'] = config['git']['repo-name']
        configDict['runEvery'] = config['contributions']['runEvery']
        configDict['contributionsPerDay'] = config['contributions']['contributionsPerDay']
    except KeyError:
        logging.error("The config file misses a key! Copy 'config-example.yaml' to 'config.yaml'!")
        exit()

    return configDict


def calcRunProbability(runEvery: int, contributionsPerDay: int) -> float:
    '''
        Calculates the probability which we need to make contributionsPerDay 
        when the program is run `runEvery` minute. This obviously is based on
        probability therefore we can have more a less contributions on a day.
    '''

    runsPerDay = 24 * 60 / runEvery
    contributionProbability = contributionsPerDay / runsPerDay
    return contributionProbability


def randomProbability(probability: float) -> bool:
    return random.random() < probability


def checkFileExistence(repo: Repository, filePath: str) -> bool:
    try:
        repo.get_contents(filePath)
        return True
    except:
        return False


def makeCommit(g: Github, repoName: str) -> None:
    '''
        The method which does all the work. We get the repo and find the
        working file (the file in which we commit). If the file is not there
        we create it. Than we parse file increment the contribution counter for 
        the current day and make a commit with the new file content.
    '''

    # get user of the token
    gitUser = g.get_user()
    # get the repo and make some error handeling
    try:
        repo = gitUser.get_repo(repoName)
    except BadCredentialsException:
        logging.error("The GitHub credentials seems to be wrong.")
        exit()
    except UnknownObjectException:
        logging.error(f"The specified repo-name: {repoName} isn't accessible/created")
        exit()

    # if the working file doesn't exists create it
    if (not checkFileExistence(repo, WORKING_FILE_PATH)):
        repo.create_file(WORKING_FILE_PATH, "Creating Working File", "")
        
    # get the yaml file, parse it and get some information about it
    yamlFile = repo.get_contents(WORKING_FILE_PATH)
    yamlFileSha = yamlFile.sha
    yamlFileContentStr = yamlFile.content
    yamlDict = yaml.safe_load(yamlFileContentStr)
    
    # short check if yaml dict was probably None (false format or something)
    if not yamlDict:
        yamlDict = {}

    # get todays string and increment the contribution counter
    todayStr = str(date.today())
    yamlDict.setdefault(todayStr, 0)
    yamlDict[todayStr] += 1
        
    # update the file with making a new commit
    commitMessage = "Made new commit at: " + str(datetime.now())
    updateYamlFileStr = yaml.dump(yamlDict)
    repo.update_file(WORKING_FILE_PATH, commitMessage, updateYamlFileStr, yamlFileSha)
        
    # logging that we successfully made a new contribution by commiting
    logging.info("Created new commit => +1 contribution")
        

def main():
    # load the configuration and get a Github instance
    configDict = loadConfig()
    g = Github(configDict['token'])

    # calculate the probability for making a commit this time
    runProb = calcRunProbability(configDict['runEvery'], configDict['contributionsPerDay'])

    # get random bool and if true make a commit (boolean based on probability)
    if (True):
        makeCommit(g, configDict['repoName'])


if __name__ == '__main__':
    # init the logger by specifing the 
    # log file path, logging message format and log level
    logging.basicConfig(
        filename='logs/bot.log',
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG)

    # run the main method
    main()