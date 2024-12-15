#include "boolean.h"
#include "listrec.h"
#include <stdio.h>
#include <stdlib.h>

int main()
{
    List l = NIL, hasil = NIL;
    int N, mid;
    ElType elmt;
    scanf("%d", &N);
    for (int i = 0; i < N; i++)
    {
        scanf("%d", &elmt);
        l = konsb(l, elmt);
    }
    List reversed = reverseList(l);
    int len = length(l);
    mid = len / 2;
    Address p = l;
    Address q = reversed;

    for (int i = 0; i < mid; i++)
    {
        hasil = konsb(hasil, INFO(p));
        hasil = konsb(hasil, INFO(q));
        p = NEXT(p);
        q = NEXT(q);
    }
    if (len % 2 == 1)
    {
        hasil = konsb(hasil, INFO(p));
    }
    
    displayList(hasil);
}