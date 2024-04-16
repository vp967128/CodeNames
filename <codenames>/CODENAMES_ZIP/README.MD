# In order to run the backend, you need to run the following commands in MacOS

```
#1. Create VirtualEnv for Flask with name `ditto`
> virtualenv ditto

#2. Activate VirtualEnv
> source bin/activate

#3. Install Dependencies
> pip install -r requirements.txt

#4. Run Flask Backend
> flask run

Go to http://127.0.0.1:5000/admin
  ```

<details>
  <summary>Windows</summary>
  
  1. Create VirtualEnv for Flask with name `ditto`
  > virtualenv ditto
  
  2. Activate VirtualEnv
  > ditto/bin/activate
  
  3. Install Dependencies
  > pip install -r requirements.txt
  
  4. Create DB Instance
  > Flask shell
  > db.create_all()
  > db.session.commit()
  
  5. Exit Shell by Pressing Ctrl + Z or Ctrl + C
  
  6. Run Flask Backend
  > flask run
  
  7. Go to http://127.0.0.1:5000/admin
</details>
