from itertools import permutations

class TDAT:
    def __init__(self, command_line=False, file_name=None) -> None:
        self.command_line = command_line
        if command_line:
            self.filename = file_name
        self.data = []
        self.separators = ["-", "_", "", "@", "."]
    
    def input(self):
        print("<==== STARTING the TDAT tool ===>\n--->Provide the answers to the questions.\n")
        if not self.command_line:
            filename = input(">>>> Enter name of the output file (press ENTER for default, 'result.txt'): ")
            self.filename = filename if len(filename) > 0 else "result.txt"

        print("\n\n<==== Must Enter Data ===>\n")
        first_name = input(">>> Target's first name: ")
        while len(first_name) == 0:
            first_name = input(">>> Target's first name: ")
        
        last_name = input(">>> Target's last name: ")
        while len(last_name) == 0:
            last_name = input(">>> Target's last name: ")
        
        tar_year = input(">>> Target's date of birth, enter year: ") 
        while len(tar_year) == 0:
            tar_year = input(">>> Target's date of birth, enter year: ") 
        tar_month = input(">>> Target's date of birth, enter month: ") 
        
        while len(tar_month) == 0:
            tar_month = input(">>> Target's date of birth, enter month: ") 
        
        tar_day = input(">>> Target's date of birth, enter day: ")
        while len(tar_day) == 0:
            tar_day = input(">>> Target's date of birth, enter day: ")

        self.data.append(first_name)
        self.data.append(last_name)
        self.data.append(tar_year)
        self.data.append(tar_month)
        self.data.append(tar_day)

        print("\n\n<==== Gathering More Data (press ENTER for unknown answers) ===>")
        nickname = input(">>> Nickname: ")
        self.data.append(nickname)
        spousename = input(">>> Spouse Name: ")
        if len(spousename) > 0:
            self.data.append(spousename)
            marrieddate = input(">>> What year was the target married on? ")
            if len(marrieddate) > 0:
                self.data.append(spousename)
        
        kidnames = input(">>> Child first name (separated by comma, if more than one): ")
        if len(kidnames) > 0:
            kid_names_list = kidnames.split(",")
            self.data.extend(kid_names_list)
        
        pet_name = input(">>> Pet's name: ")
        if len(pet_name) > 0:
            self.data.append(pet_name)
        
        company = input(">>> Company name: ")
        if len(company) > 0:
            self.data.append(company)
        
        key = input(">>> Keywords related to target (separated by space): ")
        keys = key.split()
        if len(keys) > 0:
            self.data.extend(keys)

        print("\n\n<==== Collecting all the data ===>")

    def write_combinations_to_file(self):
        print("<==== Started to make combinations ===>")
        with open(self.filename, 'w') as file:
            for i in range(1, len(self.data) + 1):
                for permutation in permutations(self.data, i):
                    if i != 1:
                        for sep in self.separators:
                            combined = sep.join(permutation)
                            file.write(combined + "\n")
                    else:
                        combined = "".join(permutation)
                        if len(combined) > 0:
                            file.write(combined + "\n")
        
        print("<==== DONE! saved as: " + self.filename + " ===>")

    def run(self):
        self.input()
        self.write_combinations_to_file()


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Target Dictionary')
    parser.add_argument('-f', required=True, metavar='Dictionary File', dest='file_name', help='Specify Dictionary File')
    args = parser.parse_args()
    tdat = TDAT(command_line=True, file_name=args.file_name)
    tdat.run()