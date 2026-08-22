#include <graphics.h>
#include <iostream>
using namespace std;

void drawLineMidpoint(int x1, int y1, int x2, int y2) {
    int dx = x2 - x1;
    int dy = y2 - y1;

    int d = dy - (dx / 2);
    int x = x1, y = y1;

    putpixel(x, y, WHITE);

    while (x < x2) {
        x++;

        if (d < 0) {
            d = d + dy;
        } else {
            d = d + (dy - dx);
            y++;
        }
        putpixel(x, y, WHITE);
    }
}

int main() {
    int gd = DETECT, gm;
    initgraph(&gd, &gm, "");

    drawLineMidpoint(100, 100, 400, 300);

    getch();
    closegraph();
    return 0;
}

