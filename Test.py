import unittest;
from math import pi;
from random import uniform
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
        # Create a circle with a random radius and random center.
        r = uniform(1, 10);
        x = uniform(-5, 5);
        y = uniform(-5, 5);
        C = Circle(r, x, y);

        # Now, create some points and see if they're in the circle
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
        C1 = Circle(2, 0, 0);
        C2 = Circle(1, .5, 0);
        C3 = Circle(1, 1, 0);
        C4 = Circle(3, 0, 0);

        self.assertTrue(C1.circle_inside(C2));
        self.assertFalse(C1.circle_inside(C3));
        self.assertFalse(C1.circle_inside(C4));

    def test_circle_overlap(self):
        C1 = Circle(1, 0, 0);
        C2 = Circle(2, 0, 0);
        C3 = Circle(1, 2, 0);
        C4 = Circle(1.1, 0, 2);

        self.assertFalse(C1.circle_overlap(C2));        # C2 contains C1
        self.assertFalse(C2.circle_overlap(C1));        # C2 contains C1
        self.assertFalse(C1.circle_overlap(C3));        # C1 and C3 only touch at the edge
        self.assertFalse(C3.circle_overlap(C1));        # C1 and C3 only touch at the edge
        self.assertTrue(C1.circle_overlap(C4));         # C1 and C4 overlap a bit
        self.assertTrue(C4.circle_overlap(C1));         # C1 and C4 overlap a bit

    def test_circle_circumscribe(self):
        r = Rectangle(0, 6, 8, 0);
        c = Circle();
        c.circle_circumscribe(r);               # c should now be centered at (4,3) with radius 5

        self.assertEqual(c.radius, 5);
        self.assertEqual(c.center.x, 4);
        self.assertEqual(c.center.y, 3);




if (__name__ == "__main__"):
    unittest.main();
