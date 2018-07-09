# Password Strength Calculator

This script define your password strength.  
Main idea is that your password has already max strength = 10.  
But if it hasn't both upper and lowercase, numbers, or it length less than 8,  
strength will be weakened for 2 points per each factor respectivily.  
If your password contains words from popular data lists (userdata, dates, abbreveations),  
total strength decrease by 1 point for each overlap.  

# How to start

Script requires you Python 3.5  
Start on Linux  
```bash
$ python password_strength.py password
```
**For example**, 
```bash
$ python password_strength.py qwerty123
```

#P.S.

You should find blacklist and other forbidden list by yourself. List in this script is only for example.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
