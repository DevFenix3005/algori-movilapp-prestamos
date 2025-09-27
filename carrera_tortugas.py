from turtle import *
from random import randint
meta_x = 200

def dance(t):
   t.speed(15)
   t.left(randint(0, 90))
   j = 0
   while j < 8:          
       t.penup()
       t.goto(0, 0)
       t.pendown()
       i = 1
       while i < 32:
           t.forward(i)
           t.left(i/2+5)
           i += 1
       j += 1
   t.penup()
   t.goto(0, 0)



t1 = Turtle()
t1.color('red')
t1.shape("turtle")
t1.penup()
t1.teleport(-200, 0)

t2 = Turtle()
t2.color('blue')
t2.shape("turtle")
t2.penup()
t2.teleport(-200, -60)

while t1.xcor() < meta_x and t2.xcor() < meta_x:
    t1.forward(randint(2,7))
    t2.forward(randint(2,7))

resultado = max(t1.xcor(), t2.xcor())

if resultado == t1.xcor():
    dance(t1)
if resultado == t2.xcor():
    dance(t2)
