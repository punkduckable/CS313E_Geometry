"""File: Geom.py

   Description: Does some basic geometry

   Student Name: Robert Stephany

   Student UT EID: rrs2558

   Course Name: CS 313E

   Unique Number: 85575

   Date Created: 06/15/2019

   Date Last Modified: 06/15/2019 """

import math

# floating point equality
def is_equal (a, b):
    tol = 1.0e-16
    return (abs (a - b) < tol)



class Point (object):
    # constructor
    # x and y are floats
    def __init__ (self, x = 0, y = 0):
        self.x = x
        self.y = y

    # get distance
    # other is a Point object
    def dist (self, other):
        return math.hypot (self.x - other.x, self.y - other.y)

    # get a string representation of a Point object
    # takes no arguments
    # returns a string
    def __str__ (self):
        return '(' + str(self.x) + ", " + str(self.y) + ")"

    # test for equality
    # other is a Point object
    # returns a Boolean
    def __eq__ (self, other):
        tol = 1.0e-16
        return ((abs (self.x - other.x) < tol) and (abs(self.y - other.y) < tol))



class Circle (object):
    # constructor
    # x, y, and radius are floats
    def __init__ (self, radius = 1, x = 0, y = 0):
        self.radius = radius;
        self.center = Point (x, y);

    # compute cirumference
    def circumference (self):
        return 2.0*math.pi*self.radius;

    # compute area
    def area (self):
        return math.pi * self.radius * self.radius;

    # determine if point is strictly inside circle
    def point_inside (self, p):
        return (self.center.dist(p) < self.radius);

    # determine if a circle c is strictly inside this circle
    def circle_inside (self, c):
        distance = self.center.dist (c.center);
        return (distance + c.radius) < self.radius;

    # determine if a circle c overlaps this circle (non-zero area of overlap)
    # but neither is completely inside the other
    # the only argument c is a Circle object
    # returns a boolean
    def circle_overlap (self, c):
        # The two circles overlap if the distance between their centers is less
        # than the sum of their radii
        center_distance = self.center.dist(c.center);
        return (center_distance < (self.radius + c.radius));

    # determine the smallest circle that circumscribes a rectangle
    # the circle goes through all the vertices of the rectangle
    # the only argument, r, is a rectangle object
    def circle_circumscribe (self, r):
        # The smallest circle to circumscribe a rectangle is the circle whose
        # center is at the center of the rectangle and whose radius is
        # the distance to any one of the four corners (they are all equidistance
        # from the center)
        center_x = r.ul.x + (r.lr.x - r.ul.x)/2;
        center_y = r.lr.y + (r.ul.y - r.lr.y)/2;
        center = Point(center_x, center_y);

        radius = center.dist(r.ul);

        return Circle(radius, center_x, center_y);


    # string representation of a circle
    # takes no arguments and returns a string
    def __str__ (self):
        return "Radius: " + str(self.radius) + ", Center: " + str(self.center)

    # test for equality of radius
    # the only argument, other, is a circle
    # returns a boolean
    def __eq__ (self, other):
        return is_equal(self.radius, other.radius);



def interval_intersection(a1, b1, a2, b2):
    """This function determines if the two intervals (a1, b1), (a2, b2)
    intersect.

    If max(a1, a2) < min[b1, b2] then they intersect. """
    a = max(a1, a2);
    b = min(b1, b2);

    if (a < b):
        return True;
    else:
        return False;


class Rectangle (object):
    # constructor
    def __init__ (self, ul_x = 0, ul_y = 1, lr_x = 1, lr_y = 0):
        if ((ul_x < lr_x) and (ul_y > lr_y)):
            self.ul = Point (ul_x, ul_y);
            self.lr = Point (lr_x, lr_y);
        else:
            self.ul = Point (0, 1);
            self.lr = Point (1, 0);

    # determine length of Rectangle (distance along the x axis)
    # takes no arguments, returns a float
    def length (self):
        return (self.lr.x - self.ul.x);

    # determine width of Rectangle (distance along the y axis)
    # takes no arguments, returns a float
    def width (self):
        return (self.ul.y - self.lr.y);

    # determine the perimeter
    # takes no arguments, returns a float
    def perimeter (self):
        return 2*(self.width() + self.length());

    # determine the area
    # takes no arguments, returns a float
    def area (self):
        return self.width()*self.length();

    # determine if a point is strictly inside the Rectangle
    # takes a point object p as an argument, returns a boolean
    def point_inside (self, p):
        # p is inside of self if p is between ul and lr's x and y coordinates
        in_x = (self.ul.x < p.x < self.lr.x);
        in_y = (self.lr.y < p.y < self.ul.y);

        return (in_x and in_y);

    # determine if another Rectangle is strictly inside this Rectangle
    # takes a rectangle object r as an argument, returns a boolean
    # should return False if self and r are equal
    def rectangle_inside (self, r):
        # this happens if r's ul and lr points are inside of self.
        return (self.point_inside(r.ul) and self.point_inside(r.lr));

    # determine if two Rectangles overlap (non-zero area of overlap)
    # takes a rectangle object r as an argument returns a boolean
    def rectangle_overlap (self, r):
        # the two rectangles overlap if both the x and y ranges of the rectangle
        # have overlap. I determine this using an "interval intersection" method,
        x_overlap = interval_intersection(self.ul.x, self.lr.x, r.ul.x, r.lr.x);
        y_overlap = interval_intersection(self.lr.y, self.ul.y, r.lr.y, r.ul.y);
        return (x_overlap and y_overlap);



    # determine the smallest rectangle that circumscribes a circle
    # sides of the rectangle are tangents to circle c
    # takes a circle object c as input and returns a rectangle object
    def rectangle_circumscribe (self, c):
        # this is just the square, centered at the center of c, whose side
        # length is the diameter of c.

        # We define ul and lr relative to the center of c.
        ul_x = c.center.x - c.radius;
        ul_y = c.center.y + c.radius;
        lr_x = c.center.x + c.radius;
        lr_y = c.center.y - c.radius;

        return Rectangle(ul_x, ul_y, lr_x, lr_y);

    # give string representation of a rectangle
    # takes no arguments, returns a string
    def __str__ (self):
        return "UL: " + str(self.ul) + ", LR: " + str(self.lr)

    # determine if two rectangles have the same length and width
    # takes a rectangle other as argument and returns a boolean
    def __eq__ (self, other):
        same_length = is_equal(self.length(), other.length());
        same_width = is_equal(self.width(), other.width());

        return (same_length and same_width);



def read_point(File):
    # First, read a line and then split it by spaces. The first two
    # components of the resulting list should be our numbers
    words = (File.readline()).split(" ");
    point_coords = words[0:2];
    return Point(float(point_coords[0]), float(point_coords[1]));

def read_circle(File):
    # First read a line and split it by spaces. The first 3 components of the
    # resulting list should be the radius and center coordinates
    words = (File.readline()).split(" ");
    radius_and_center = words[0:3];
    return Circle(float(radius_and_center[0]), float(radius_and_center[1]), float(radius_and_center[2]));

def read_rectangle(File):
    # Read a lit and split it by spaces. The first 4 components of the resulting
    # list should be the coordinates of the upper left and lower right corners
    words = (File.readline()).split(" ");
    coords = words[0:4];
    return Rectangle(float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3]));



def main():
    # open the file geom.txt
    File = open("geom.txt","r");

    # create Point objects P and Q
    P = read_point(File);
    Q = read_point(File);

    # print the coordinates of the points P and Q
    print("Coordinates of P: ", P);
    print("Coordinates of Q: ", Q);

    # find the distance between the points P and Q
    print("Distance between P and Q: %f" % P.dist(Q));

    # create two Circle objects C and D
    C = read_circle(File);
    D = read_circle(File);

    # print C and D
    print("Circle C: ", C);
    print("Circle D: ", D);

    # compute the circumference of C
    print("Circumference of C: %f" % C.circumference());

    # compute the area of D
    print("Area of D: %f" % D.area());

    # determine if P is strictly inside C
    print("P " + ("is " if (C.point_inside(P)) else "is not ") + "inside C");

    # determine if C is strictly inside D
    print("C " + ("is " if (D.circle_inside(C)) else "is not ") + "inside D")

    # determine if C and D intersect (non zero area of intersection)
    print("C " + ("does " if (C.circle_overlap(D)) else "does not ") + "intersect D");

    # determine if C and D are equal (have the same radius)
    print("C " + ("is " if (C==D) else "is not ") + "equal to D");

    # create two rectangle objects G and H
    G = read_rectangle(File);
    H = read_rectangle(File);

    # print the two rectangles G and H
    print("Rectangle G: ", G);
    print("Rectangle H: ", H);

    # determine the length of G (distance along x axis)
    print("Length of G: %.2f" % G.length());

    # determine the width of H (distance along y axis)
    print("Width of H: %.2f" % G.width());

    # determine the perimeter of G
    print("Perimeter of G: %.2f" % G.perimeter());

    # determine the area of H
    print("Area of H: %.2f" % H.area());

    # determine if point P is strictly inside rectangle G
    print("P " + ("is " if (G.point_inside(P)) else "is not ") + "inside G");

    # determine if rectangle G is strictly inside rectangle H
    print("G " + ("is " if (H.rectangle_inside(G)) else "is not ") + "inside H");

    # determine if rectangles G and H overlap (non-zero area of overlap)
    print("G " + ("does " if (H.rectangle_overlap(G)) else "does not ") + "overlap H");

    # find the smallest circle that circumscribes rectangle G
    # goes through the four vertices of the rectangle
    print("Circle that circumscribes G: ", C.circle_circumscribe(G));

    # find the smallest rectangle that circumscribes circle D
    # all four sides of the rectangle are tangents to the circle
    print("Rectangle that circumscribes D: ", G.rectangle_circumscribe(D));

    # determine if the two rectangles have the same length and width
    print("Rectangle G " + ("is " if (G == H) else "is not ") + "equal to H");

    # close the file geom.txt
    File.close();



# This line above main is for grading purposes. It will not affect how
# your code will run while you develop and test it.
# DO NOT REMOVE THE LINE ABOVE MAIN
if __name__ == "__main__":
    main()
