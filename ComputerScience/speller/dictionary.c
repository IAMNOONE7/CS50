// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 50000;

// Hash table
node *table[N];

static unsigned int word_count = 0;

unsigned int hash(const char *word)
{
    unsigned long h = 5381;
    for(const unsigned char *p = (const unsigned char *)word; *p;p++)
    {
        unsigned char c = (unsigned char)tolower(*p);
        h = ((h<<5)+h) ^c;
    }
    return (unsigned int)(h%N);
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int i = hash(word);
    for(node *cur = table[i]; cur != NULL; cur = cur -> next)
    {
        if(strcasecmp(cur -> word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *fp = fopen(dictionary, "r");
    if(fp == NULL)
    {
        return false;
    }

    char buffer[LENGTH+1];
    while(fscanf(fp, "%45s", buffer) ==1)
    {
        node *n = malloc(sizeof(node));
        if(!n)
        {
            fclose(fp);
            return false;
        }
        strcpy(n->word, buffer);

        unsigned int i = hash(n->word);
        n->next = table[i];
        table[i] = n;
        word_count++;
    }

    fclose(fp);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for(unsigned int i = 0; i < N; i++)
    {
        node *cur = table[i];
        while(cur)
        {
            node *next = cur -> next;
            free(cur);
            cur = next;
        }
        table[i] = NULL;
    }
    word_count = 0;
    return true;
}
