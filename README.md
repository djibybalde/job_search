
[JobFinder](https://github.com/djibybalde/job_search) 
==========

Build a [`JobFinder`](https://github.com/djibybalde/job_search) to scrape jobs on https://fr.indeed.com.


External tool
=============
This material uses [`ChromeDriver`](https://chromedriver.chromium.org) to run and control `Google Chrome browser`. 
So, make sur that you have `Chrome navigator` in your computer or download it. 
If your are using MacOS, you don't have to download [ChromeDriver](https://chromedriver.chromium.org). 
Otherwise, download it from [here](https://chromedriver.chromium.org) and put it in the `references` folder with the name `chromedriver`. 


How to use this [`JobFinder`](https://github.com/djibybalde/job_search)
============

To install the material in your computer:
- Open your Terminal
- Go to the [job_search](https://github.com/djibybalde/job_search) folder and install the necessary packages as following
```bash
$ cd job_search
$ pip install pipenv
$ pipenv install
```
or 
```bash
$ cd job_search
$ pip install job_search
```

- After installation, run the following to scrape your job and apply it. 
```bash
$ python
>>> from indeed import JobFinder
>>> JobFinder().get_results()
```

- You can also specifier some arguments:
- `login[OPTIONAL]`: Whether to login with your email and password on the website.  
- `job_title[OPTIONAL]`: What job are you looking for ? Default is `Data Science` 
- `location[OPTIONAL]`: Where do you want to apply for job ? For example Paris, Lyon.
- `max_numb[OPTIONAL]`: How many example of job do you want to apply ? Default is 20. 

```bash
$ python
>> from indeed import JobFinder
>> JobFinder(login=True, job_title='Data Science', location='Lyon', max_numb=10).get_results()
```

- ***Note that*** if you set `login=True`, your [fr.indeed.com](https://fr.indeed.com) `email` and `password` will be asked to login.

**Enjoy with [JobFinder](https://github.com/djibybalde/job_search) and *good Luck!***
