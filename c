#include <stdio.h>
#include<stdlib.h>
#define n 5
int q[n];
int front=-1;
int rear=-1;

void enqueue();
void dequeue();
void peek();
void display();

void enqueue()
{
    int data;
    printf("Enter the data\n");
    scanf("%d",&data);
    if(rear==n-1)
    {
        printf("Queue overflow\n");
    }
    else if(front==-1 && rear==-1)
    {
        front=rear=0;
        q[rear]=data;
    }
    else
    {
        rear++;
        q[rear]=data;
    }
}
void peek()
{
    if(front==rear==-1)
    {
        printf("Queue unerflow\n");
    }
    else
    {
        printf("The 1st element in the queue is %d",q[front]);
    }
}
void dequeue()
{
    if(front==rear==-1)
    {
        printf("Queue underflow\n");
    }
    else if(front==rear)
    {
        front=rear=-1;
    }
    else
    {
        printf("The deleted element is %d",q[front]);
        front++;
    }
}
void display()
{
    printf("The elements in the queue are ");
    for(int i=front;i<=rear;i++)
    {
        printf("%d\t",q[i]);
    }
}
int main() {
    // Write C code here
       int ch;
    do
    {
    printf("\nEnter choice:\n1.Enqueue\n2.Dequue\n3.Peek\n4.Display\n");
    scanf("%d",&ch);
    switch(ch)
    {
    case 1:
    enqueue();
    break;
    case 2:
    dequeue();
    break;
    case 3:
    peek();
    break;
    case 4:
    display();
    break;
    default:
    printf("Invalid choice\n");
    }
    }while(ch!=0);
    return 0;

    return 0;
}
