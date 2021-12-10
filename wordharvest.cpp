#include <iostream>
#include <forward_list>
#include <string.h>
#include <unistd.h>
#include <algorithm>
#include <sstream>

using namespace std;

#define MAXTABLE 100000

forward_list<string> list;
forward_list<char*> hash_tab[MAXTABLE];

/*** Hash table functions ***/
/** XOR version djb2 algorithm */
unsigned long hash_function(char *str) {
    int c;
    unsigned long hash = 5381; /* seed */
    while ((c = *str++))
        hash = ((hash << 5) + hash) ^ c;
    return hash;
}

void write_file(char *word, FILE *fp) {
    /* hash index fitting the table size (hash mod MAXTABLE) */
    unsigned long index = hash_function(word) % MAXTABLE; /* searching only at hash index */
	auto findIter = find(hash_tab[index].begin(), hash_tab[index].end(), word);
    bool found = (findIter != hash_tab[index].end());
    if (!found) {
        hash_tab[index].push_front(word);
        fprintf(fp, "%s\n", word);
    }
}


void harvest_words(char *filename, FILE *ofp) {
    FILE *fp;
    char word[30]; /* 29 char words */
    if ((fp = fopen(filename, "r")) == NULL) {
        fprintf(stderr, "can't open file %s", filename);
    }
    else {
        /* scan for alphanumeric words */
        while (fscanf(fp, "%29[a-zA-Z0-9]", word) == 1) {
            write_file(word, ofp);
            /* any other char is a word separator */
            if (fscanf(fp, "%29[^a-zA-Z0-9]", word) != 1) {
                continue;
            }
            fclose(fp);
        }
    }
}

void break_ext(char *str, forward_list<string>& list)
{
    char *saveptr, *token;
    for (int j = 0;; j++, str = NULL)
    {
        token = strtok_r(str, ":", &saveptr);
        if (token == NULL)
            /* ':' delimiter */
            break;
		list.push_front(token);
    }
}

void find_and_harvest(string dir, char *outfile) {
	auto p = list.begin();
	FILE *fp, *ofp;
	char command[1024], filename[1024];

	ofp = fopen(outfile,"w");
	if (!ofp) {
		perror("can't open write file");
		exit(1);
	}
	while (p != list.end()) {
        stringstream ss;
        ss << "find " << dir <<" -name \"*." << *p <<"\" -type f 2>/dev/null";
		if (snprintf(command, sizeof(command), "%s", ss.str().c_str()) > sizeof(command) )
		{
			fprintf(stderr,"path too long, it may be truncated");
		}
		/* send 'find' command */
		if ((fp = popen(command, "r")) == NULL) {
			perror("find");
		}
		/* harvest on each file found */
		while (fgets(filename, sizeof(filename)-1, fp) != NULL) {
			filename[strcspn(filename, "\n")] = 0;
			harvest_words(filename, ofp);
		}
		pclose(fp);
		p++;
	}
	fclose(ofp);
}


void usage() {
    cerr << "Usage: wordharvest [-e extensions] -d directory -o outfile\n";
    exit(1);
}

int main(int argc, char **argv)
{
    int opt, misopt, dflag = 0, eflag = 0, oflag = 0;
    string path;
    char* outfile;

    if (argc < 5)
        usage();
    /* comand-line options and arguments */
    while ((opt = getopt(argc, argv, ":d:o:e:")) != -1) {
        switch (opt) {
            case 'e':
                eflag = 1;
                if (optarg[0] == '-')
                    misopt = 'e';
                if (optarg)
                    break_ext(optarg, list);
                break;
            case 'd':
                if (optarg[0] == '-')
                    misopt = 'd';
                dflag = 1;
                path = argv[optind - 1];
                break;

            case 'o':
                if (optarg[0] == '-')
                    misopt = 'o';
                oflag = 1;
                outfile = argv[optind - 1];
                break;
            case ':':
                cerr << "option '-" << optopt << "' requires an argument\n";
                usage();
                break;
            case '?':
            default:
                cerr << "option '-" << optopt << "' is invalid\n";
                usage();
                break;
        }
    }
    // missing any option argument  
    if (optind < argc) {
        cerr << "option '-" << misopt << "' requires an argument\n";
        usage();
    }
    // missing required options
    if ((dflag && oflag) == 0) {
        cerr << "missing required option '-" << ((dflag == 0) ? "d" : "o") << "'\n";
        usage();
    }

    if (eflag == 0) {
		list.push_front("txt");
		list.push_front("text");
    }
    
    find_and_harvest(path, outfile);
    for(auto ht: hash_tab){
        ht.clear();
    }
    list.clear();
    cout << "WORD HARVEST DONE" << endl;
    return 0;
}