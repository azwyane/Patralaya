## PATRALAYA

## Table of Contents
- [Requirements](#Requirements)
- [ForkWorkflow](#ForkWorkflow)
- [BasicWorkflow](#BasicWorkflow)


### Requirements
- Install python 3.7/3.8/3.9 (python 3.7/3.8 would be better)

### ForkWorkflow

1. #### FORK THE REPO 
2. #### CLONE YOUR FORK TO YOUR LOCAL MACHINE
   ```sh
   $ git clone https://github.com/<yourname>/Patralaya.git
   ```
3. #### MAKE YOUR CHANGES (follow steps 3 and 4 mentioned in BasicWorkflow)
4. #### COMMIT THE CHANGES
   ```
   git add .
   git status <shows your files added to the git stage>
   git commit -m "<commit message>"
   ```
5. #### ADD ORIGINAL REPO 
   ```
    $ git remote add upstream https://github.com/azwyane/Patralaya.git
    $ git fetch upstream
    $ git checkout master
    $ git merge upstream/master

    ```
> If you get no conflicts then push the changes to your fork
6. #### PUSH THE CHANGES TO YOUR FORK
   ```
   $ git push origin master
   ```
7. #### MAKE A PULL REQUEST TO THE MAIN REPO IN GITHUB
8. #### BE READY TO REPEAT THE SAME STEPS BUT FIRST ALWAYS BE UPDATE WITH ORIGINAL REPO(step 5.2)

### BasicWorkflow

1. #### GOTO YOUR WORKSPACE AND OPEN UP A SHELL/TERMINAL
> Clone the repo to your local device 
```
$ git clone https://github.com/azwyane/Patralaya.git
```
This will create a folder called Patralaya in your workspace with 
all the files and folders from the repo.

2. #### NOW CD INTO PATRALAYA (ROOT FOLDER) AND THEN FOLLOW AS:
```
$ python3 -m venv venv
``` 
This will create a virutal environment for the project named as venv in side the base directory(Patralaya)

3. #### ACTIVATE THE VIRTUAL ENVIRONMENT AS:

> ### IT IS THE MOST CRUCIAL STEP SO DONT FORGET TO ACTIVATE BEFORE GETTING YOUR HANDS ON


- If on GNU/Linux follow as:
```
$ . venv/bin/activate
```

- If on windows follow as: refer to [here](https://docs.djangoproject.com/en/3.1/howto/windows/)
```
...\> venv\Scripts\activate.bat
```
which will result as this (virtual env for the project): 
```
(venv)$ 
```
4. GET THE HACK DONE (refer to working with [Django project](https://docs.djangoproject.com/en/3.1/))

```
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
(venv)$ python manage.py migrate
(venv)$ python manage.py makemigrations
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver
```

5. BEFORE SUBMITTING THE PUSH ALWAYS REMEMBER TO SHARE CODE WITH PEERS TO BE SURE OF THE CHANGES, THEN CHECK THE LATEST CHANGES IN THE REPO 

For that follow as:
```
$ git fetch origin
$ git checkout master
$ git merge origin/master
```
> Be sure to check the conflicts, don't remove anything from
> the repo by yourself to manage conflict if you aren't sure about that 
> so discuss to Peers for necessary solution

Then make push by:
```
$ git push origin master
```

### The project can be run on docker

- Clone the repo and then follow with:

```
$ docker build .
```
```
$ docker-compose up
```

after stopping dont forget to `$ docker-compose down`

After making changes run by:

```
$ docker-compose build
```



Project is licensed under:

![GNU GPLV3](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)