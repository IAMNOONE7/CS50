#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];
    FILE *out = NULL;
    int file_index = 0;
    char filename[8];

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            if (out != NULL)
            {
                fclose(out);
            }

            sprintf(filename, "%03i.jpg", file_index++);

            out = fopen(filename, "wb");
            if(out == NULL)
            {
                fclose(card);
                printf("Could not create output file.\n");
                return 1;
            }
        }

        if(out != NULL)
        {
            fwrite(buffer,1,512,out);
        }
    }

    if(out!=NULL)
    {
        fclose(out);
    }
    fclose(card);
    return 0;

}

