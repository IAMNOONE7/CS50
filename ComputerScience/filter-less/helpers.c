#include "helpers.h"
#include <math.h>


static inline BYTE CapSepia(int x)
{
    if(x<0) return 0;
    if(x>255) return 255;
    return(BYTE)x;
}
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;

            BYTE avg = (BYTE) round((r+g+b)/3.0);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;

            int SR = (int) round(0.393 * r + 0.769 * g + 0.189 *b);
            int SG = (int) round(0.349 * r + 0.686 * g + 0.168 *b);
            int SB = (int) round(0.272 * r + 0.534 * g + 0.131 *b);

            image[i][j].rgbtRed = CapSepia(SR);
            image[i][j].rgbtGreen = CapSepia(SG);
            image[i][j].rgbtBlue = CapSepia(SB);
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
     // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width/2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width -1 -j] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
      // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for(int i = 0; i<height;i++)
    {
        for(int j = 0; j<width;j++)
        {
            int sumR = 0;
            int sumG = 0;
            int sumB = 0;
            int count = 0;
            for(int di = -1; di<=1;di++)
            {
                for(int dj = -1; dj<=1;dj++)
                {
                    int xi = i + di;
                    int xj = j + dj;
                    if(xi < 0 || xi >= height || xj < 0 || xj >= width)
                    {
                        continue;
                    }

                    sumR += copy[xi][xj].rgbtRed;
                    sumG += copy[xi][xj].rgbtGreen;
                    sumB += copy[xi][xj].rgbtBlue;
                    count++;
                }
            }
            image[i][j].rgbtRed = (BYTE) round(sumR/(double)count);
            image[i][j].rgbtGreen = (BYTE) round(sumG/(double)count);
            image[i][j].rgbtBlue = (BYTE) round(sumB/(double)count);
        }
    }

}
