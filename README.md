
[Job Search](https://github.com/djibybalde/job_search) 
==========
Build a [`Job Finder`](https://github.com/djibybalde/job_search) to scrape jobs on https://fr.indeed.com website.


External tool
=============
This material uses `ChromeDriver` to run and control `Google Chrome browser`. So, you should have `Chrome navigator` in your computer and download [`ChromeDriver`](https://chromedriver.chromium.org) from [here](https://chromedriver.chromium.org). 
After downloading [ChromeDriver](https://chromedriver.chromium.org), put it the `references` folder with the name `chromedriver`. 

How to use this [`Job Finder`](https://github.com/djibybalde/job_search)
============

To install the material in your computer:
- Open your Terminal
- Go to the [job_search](https://github.com/djibybalde/job_search) folder
```bash
$ cd job_search
```
- Run the following to install the necessary packages
```bash
$ pip install pipenv
$ pipenv install
```
or 
```bash
$ pip install job_search
```

- Enter your [fr.indeed.com](https://fr.indeed.com) `E-mail` and `password`, when instructed.
```
Enter your E-mail address here: my_email@example.com
Enter your password here: ********

```
```bash
$ python
>>> from indeed import JobFinder
>>> JobFinder().get_results()
```

You can specifier some arguments:
- `job_title[OPTIONAL]`: the title of the job you are looking for, e.g. `Data Science`
- `location[OPTIONAL]`: your favorite location or address, e.g. `Paris` 
- `job_type[OPTIONAL]`: `CDI` or `CDD`
- `length[OPTIONAL]`: the number of jobs to scrape and write in the `data` e.g. 20

For example

```bash
$ python
>>> from indeed import JobFinder
>>> JobFinder(job_title='Data Science', location='Lyon', length=10).get_results()
```

Enjoy with [Job Search](https://github.com/djibybalde/job_search) and **good Luck!**