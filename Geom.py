"""File: Geom.py

   Description: Does some basic geometry with points, squares, and circles.

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
        return (is_equal(self.x, other.x)) and (is_equal(self.y, other.y));



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
        # a point is strictly inside of a circle if its distance from the center
        # is less than the radius of the circle.
        return (self.center.dist(p) < self.radius);

    # determine if a circle c is strictly inside self 
    def circle_inside (self, c):
        """ a c is strictly inside of self if every point in c is inside of
        self. Thus, let's consider an arbitrary point in c, x. In particular,
        let's consider how we get from the center of c to x. We could go
        straight to c or we could do it in a two step process: first going
        from the center of self to the center of c and then from the center
        of c to the point x. By the triangle inequality, the distance
        from the center of self to x is less than the sum of the length of the
        two steps. In other words,
            d(self.center, x) <= d(self.center, c.center) + d(c.center, x)
        since x is in c, d(c.center, x) is less than the radius of c,
            d(self.center, x) < d(self.center, c.center) + c.radius
        Note: expression on the right is independent of x. Since x was
        arbitrary chosen, this must hold for all x in c. As long as the sum
        on the right is less than self's radius, we can conclude that every
        point x in c is also in self. """
        distance_between_centers = self.center.dist (c.center);
        return (distance_between_centers + c.radius) < self.radius;

    # determine if a circle c overlaps this circle (non-zero area of overlap)
    # but neither is completely inside the other
    # the only argument c is a Circle object
    # returns a boolean
    def circle_overlap (self, c):
        # First, make sure that neither circle contains the other.
        if(self.circle_inside(c) or c.circle_inside(self)):
            return False;

        # Note: If we've made it here then neither circle (self, c) contains the other.

        """If the two circles overlap, then there exists some point x that is
        strictly inside both self and c. Since x is in self,
                d(x, self.center) < self.radius
       likewise, since x is in c,
                d(x, c.center) < c.raidus
        combining these two inequalities and using the triangle inequality gives,
                d(c.center, self.center) < c.radius + self.radius
        This gives us a criterion for checking if two circles overlap"""
        center_distance = self.center.dist(c.center);
        return (center_distance < (self.radius + c.radius));

    # determine the smallest circle that circumscribes a rectangle
    # the circle goes through all the vertices of the rectangle
    # the only argument, r, is a rectangle object
    def circle_circumscribe (self, r):
        """ This function modifies self (a circle object) to become the
        smallest circle that circumscribes the rectangle r.

        The smallest circle to circumscribe a rectangle is the circle whose
        center is at the center of the rectangle and whose radius is the
        distance to any one of the four corners (they are all equidistance
        from the center).

        The x coordinate of the center of the rectangle is at the average of the
        left and right edge of the rectangle. Likewise, the y coordinate of the
        center is at the average of the top and bottom edge of the rectangle """
        center_x = (r.lr.x + r.ul.x)/2;
        center_y = (r.ul.y + r.lr.y)/2;

        center = Point(center_x, center_y);
        radius = center.dist(r.ul);

        self.center = center;
        self.radius = radius;

    # string representation of a circle
    # takes no arguments and returns a string
    def __str__ (self):
        return "Radius: " + str(self.radius) + ", Center: " + str(self.center)

    # test for equality of radius
    # the only argument, other, is a circle
    # returns a boolean
    def __eq__ (self, other):
        return is_equal(self.radius, other.radius);



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
    # Note: we say that two rectangles do not overlap if one contains the other.
    # takes a rectangle object r as an argument returns a boolean
    def rectangle_overlap (self, r):
        # First, check that neither rectangle contains the other.
        if(self.rectangle_inside(r) or r.rectangle_inside(r)):
            return False;

        # Next, determine if the two rectangles overlap if both the x and y
        # ranges of the rectangle have overlap. I determine this using an
        # "interval intersection" method,
        x_overlap = self._interval_intersection(self.ul.x, self.lr.x, r.ul.x, r.lr.x);
        y_overlap = self._interval_intersection(self.lr.y, self.ul.y, r.lr.y, r.ul.y);

        return (x_overlap and y_overlap);

    # Find the intersection of two intervals. This is used to help the rectangle
    # overlap function (and thus is private)
    def _interval_intersection(self, a1, b1, a2, b2):
        """This function determines if the two intervals (a1, b1), (a2, b2)
        intersect.

        If max(a1, a2) < min[b1, b2] then they intersect. """
        a = max(a1, a2);
        b = min(b1, b2);

        if (a < b):
            return True;
        else:
            return False;

    # determine the smallest rectangle that circumscribes a circle
    # sides of the rectangle are tangents to circle c
    # takes a circle object c as input and returns a rectangle object
    def rectangle_circumscribe(self, c):
        """ This function modifies self to become the smallest rectangle that
        circumscribes circle c

        this is just the square, centered at the center of c, whose side
        length is the diameter of c. """

        # We define ul and lr relative to the center of c.
        ul_x = c.center.x - c.radius;
        ul_y = c.center.y + c.radius;
        lr_x = c.center.x + c.radius;
        lr_y = c.center.y - c.radius;

        self.ul = Point(ul_x, ul_y);
        self.lr = Point(lr_x, lr_y);

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
    print("C " + ("is " if (C == D) else "is not ") + "equal to D");

    # create two rectangle objects G and H
    G = read_rectangle(File);
    H = read_rectangle(File);

    # print the two rectangles G and H
    print("Rectangle G: ", G);
    print("Rectangle H: ", H);

    # determine the length of G (distance along x axis)
    print("Length of G: %.2f" % G.length());

    # determine the width of H (distance along y axis)
    print("Width of H: %.2f" % H.width());

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
    G_circum = Circle()
    G_circum.circle_circumscribe(G);
    print("Circle that circumscribes G: ", G_circum);

    # find the smallest rectangle that circumscribes circle D
    # all four sides of the rectangle are tangents to the circle
    D_circum = Rectangle();
    D_circum.rectangle_circumscribe(D);
    print("Rectangle that circumscribes D: ", D_circum);

    # determine if the two rectangles have the same length and width
    print("Rectangle G " + ("is " if (G == H) else "is not ") + "equal to H");

    # close the file geom.txt
    File.close();



# This line above main is for grading purposes. It will not affect how
# your code will run while you develop and test it.
# DO NOT REMOVE THE LINE ABOVE MAIN
if __name__ == "__main__":
    main()
