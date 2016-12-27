# Grab Yo Umbrella
A utility for people too lazy to use a weather app everyday, it texts you instead.  
This was tested on Ubuntu Linux with Python 2.7.12

## Dependencies  
> pip install pyyaml  
> pip install smptlib  

## Setup
1. The config.yaml needs to be populated with information e.g smtp server etc  
2. I use openweathermap as the weather forecast provider(It's free)  
3. I setup a cron job to text me every morning at 7 AM. My cron entry looks like this,  
  0 7 * * * /usr/bin/python /path/to/alert_me.py /path/to/config.yaml
