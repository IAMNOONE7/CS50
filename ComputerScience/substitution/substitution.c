#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool validate(string key);

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    if(!validate(key))
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        char c = plaintext[i];
        if(isalpha(c))
        {
            if(isupper(c))
            {
                int index = c - 'A';
                char sub = toupper(key[index]);
                printf("%c",sub);
            }
            else
            {
                int index = c - 'a';
                char sub = tolower(key[index]);
                printf("%c",sub);
            }
        }
        else
        {
            printf("%c",c);
        }
    }
    printf("\n");
    return 0;
}

bool validate(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }

    bool used[26] = {false};

    for(int i = 0; i < 26 ; i++)
    {
        if(!isalpha(key[i]))
        {
            return false;
        }

        int index = toupper(key[i]) - 'A';
        if(used[index])
        {
            return false;
        }
        used[index] = true;
    }
    return true;
}
