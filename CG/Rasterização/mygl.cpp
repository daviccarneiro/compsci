#include "mygl.h"
#include <iostream>
#include <cmath>

using namespace std;

// Função para definir a cor de um pixel na matriz de imagem
void PutPixel(Point p, Color c) {
    // Calcula o índice do pixel na matriz de pixels:
    int pixelIndex = (p.x + p.y * IMAGE_WIDTH) * 4;

    // Escreve os componentes de cor na posição correta do pixel:
    FBptr[pixelIndex] = c.red;
    FBptr[pixelIndex + 1] = c.green;
    FBptr[pixelIndex + 2] = c.blue;
    FBptr[pixelIndex + 3] = c.alpha;
}

// Função para desenhar uma linha usando o algoritmo de Bresenham
void DrawLine(Point p0, Point p1, Color color) {
    int x0 = p0.x;
    int y0 = p0.y;
    int x1 = p1.x;
    int y1 = p1.y;

    int dx = abs(x1 - x0);
    int dy = abs(y1 - y0);
    int sx = x0 < x1 ? 1 : -1;
    int sy = y0 < y1 ? 1 : -1;
    int error = dx - dy;
    int x = x0;
    int y = y0;

    while (x != x1 || y != y1) {
        PutPixel(Point(x, y), color);

        // Atualiza o erro
        int newError = 2 * error;
        if (newError > -dy) {
            error -= dy;
            x += sx;
        }
        if (newError < dx) {
            error += dx;
            y += sy;
        }
    }
}

// Função para desenhar um triângulo conectando três pontos
void DrawTriangle(Point p0, Point p1, Point p2, Color color) {
    DrawLine(p0, p1, color);
    DrawLine(p1, p2, color);
    DrawLine(p2, p0, color);
}

void MyGlDraw(void) {
    // Desenha uma linha azul de (50, 50) a (200, 200)
    Point lineStart(50, 50);
    Point lineEnd(200, 200);
    Color blue(0, 0, 255, 255);
    DrawLine(lineStart, lineEnd, blue);

    // Desenha um triângulo vermelho com vértices em (300, 50), (200, 175) e (300, 150)
    Point vertex1(300, 50);
    Point vertex2(200, 175);
    Point vertex3(300, 150);
    Color red(255, 0, 0, 255);
    DrawTriangle(vertex1, vertex2, vertex3, red);
}

