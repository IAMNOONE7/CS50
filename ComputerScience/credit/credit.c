#include <cs50.h>
#include <stdio.h>


int luhn(long n);
int length(long n);
int first_two(long n);

int main(void)
{
    long n = get_long("Number: ");

    if(luhn(n) != 0)
    {
        //
    }

    int len = length(n);
    int firsttwo = first_two(n);
    int first = firsttwo/10;

    if(luhn(n)==0)
    {
        if(len == 15 && (firsttwo == 34 || firsttwo == 37))
        {
            printf("AMEX\n");
        }
        else if(len == 16 &&(firsttwo >= 51 && firsttwo<=55))
        {
            printf("MASTERCARD\n");
        }
        else if((len == 13 || len == 16) && first ==4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

}



int luhn(long n)
{
    int sum = 0;
    bool _switch = false;

    while(n>0)
    {
        int digit = n%10;
        n/=10;

        if(_switch)
        {
            int d = digit*2;
            sum += (d/10) + (d%10);
        }
        else
        {
            sum += digit;
        }
        _switch = !_switch;
    }
    return sum%10;
}

int length(long n)
{
    int len = 0;
    while(n>0)
    {
        n/=10;
        len++;
    }
    return len;
}


int first_two(long n)
{
    while(n >= 100)
    {
        n/=10;
    }
    return (int)n;
}
