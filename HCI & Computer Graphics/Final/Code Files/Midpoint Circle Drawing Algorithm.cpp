#include <graphics.h>
#include <iostream>
using namespace std;

void drawCircleMidpoint(int xc, int yc, int r) {
    int x = 0;
    int y = r;
    int p = 1 - r;

    while (x <= y) {
        putpixel(xc + x, yc + y, WHITE);
        putpixel(xc - x, yc + y, WHITE);
        putpixel(xc + x, yc - y, WHITE);
        putpixel(xc - x, yc - y, WHITE);
        putpixel(xc + y, yc + x, WHITE);
        putpixel(xc - y, yc + x, WHITE);
        putpixel(xc + y, yc - x, WHITE);
        putpixel(xc - y, yc - x, WHITE);

        x++;
        if (p < 0)
            p = p + 2 * x + 1;
        else {
            y--;
            p = p + 2 * (x - y) + 1;
        }
    }
}

int main() {
    int gd = DETECT, gm;
    initgraph(&gd, &gm, "");

    drawCircleMidpoint(300, 200, 100);

    getch();
    closegraph();
    return 0;
}

