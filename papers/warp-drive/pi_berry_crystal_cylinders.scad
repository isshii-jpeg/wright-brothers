// π-Berry crystal: CYLINDER VERSION (easier to print)
// Cylindrical channels instead of spherical holes

$fn = 32;

difference() {
    cube([100.0, 100.0, 100.0]);

    // Large channels (r=4.0mm) at unit cell corners
    translate([0.0, 0.0, -1]) cylinder(r=4.0, h=102.0);
    translate([0.0, 20.0, -1]) cylinder(r=4.0, h=102.0);
    translate([0.0, 40.0, -1]) cylinder(r=4.0, h=102.0);
    translate([0.0, 60.0, -1]) cylinder(r=4.0, h=102.0);
    translate([0.0, 80.0, -1]) cylinder(r=4.0, h=102.0);
    translate([0.0, 100.0, -1]) cylinder(r=4.0, h=102.0);
    translate([20.0, 0.0, -1]) cylinder(r=4.0, h=102.0);
    translate([20.0, 20.0, -1]) cylinder(r=4.0, h=102.0);
    translate([20.0, 40.0, -1]) cylinder(r=4.0, h=102.0);
    translate([20.0, 60.0, -1]) cylinder(r=4.0, h=102.0);
    translate([20.0, 80.0, -1]) cylinder(r=4.0, h=102.0);
    translate([20.0, 100.0, -1]) cylinder(r=4.0, h=102.0);
    translate([40.0, 0.0, -1]) cylinder(r=4.0, h=102.0);
    translate([40.0, 20.0, -1]) cylinder(r=4.0, h=102.0);
    translate([40.0, 40.0, -1]) cylinder(r=4.0, h=102.0);
    translate([40.0, 60.0, -1]) cylinder(r=4.0, h=102.0);
    translate([40.0, 80.0, -1]) cylinder(r=4.0, h=102.0);
    translate([40.0, 100.0, -1]) cylinder(r=4.0, h=102.0);
    translate([60.0, 0.0, -1]) cylinder(r=4.0, h=102.0);
    translate([60.0, 20.0, -1]) cylinder(r=4.0, h=102.0);
    translate([60.0, 40.0, -1]) cylinder(r=4.0, h=102.0);
    translate([60.0, 60.0, -1]) cylinder(r=4.0, h=102.0);
    translate([60.0, 80.0, -1]) cylinder(r=4.0, h=102.0);
    translate([60.0, 100.0, -1]) cylinder(r=4.0, h=102.0);
    translate([80.0, 0.0, -1]) cylinder(r=4.0, h=102.0);
    translate([80.0, 20.0, -1]) cylinder(r=4.0, h=102.0);
    translate([80.0, 40.0, -1]) cylinder(r=4.0, h=102.0);
    translate([80.0, 60.0, -1]) cylinder(r=4.0, h=102.0);
    translate([80.0, 80.0, -1]) cylinder(r=4.0, h=102.0);
    translate([80.0, 100.0, -1]) cylinder(r=4.0, h=102.0);
    translate([100.0, 0.0, -1]) cylinder(r=4.0, h=102.0);
    translate([100.0, 20.0, -1]) cylinder(r=4.0, h=102.0);
    translate([100.0, 40.0, -1]) cylinder(r=4.0, h=102.0);
    translate([100.0, 60.0, -1]) cylinder(r=4.0, h=102.0);
    translate([100.0, 80.0, -1]) cylinder(r=4.0, h=102.0);
    translate([100.0, 100.0, -1]) cylinder(r=4.0, h=102.0);

    // Small channels (r=3.0mm) at body-center
    translate([10.0, 10.0, -1]) cylinder(r=3.0, h=102.0);
    translate([10.0, 30.0, -1]) cylinder(r=3.0, h=102.0);
    translate([10.0, 50.0, -1]) cylinder(r=3.0, h=102.0);
    translate([10.0, 70.0, -1]) cylinder(r=3.0, h=102.0);
    translate([10.0, 90.0, -1]) cylinder(r=3.0, h=102.0);
    translate([30.0, 10.0, -1]) cylinder(r=3.0, h=102.0);
    translate([30.0, 30.0, -1]) cylinder(r=3.0, h=102.0);
    translate([30.0, 50.0, -1]) cylinder(r=3.0, h=102.0);
    translate([30.0, 70.0, -1]) cylinder(r=3.0, h=102.0);
    translate([30.0, 90.0, -1]) cylinder(r=3.0, h=102.0);
    translate([50.0, 10.0, -1]) cylinder(r=3.0, h=102.0);
    translate([50.0, 30.0, -1]) cylinder(r=3.0, h=102.0);
    translate([50.0, 50.0, -1]) cylinder(r=3.0, h=102.0);
    translate([50.0, 70.0, -1]) cylinder(r=3.0, h=102.0);
    translate([50.0, 90.0, -1]) cylinder(r=3.0, h=102.0);
    translate([70.0, 10.0, -1]) cylinder(r=3.0, h=102.0);
    translate([70.0, 30.0, -1]) cylinder(r=3.0, h=102.0);
    translate([70.0, 50.0, -1]) cylinder(r=3.0, h=102.0);
    translate([70.0, 70.0, -1]) cylinder(r=3.0, h=102.0);
    translate([70.0, 90.0, -1]) cylinder(r=3.0, h=102.0);
    translate([90.0, 10.0, -1]) cylinder(r=3.0, h=102.0);
    translate([90.0, 30.0, -1]) cylinder(r=3.0, h=102.0);
    translate([90.0, 50.0, -1]) cylinder(r=3.0, h=102.0);
    translate([90.0, 70.0, -1]) cylinder(r=3.0, h=102.0);
    translate([90.0, 90.0, -1]) cylinder(r=3.0, h=102.0);
}
