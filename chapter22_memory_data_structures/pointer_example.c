#include <stdio.h>
#include <stdlib.h>

struct Person {
 int age;
 char gender;
 double height; 
 struct Person* spouse;
 int n_children;
 struct Person* children;
};
typedef struct Person Person;

void marry(Person* p1, Person* p2) {
 p1->spouse = p2;
 p2->spouse = p1;
}

int main() {
 Person Jane = {30, 'M', 5.9, NULL};
 Person Bob = {28, 'F', 5.5, NULL};
 marry(&Jane, &Bob);
 printf("Jane is %f feet tall\n", Jane.height);
 printf("Bobs spouse is %f feet tall\n",
  Bob.spouse->height);
 int NUM_KIDS = 5;
 Jane.n_children = NUM_KIDS;
 Jane.children = (Person*) malloc(
   NUM_KIDS*sizeof(Person));
 Bob.n_children = NUM_KIDS;
 Bob.children = Jane.children;
 for (int i=0; i<NUM_KIDS; i++) {
   Person* ith_kid = &Jane.children[i];
   if (i<3) ith_kid->gender='M';
   else ith_kid->gender='F';
 }
 int n_sons = 0;
 for (int i=0; i<NUM_KIDS; i++) {
   if (Jane.children[i].gender=='M') n_sons++;
 }
 printf("Jane has %i sons\n", n_sons);
 free(Jane.children);
 return 0;
}
