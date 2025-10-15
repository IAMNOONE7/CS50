#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    double L = (double) letters * 100.0 / (double)words;
    double S = (double) sentences * 100.0 / (double)words;
    int grade = (int)round(0.0588 * L - 0.296 * S - 15.8);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if(grade>=16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n",grade);
    }

    // Compute the Coleman-Liau index

    // Print the grade level
}

int count_letters(string text)
{
    int count = 0;

    for(int i = 0; text[i] != '\0'; i++)
    {
        if(isalpha((unsigned char) text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 0;
    bool end = false;

    for(int i = 0; text[i] != '\0'; i++)
    {
        if(isspace((unsigned char) text[i]))
        {
            end = false;
        }
        else if(!end)
        {
            end = true;
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;

    for(int i = 0; text[i] != '\0'; i++)
    {
        char c = text[i];
        if(c == '.' || c == '!' || c == '?')
        {
            count ++;
        }
    }
    return count;
}
