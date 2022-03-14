#!/bin/bash
source ~/project/bin/activate;
# Beginning of sampling 1
doit create_index --table jungle -c int_field8 -c varchar_field0 -c varchar_field9;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 300 --rate 6551 -i jungle_int_field8_varchar_field0_varchar_field9
doit drop_index --table jungle -c int_field8 -c varchar_field0 -c varchar_field9;

# End of sampling 1


# Beginning of sampling 2
doit create_index --table jungle -c float_field5 -c timestamp_field3 -c timestamp_field4;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 240 --rate 1206 -i jungle_float_field5_timestamp_field3_timestamp_field4
doit drop_index --table jungle -c float_field5 -c timestamp_field3 -c timestamp_field4;

# End of sampling 2


# Beginning of sampling 3
doit create_index --table jungle -c uuid_field -c float_field8 -c timestamp_field0;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 150 --rate 26 -i jungle_uuid_field_float_field8_timestamp_field0
doit drop_index --table jungle -c uuid_field -c float_field8 -c timestamp_field0;

# End of sampling 3


# Beginning of sampling 4
doit create_index --table jungle -c varchar_field4 -c timestamp_field2 -c timestamp_field6;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 210 --rate 2442 -i jungle_varchar_field4_timestamp_field2_timestamp_field6
doit drop_index --table jungle -c varchar_field4 -c timestamp_field2 -c timestamp_field6;

# End of sampling 4


# Beginning of sampling 5
doit create_index --table jungle -c int_field2 -c int_field9 -c timestamp_field9;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 60 --rate 222 -i jungle_int_field2_int_field9_timestamp_field9
doit drop_index --table jungle -c int_field2 -c int_field9 -c timestamp_field9;

# End of sampling 5


# Beginning of sampling 6
doit create_index --table jungle -c int_field4 -c float_field9 -c timestamp_field3;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 270 --rate 3727 -i jungle_int_field4_float_field9_timestamp_field3
doit drop_index --table jungle -c int_field4 -c float_field9 -c timestamp_field3;

# End of sampling 6


# Beginning of sampling 7
doit create_index --table jungle -c varchar_field2 -c timestamp_field2 -c timestamp_field4;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 120 --rate 1389 -i jungle_varchar_field2_timestamp_field2_timestamp_field4
doit drop_index --table jungle -c varchar_field2 -c timestamp_field2 -c timestamp_field4;

# End of sampling 7


# Beginning of sampling 8
doit create_index --table jungle -c int_field7 -c float_field3 -c varchar_field3;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 240 --rate 40 -i jungle_int_field7_float_field3_varchar_field3
doit drop_index --table jungle -c int_field7 -c float_field3 -c varchar_field3;

# End of sampling 8


# Beginning of sampling 9
doit create_index --table jungle -c uuid_field -c float_field2 -c timestamp_field5;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 270 --rate 4291 -i jungle_uuid_field_float_field2_timestamp_field5
doit drop_index --table jungle -c uuid_field -c float_field2 -c timestamp_field5;

# End of sampling 9


# Beginning of sampling 10
doit create_index --table jungle -c int_field5 -c float_field4 -c varchar_field1;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 180 --rate 10 -i jungle_int_field5_float_field4_varchar_field1
doit drop_index --table jungle -c int_field5 -c float_field4 -c varchar_field1;

# End of sampling 10


# Beginning of sampling 11
doit create_index --table jungle -c int_field6 -c int_field9 -c timestamp_field5;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 300 --rate 54 -i jungle_int_field6_int_field9_timestamp_field5
doit drop_index --table jungle -c int_field6 -c int_field9 -c timestamp_field5;

# End of sampling 11


# Beginning of sampling 12
doit create_index --table jungle -c int_field9 -c varchar_field5 -c varchar_field9;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 210 --rate 1599 -i jungle_int_field9_varchar_field5_varchar_field9
doit drop_index --table jungle -c int_field9 -c varchar_field5 -c varchar_field9;

# End of sampling 12


# Beginning of sampling 13
doit create_index --table jungle -c int_field5 -c float_field7 -c timestamp_field9;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 150 --rate 517 -i jungle_int_field5_float_field7_timestamp_field9
doit drop_index --table jungle -c int_field5 -c float_field7 -c timestamp_field9;

# End of sampling 13


# Beginning of sampling 14
doit create_index --table jungle -c int_field4 -c int_field8 -c varchar_field7;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 120 --rate 17 -i jungle_int_field4_int_field8_varchar_field7
doit drop_index --table jungle -c int_field4 -c int_field8 -c varchar_field7;

# End of sampling 14


# Beginning of sampling 15
doit create_index --table jungle -c varchar_field2 -c varchar_field4 -c varchar_field7;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 210 --rate 449 -i jungle_varchar_field2_varchar_field4_varchar_field7
doit drop_index --table jungle -c varchar_field2 -c varchar_field4 -c varchar_field7;

# End of sampling 15


# Beginning of sampling 16
doit create_index --table jungle -c float_field3 -c float_field4;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 90 --rate 15 -i jungle_float_field3_float_field4
doit drop_index --table jungle -c float_field3 -c float_field4;

# End of sampling 16


# Beginning of sampling 17
doit create_index --table jungle -c int_field2 -c float_field4 -c varchar_field1;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 90 --rate 109 -i jungle_int_field2_float_field4_varchar_field1
doit drop_index --table jungle -c int_field2 -c float_field4 -c varchar_field1;

# End of sampling 17


# Beginning of sampling 18
doit create_index --table jungle -c float_field0 -c float_field7 -c varchar_field0;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 240 --rate 339 -i jungle_float_field0_float_field7_varchar_field0
doit drop_index --table jungle -c float_field0 -c float_field7 -c varchar_field0;

# End of sampling 18


# Beginning of sampling 19
doit create_index --table jungle -c float_field7 -c varchar_field2 -c varchar_field4;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 60 --rate 82 -i jungle_float_field7_varchar_field2_varchar_field4
doit drop_index --table jungle -c float_field7 -c varchar_field2 -c varchar_field4;

# End of sampling 19


# Beginning of sampling 20
doit create_index --table jungle -c int_field0 -c varchar_field3 -c varchar_field6;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 270 --rate 2120 -i jungle_int_field0_varchar_field3_varchar_field6
doit drop_index --table jungle -c int_field0 -c varchar_field3 -c varchar_field6;

# End of sampling 20


# Beginning of sampling 21
doit create_index --table jungle -c int_field4 -c float_field3 -c varchar_field5;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 300 --rate 910 -i jungle_int_field4_float_field3_varchar_field5
doit drop_index --table jungle -c int_field4 -c float_field3 -c varchar_field5;

# End of sampling 21


# Beginning of sampling 22
doit create_index --table jungle -c int_field7 -c varchar_field1;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 240 --rate 11 -i jungle_int_field7_varchar_field1
doit drop_index --table jungle -c int_field7 -c varchar_field1;

# End of sampling 22


# Beginning of sampling 23
doit create_index --table jungle -c float_field7 -c varchar_field4 -c timestamp_field4;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 180 --rate 1048 -i jungle_float_field7_varchar_field4_timestamp_field4
doit drop_index --table jungle -c float_field7 -c varchar_field4 -c timestamp_field4;

# End of sampling 23


# Beginning of sampling 24
doit create_index --table jungle -c float_field9 -c varchar_field5 -c timestamp_field5;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 60 --rate 145 -i jungle_float_field9_varchar_field5_timestamp_field5
doit drop_index --table jungle -c float_field9 -c varchar_field5 -c timestamp_field5;

# End of sampling 24


# Beginning of sampling 25
doit create_index --table jungle -c int_field8 -c varchar_field2 -c timestamp_field0;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 90 --rate 193 -i jungle_int_field8_varchar_field2_timestamp_field0
doit drop_index --table jungle -c int_field8 -c varchar_field2 -c timestamp_field0;

# End of sampling 25


# Beginning of sampling 26
doit create_index --table jungle -c float_field5 -c float_field7 -c varchar_field2;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 90 --rate 23 -i jungle_float_field5_float_field7_varchar_field2
doit drop_index --table jungle -c float_field5 -c float_field7 -c varchar_field2;

# End of sampling 26


# Beginning of sampling 27
doit create_index --table jungle -c int_field1 -c int_field7 -c timestamp_field7;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 270 --rate 71 -i jungle_int_field1_int_field7_timestamp_field7
doit drop_index --table jungle -c int_field1 -c int_field7 -c timestamp_field7;

# End of sampling 27


# Beginning of sampling 28
doit create_index --table jungle -c int_field3 -c int_field9 -c varchar_field0;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 150 --rate 3237 -i jungle_int_field3_int_field9_varchar_field0
doit drop_index --table jungle -c int_field3 -c int_field9 -c varchar_field0;

# End of sampling 28


# Beginning of sampling 29
doit create_index --table jungle -c float_field3 -c varchar_field1 -c varchar_field2;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 120 --rate 8685 -i jungle_float_field3_varchar_field1_varchar_field2
doit drop_index --table jungle -c float_field3 -c varchar_field1 -c varchar_field2;

# End of sampling 29


# Beginning of sampling 30
doit create_index --table jungle -c uuid_field -c int_field4;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 150 --rate 5689 -i jungle_uuid_field_int_field4
doit drop_index --table jungle -c uuid_field -c int_field4;

# End of sampling 30


# Beginning of sampling 31
doit create_index --table jungle -c float_field3 -c float_field6 -c varchar_field7;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 210 --rate 2811 -i jungle_float_field3_float_field6_varchar_field7
doit drop_index --table jungle -c float_field3 -c float_field6 -c varchar_field7;

# End of sampling 31


# Beginning of sampling 32
doit create_index --table jungle -c varchar_field2 -c timestamp_field5;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 90 --rate 7543 -i jungle_varchar_field2_timestamp_field5
doit drop_index --table jungle -c varchar_field2 -c timestamp_field5;

# End of sampling 32


# Beginning of sampling 33
doit create_index --table jungle -c float_field2 -c float_field5 -c timestamp_field9;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 150 --rate 126 -i jungle_float_field2_float_field5_timestamp_field9
doit drop_index --table jungle -c float_field2 -c float_field5 -c timestamp_field9;

# End of sampling 33


# Beginning of sampling 34
doit create_index --table jungle -c int_field1 -c float_field5 -c float_field8;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 120 --rate 596 -i jungle_int_field1_float_field5_float_field8
doit drop_index --table jungle -c int_field1 -c float_field5 -c float_field8;

# End of sampling 34


# Beginning of sampling 35
doit create_index --table jungle -c int_field0 -c int_field1 -c timestamp_field4;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 240 --rate 10000 -i jungle_int_field0_int_field1_timestamp_field4
doit drop_index --table jungle -c int_field0 -c int_field1 -c timestamp_field4;

# End of sampling 35


# Beginning of sampling 36
doit create_index --table jungle -c int_field0 -c varchar_field1 -c timestamp_field6;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 90 --rate 62 -i jungle_int_field0_varchar_field1_timestamp_field6
doit drop_index --table jungle -c int_field0 -c varchar_field1 -c timestamp_field6;

# End of sampling 36


# Beginning of sampling 37
doit create_index --table jungle -c float_field4 -c varchar_field4 -c timestamp_field8;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 180 --rate 35 -i jungle_float_field4_varchar_field4_timestamp_field8
doit drop_index --table jungle -c float_field4 -c varchar_field4 -c timestamp_field8;

# End of sampling 37


# Beginning of sampling 38
doit create_index --table jungle -c int_field3 -c float_field9 -c timestamp_field5;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 300 --rate 167 -i jungle_int_field3_float_field9_timestamp_field5
doit drop_index --table jungle -c int_field3 -c float_field9 -c timestamp_field5;

# End of sampling 38


# Beginning of sampling 39
doit create_index --table jungle -c int_field3 -c int_field6 -c float_field7;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 150 --rate 20 -i jungle_int_field3_int_field6_float_field7
doit drop_index --table jungle -c int_field3 -c int_field6 -c float_field7;

# End of sampling 39


# Beginning of sampling 40
doit create_index --table jungle -c int_field1 -c varchar_field9 -c timestamp_field4;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 60 --rate 95 -i jungle_int_field1_varchar_field9_timestamp_field4
doit drop_index --table jungle -c int_field1 -c varchar_field9 -c timestamp_field4;

# End of sampling 40


# Beginning of sampling 41
doit create_index --table jungle -c float_field1 -c timestamp_field3 -c timestamp_field9;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 300 --rate 13 -i jungle_float_field1_timestamp_field3_timestamp_field9
doit drop_index --table jungle -c float_field1 -c timestamp_field3 -c timestamp_field9;

# End of sampling 41


# Beginning of sampling 42
doit create_index --table jungle -c varchar_field7 -c timestamp_field2 -c timestamp_field9;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 180 --rate 30 -i jungle_varchar_field7_timestamp_field2_timestamp_field9
doit drop_index --table jungle -c varchar_field7 -c timestamp_field2 -c timestamp_field9;

# End of sampling 42


# Beginning of sampling 43
doit create_index --table jungle -c uuid_field -c int_field4 -c timestamp_field0;
doit run_workload --benchmark indexjungle --scalefactor 10.0 --time 120 --rate 686 -i jungle_uuid_field_int_field4_timestamp_field0
doit drop_index --table jungle -c uuid_field -c int_field4 -c timestamp_field0;

# End of sampling 43


# Beginning of sampling 44
doit create_index --table jungle -c int_field9 -c float_field5 -c varchar_field5;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 60 --rate 255 -i jungle_int_field9_float_field5_varchar_field5
doit drop_index --table jungle -c int_field9 -c float_field5 -c varchar_field5;

# End of sampling 44


# Beginning of sampling 45
doit create_index --table jungle -c int_field6 -c float_field6 -c float_field8;
doit run_workload --benchmark indexjungle --scalefactor 100.0 --time 210 --rate 294 -i jungle_int_field6_float_field6_float_field8
doit drop_index --table jungle -c int_field6 -c float_field6 -c float_field8;

# End of sampling 45


# Beginning of sampling 46
doit create_index --table jungle -c int_field0 -c int_field9 -c float_field4;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 180 --rate 4941 -i jungle_int_field0_int_field9_float_field4
doit drop_index --table jungle -c int_field0 -c int_field9 -c float_field4;

# End of sampling 46


# Beginning of sampling 47
doit create_index --table jungle -c float_field9 -c timestamp_field1 -c timestamp_field9;
doit run_workload --benchmark indexjungle --scalefactor 1.0 --time 300 --rate 47 -i jungle_float_field9_timestamp_field1_timestamp_field9
doit drop_index --table jungle -c float_field9 -c timestamp_field1 -c timestamp_field9;

# End of sampling 47


# Beginning of sampling 48
doit create_index --table jungle -c int_field7 -c varchar_field2 -c timestamp_field7;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 180 --rate 1842 -i jungle_int_field7_varchar_field2_timestamp_field7
doit drop_index --table jungle -c int_field7 -c varchar_field2 -c timestamp_field7;

# End of sampling 48


# Beginning of sampling 49
doit create_index --table jungle -c int_field6 -c varchar_field3 -c varchar_field5;
doit run_workload --benchmark indexjungle --scalefactor 0.1 --time 270 --rate 790 -i jungle_int_field6_varchar_field3_varchar_field5
doit drop_index --table jungle -c int_field6 -c varchar_field3 -c varchar_field5;

# End of sampling 49


# Beginning of sampling 50
doit create_index --table jungle -c float_field1 -c float_field4 -c varchar_field2;
doit run_workload --benchmark indexjungle --scalefactor 0.01 --time 240 --rate 390 -i jungle_float_field1_float_field4_varchar_field2
doit drop_index --table jungle -c float_field1 -c float_field4 -c varchar_field2;

# End of sampling 50

