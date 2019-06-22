import unittest;
from math import pi;
from Geom import Point, Circle, Rectangle;

class PointTests(unittest.TestCase):
    def test_dist(self):
        # First, create some Points
        P1 = Point(0,0);
        P2 = Point(3,4);

        # Now, test that the distance between them is what we expect
        self.assertEqual(P1.dist(P2), 5);

    def test_equal(self):
        # Create two points.
        P1 = Point(3,7.0);
        P2 = Point(3.0,7);

        # Make sure they are equal
        self.assertEqual(P1,P2);

class CircleTests(unittest.TestCase):
    def test_circum(self):
        # First, create a cricle. Then, check that it has the correct circumfrence
        C1 = Circle(1.0, 0, 0);
        C2 = Circle(2, 4.2, 3.0293);

        self.assertEqual(C1.circumference(), 2*pi);
        self.assertEqual(C2.circumference(), 4*pi);

    def test_area(self):
        # Create some circles, see that we get the correct area.
        C1 = Circle(1.0, 0,0);
        C2 = Circle(4.23, 5.2, 392.30);

        tol = 1e-14;

        C1_diff = abs(C1.area() - pi);
        self.assertLess(C1_diff, tol);

        C2_diff = abs(C2.area() - pi*(4.23*4.23));
        self.assertLess(C2_diff, tol);

    def test_point_inside(self):
        # A point is strictly inside of a circle if the distance from it to the
        # center of the circle is less than the radius of the circle
        r = 1
        x = .5
        y = .5
        C = Circle(r, x, y);

        P1 = Point(x-2*r, y);                   # To the left of the circle
        P2 = Point(x-r, y);                     # On the left edge of the circle
        P3 = Point(x - r*.99, y);               # Barely inside of the circle
        P4 = Point(x-r*.25,y+r*.25);            # Inside of the circle
        P5 = Point(x, y + .99*r);               # Barely inside of the circle
        P6 = Point(x, y + r);                   # On the top edge of the circle.
        P7 = Point(x, y + 2*r);                 # Above the circle

        self.assertFalse(C.point_inside(P1));
        self.assertFalse(C.point_inside(P2));
        self.assertTrue(C.point_inside(P3));
        self.assertTrue(C.point_inside(P4));
        self.assertTrue(C.point_inside(P5));
        self.assertFalse(C.point_inside(P6));
        self.assertFalse(C.point_inside(P7));

    def test_circle_inside(self):
        # a circle c1 circle is strictly inside another circle c2 if the radius
        # of c2 is greater than the sum of the radius of c1 and the distance
        # from the center of c1 to the center of c2.
        C1 = Circle(2, 0, 0);
        C2 = Circle(1, .5, 0);
        C3 = Circle(1, 1, 0);
        C4 = Circle(3, 0, 0);

        self.assertFalse(C1.circle_inside(C1));     # A circle is not inside itself
        self.assertTrue(C1.circle_inside(C2));
        self.assertFalse(C1.circle_inside(C3));
        self.assertFalse(C1.circle_inside(C4));

    def test_circle_overlap(self):
        # two circles overlap if there is at least one point that is in strictly
        # inside both circles but neither circle contains ther other
        C1 = Circle(1, 0, 0);
        C2 = Circle(2, 0, 0);
        C3 = Circle(1, 2, 0);
        C4 = Circle(1.1, 0, 2);

        # self.assertFalse(C1.circle_overlap(C1));        # a circle does not overlap itself
        self.assertFalse(C1.circle_overlap(C2));        # C2 contains C1
        self.assertFalse(C2.circle_overlap(C1));        # C2 contains C1
        self.assertFalse(C1.circle_overlap(C3));        # C1 and C3 only touch at the edge
        self.assertFalse(C3.circle_overlap(C1));        # C1 and C3 only touch at the edge
        self.assertTrue(C1.circle_overlap(C4));         # C1 and C4 overlap a bit
        self.assertTrue(C4.circle_overlap(C1));         # C1 and C4 overlap a bit

    def test_circle_circumscribe(self):
        # the circle circumscribe method should return the smallest circle that
        # encloses a rectangle r.
        r = Rectangle(0, 6, 8, 0);
        c = Circle();
        c.circle_circumscribe(r);               # c should now be centered at (4,3) with radius 5

        self.assertEqual(c.radius, 5);
        self.assertEqual(c.center.x, 4);
        self.assertEqual(c.center.y, 3);

    def test_equal(self):
        # Two circles are equal if their radii are the same.
        C1 = Circle(1, 0, 0);
        C2 = Circle(1, 1.2, 1.292);
        C3 = Circle(1.1, 0, 0);

        self.assertTrue(C1 == C1);
        self.assertTrue(C1 == C2);
        self.assertFalse(C1 == C3);


class RectangleTests(unittest.TestCase):
    def test_length_width(self):
        R1 = Rectangle(0, 3, 4, 0);
        self.assertEqual(R1.length(), 4);
        self.assertEqual(R1.width(), 3);

        R2 = Rectangle(1.4, 1.2, 2.3, -.3);
        self.assertEqual(R2.length(), 2.3 - 1.4);
        self.assertEqual(R2.width(), 1.2 -(-.3));

    def test_perimeter(self):
        R1 = Rectangle(0, 2, 5, 0);
        R2 = Rectangle(-1.1, 2.5, 1.3, -3.2);

        self.assertEqual(R1.perimeter(), 14);
        self.assertEqual(R2.perimeter(), 2*(1.3-(-1.1)) + 2*(2.5 - (-3.2)));

    def test_area(self):
        R1 = Rectangle(0, 4, 5, 0);
        R2 = Rectangle(.1, 1.1, 1.1, .1);

        self.assertEqual(R1.area(), 20);
        self.assertEqual(R2.area(), 1);

    def test_point_inside(self):
        # A point is inside of a rectangle if is strictly inside both the
        # x and y domain of the rectangle
        R1 = Rectangle(0, 1, 1, 0);

        P1 = Point(-.5,.5);             # Left of the Rectangle.
        P2 = Point(0,.5);               # Left edge of the Rectangle
        P3 = Point(.01, .5);            # Just inside the rectangle.
        P4 = Point(.5, .5);             # Inside the rectangle.
        P5 = Point(.5, .99);            # Just inside the rectangle.
        P6 = Point(.5, 1);              # Top edge of the rectangle.
        P7 = Point(.5, 1.5);            # Above the Rectangle.

        self.assertFalse(R1.point_inside(P1));
        self.assertFalse(R1.point_inside(P2));
        self.assertTrue(R1.point_inside(P3));
        self.assertTrue(R1.point_inside(P4));
        self.assertTrue(R1.point_inside(P5));
        self.assertFalse(R1.point_inside(P6));
        self.assertFalse(R1.point_inside(P7));

    def test_rectangle_inside(self):
        # A rectangle r1 is said to be inside of another one r2 if every point
        # in r1 is strictly inside r2. This means that both the upper left
        # and the lower right corners of r2 are inside of r1.
        R1 = Rectangle(.5, 1.5, 1.5, .5);
        R2 = Rectangle(.7, 1.3, 1.3, .7);      # Should be in R1
        R3 = Rectangle(0, 1, 1, 0);             # Overlaps with R1 but not inside

        self.assertFalse(R1.rectangle_inside(R1));      # edges of R1 are not in itself
        self.assertTrue(R1.rectangle_inside(R2));
        self.assertFalse(R1.rectangle_inside(R3));


    def test_rectangle_overlap(self):
        # Two rectangles overlap if there is at least one point in both of them
        # and neither rectangle contains the other
        R1 = Rectangle(0, 1, 1, 0);
        R2 = Rectangle(.2, .8, .8, .2);     # Inside of R1
        R3 = Rectangle(.2, 1.2, .8, -.2);   # overlaps R1
        R4 = Rectangle(0, 1.5, 1, .5);      # Overlaps R1
        R5 = Rectangle(.5, 1.5, 1.5, .5);   # Overlaps R1
        R6 = Rectangle(1, 1, 2, 0);         # Touches but does not overlap R1
        R7 = Rectangle(3, 1, 4, 0);         # Does not overlap R1.

        # self.assertFalse(R1.rectangle_overlap(R1));  # A rectangle does not contain itself
        self.assertFalse(R1.rectangle_overlap(R2)); # R1 contains R2
        self.assertFalse(R2.rectangle_overlap(R1)); # R1 contains R2
        self.assertTrue(R1.rectangle_overlap(R3));  # R3 and R1 overlap
        self.assertTrue(R3.rectangle_overlap(R1));  # R3 and R1 overlap
        self.assertTrue(R1.rectangle_overlap(R4));  # R4 and R1 overlap
        self.assertTrue(R5.rectangle_overlap(R1));  # R5 and R1 overlap
        self.assertFalse(R1.rectangle_overlap(R6)); # R6 touches but does not overlap R1
        self.assertFalse(R6.rectangle_overlap(R1)); # R6 touches but does not overlap R1
        self.assertFalse(R1.rectangle_overlap(R7)); # R7 and R1 do not overlap

    def test_rectangle_circumscribe(self):
        # the rectangle_circumscribe method should modify the self parameter
        # to become the smallest rectangle that contains the circle. This is
        # a square whose side length is the diameter of the circle and whose
        # center is at the center of the circle.
        C = Circle(2, 1, 0);
        R = Rectangle();
        R.rectangle_circumscribe(C);

        self.assertEqual(R.ul.x, -1);
        self.assertEqual(R.ul.y, 2);
        self.assertEqual(R.lr.x, 3);
        self.assertEqual(R.lr.y, -2);

    def test_equal(self):
        # Two rectangles are said to be equal if their length and width are the
        # same
        R1 = Rectangle(0, 1, 1, 0);
        R2 = Rectangle(5, -3, 6, -4);
        R3 = Rectangle(0, 1, 1, -.1);
        R4 = Rectangle(0, 1, 1.1, 0);

        self.assertTrue(R1 == R1);
        self.assertTrue(R1 == R2);
        self.assertFalse(R1 == R3);
        self.assertFalse(R1 == R4);



if (__name__ == "__main__"):
    unittest.main();
