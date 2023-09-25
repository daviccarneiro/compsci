#ifndef _MYGL_H_
#define _MYGL_H_

class Point {
public:
    int x;
    int y;

    Point() : x(0), y(0) {}
    Point(int x, int y) : x(x), y(y) {}
};

class Color {
public:
    int red;
    int green;
    int blue;
    int alpha;

    Color() : red(0), green(0), blue(0), alpha(255) {}
    Color(int r, int g, int b, int a) : red(r), green(g), blue(b), alpha(a) {}
};

void MyGlDraw(void);

#endif

