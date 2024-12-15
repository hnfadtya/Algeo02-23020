#include "listrec.h"
#include <stdio.h>
#include <stdlib.h>

void mergeSortedUnique(List l1, List l2, List *res) {
    while (!isEmpty(l1) && !isEmpty(l2))
    {
        if (head(l1) <= head(l2))
        {
            if (!isMember(*res, head(l1)))
            {
                *res = konsb(*res, head(l1));
                
            }
            l1 = tail(l1);
        }
        else
        {
            if (!isMember(*res, head(l2)))
            {
                *res = konsb(*res, head(l2));
            }
            l2 = tail(l2);
        }
    }

    while(!isEmpty(l1))
    {
        if (!isMember(*res, head(l1)))
        {
            *res = konsb(*res, head(l1));
            
        }
        l1 = tail(l1);
    }
    
    while (!isEmpty(l2))
    {
        if (!isMember(*res, head(l2)))
        {
            *res = konsb(*res, head(l2));
        }
        l2 = tail(l2);
    }
}