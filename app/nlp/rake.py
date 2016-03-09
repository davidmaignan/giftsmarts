from app.vendor.rake import Rake
from app.config.config import config

rake_runner = Rake(config["STOPLIST"])

def run(text):
    return rake_runner.run(text)
