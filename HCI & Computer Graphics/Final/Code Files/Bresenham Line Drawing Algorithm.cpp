#include <graphics.h>
#include <iostream>
using namespace std;

void drawLineBresenham(int x1, int y1, int x2, int y2) {
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);

    int p = 2 * dy - dx;
    int x = x1, y = y1;

    int xEnd = x2;

    while (x <= xEnd) {
        putpixel(x, y, WHITE);
        x++;

        if (p < 0) {
            p = p + 2 * dy;
        } else {
            y++;
            p = p + 2 * (dy - dx);
        }
    }
}

int main() {
    int gd = DETECT, gm;
    initgraph(&gd, &gm, "");

    drawLineBresenham(100, 100, 400, 300);

    getch();
    closegraph();
    return 0;
}
