#!/bin/sh

echo "<==-- WELCOME TO DICTIONARY ATTACK --==>\n\n<== Create Dictionary ==>\n"

echo "\n<== Target Dictionary ==>\n"
read -p "Enter name of the file: " TD_FILE_NAME
python TDAT.py -f ${TD_FILE_NAME}

echo "\n\n<== CRUNCH ==>\n"
read -p "Enter the minimum length string you want crunch to start at: " MIN_LEN
read -p "Enter the maximum length string you want crunch to end with: " MAX_LEN
read -p "Enter characters used: " CHARACTERS
read -p "Enter name of the file: " C_FILE_NAME

echo "\n\n"
crunch ${MIN_LEN} ${MAX_LEN} ${CHARACTERS} > ${C_FILE_NAME}


echo "\n\n<== Word Harvest ==>\n"
read -p "Do you want to run word harvest (yes|no): " CHOICE

if [ "$CHOICE" == "yes" ]
then
    read -p "Enter Directory: " DIR
    read -p "Enter name of the file: " W_FILE_NAME
    echo "\n\n"
    ./wordharvest -d ${DIR} -o ${W_FILE_NAME}
fi


echo "\n\n<==== Combining all generated files to dictionary.txt ====>"
if [ "$CHOICE" == "yes" ]
then
    cat ${TD_FILE_NAME} ${C_FILE_NAME} ${W_FILE_NAME} > dictionary.txt
else
    cat ${TD_FILE_NAME} ${C_FILE_NAME} > dictionary.txt
fi


echo "\n\n<== Perform Dictionary Attack ==>\n"
read -p "Enter the path to zip file for attack: " ZIP_FILE_PATH

echo "\n\n"
python DictionaryAttack.py -l dictionary.txt -f ${ZIP_FILE_PATH}

echo "\n\nTHANK YOU FOR USING OUR SERVICE !!!\n"