# Grab Yo Umbrella
A utility for people too lazy to use a weather app everyday, it texts you instead.  
This was tested on Ubuntu Linux with Python 2.7.12 

# Installation
cd /location/of/repository  
sudo -H pip install .

# Usage
#### This will retrieve the weather forecast and print it to console
grab_yo_umbrella <config_file_location>
#### This will retrieve the weather forecast, print it to console and send a text
grab_yo_umbrella <config_file_location> --text

# Notes
1. The config.yaml needs to be populated with information e.g smtp server etc  
2. I use openweathermap as the weather forecast provider(It's free)  
3. I setup a cron job to text me every morning at 7 AM. My cron entry looks like this,  
```0 7 * * * grab_yo_umbrella /path/to/config.yaml --text >> /path/to/log/file 2>&1```  
The bit at the end is to log the results of the day
