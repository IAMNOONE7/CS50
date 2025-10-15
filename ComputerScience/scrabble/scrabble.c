#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int compute(string w);

int main(void)
{

    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int player1 = compute(word1);
    int player2 = compute(word2);

    if(player1>player2)
    {
        printf("Player 1 wins!\n");
    }
    else if(player1<player2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    // Print the winner
}


int compute(string w)
{
    int points_arr[]= {1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10};
    int points = 0;

    for (int i = 0; i<strlen(w); i++)
    {
        if(isupper(w[i]))
        {
            points += points_arr[w[i] - 'A'];
        }
        if(islower(w[i]))
        {
            points += points_arr[w[i] - 'a'];
        }
    }

    return points;
}
