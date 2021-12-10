# Dictionary Attack

### Components

* Target Dictionary Creation: `TDAT.py`
    - This python code is used to create a target dictionary using the personal details of the target person. The code is Modular so that it can also be used as a part of another project as well.

* Crunch Dictionary Creation: `crunch`
    - A linux command which creates strings from the characters given within the specified range.
    - usage: ```crunch min_len max_len characters_used > file_name.txt```

* Attack Zip File: `DictionaryAttack.py`
    - This python code is used to attack the encrypted zip file using a user provided dictionary. The dictionary passwords are converted into bytes and then an attack is performed. Zipfile module is used for this purpose
    - usage: ```python DictionaryAttack.py -l dictionary.txt -f ZIP_FILE_PATH```

* Run Script: `run_dictionary_attack.sh`
    - This combines all the modules like TDAT.py, Crunch and Dictionary attack on one single run script.

 
### Pre-requisite
 
* Linux Terminal
* Python 3
* Python libraries  
    - tqdm
* C++ 11 or above
* Crunch
 
 
### TO Run
 
```
./run_dictionary_attack.sh
```


