import yaml
import logging
import random
from github import Github

def loadConfig() -> dict:
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
        configDict['runsEvery'] = config['contributions']['runEvery']
        configDict['contributionsPerDay'] = config['contributions']['contributionsPerDay']
    except KeyError:
        logging.error("The config file misses a key! Copy 'config-example.yaml' to 'config.yaml'!")

    return configDict

def randomProbability(probability: float) -> bool:
    return random.random() < probability

def calcRunProbability(runEvery: int, contributionPerDay: int) -> float:
    runsPerDay = 24 * 60 / runEvery
    contributionProbabilty = contributionPerDay / runsPerDay
    return contributionProbabilty

def makeCommit(g: Github, repoName: str, runProb: float) -> None:
    if (randomProbability(runProb)):
        logging.info("Making a log entry for a new commit.")
        

def main():
    configDict = loadConfig()
    g = Github(configDict['token'])
    runProb = calcRunProbability(configDict['runEvery'], configDict['contributionsPerDay'])
    makeCommit(g, configDict['repoName'], runProb)

if __name__ == '__main__':
    logging.basicConfig(
        filename='logs/bot.log',
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG)
    main()