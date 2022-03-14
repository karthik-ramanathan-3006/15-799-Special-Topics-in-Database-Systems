#!/bin/bash
source ~/project/bin/activate;
# Beginning of sampling 1
doit create_index --table sessions -c id -c source_id -c agent;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 180 --rate 17 -i sessions_id_source_id_agent
doit drop_index --table sessions -c id -c source_id -c agent;

# End of sampling 1


# Beginning of sampling 2
doit create_index --table sources -c name;
doit create_index --table types -c id;
doit create_index --table observations -c source_id -c type_id;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 210 --rate 5689 -i sources_name -i types_id -i observations_source_id_type_id
doit drop_index --table sources -c name;
doit drop_index --table types -c id;
doit drop_index --table observations -c source_id -c type_id;

# End of sampling 2


# Beginning of sampling 3
doit create_index --table types -c value_type;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 120 --rate 109 -i types_value_type
doit drop_index --table types -c value_type;

# End of sampling 3


# Beginning of sampling 4
doit create_index --table types -c id -c name;
doit create_index --table observations -c id -c type_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 60 --rate 20 -i types_id_name -i observations_id_type_id_created_time
doit drop_index --table types -c id -c name;
doit drop_index --table observations -c id -c type_id -c created_time;

# End of sampling 4


# Beginning of sampling 5
doit create_index --table sources -c id;
doit create_index --table types -c id -c category -c name;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 60 --rate 2442 -i sources_id -i types_id_category_name
doit drop_index --table sources -c id;
doit drop_index --table types -c id -c category -c name;

# End of sampling 5


# Beginning of sampling 6
doit create_index --table types -c id -c value_type -c name;
doit create_index --table observations -c session_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 240 --rate 1048 -i types_id_value_type_name -i observations_session_id_created_time
doit drop_index --table types -c id -c value_type -c name;
doit drop_index --table observations -c session_id -c created_time;

# End of sampling 6


# Beginning of sampling 7
doit create_index --table sources -c created_time;
doit create_index --table sessions -c agent;
doit create_index --table observations -c source_id;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 60 --rate 167 -i sources_created_time -i sessions_agent -i observations_source_id
doit drop_index --table sources -c created_time;
doit drop_index --table sessions -c agent;
doit drop_index --table observations -c source_id;

# End of sampling 7


# Beginning of sampling 8
doit create_index --table sources -c created_time;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 120 --rate 4291 -i sources_created_time
doit drop_index --table sources -c created_time;

# End of sampling 8


# Beginning of sampling 9
doit create_index --table sources -c created_time;
doit create_index --table types -c value_type -c name;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 150 --rate 1389 -i sources_created_time -i types_value_type_name
doit drop_index --table sources -c created_time;
doit drop_index --table types -c value_type -c name;

# End of sampling 9


# Beginning of sampling 10
doit create_index --table types -c id -c value_type;
doit create_index --table sessions -c id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 60 --rate 11 -i types_id_value_type -i sessions_id_created_time
doit drop_index --table types -c id -c value_type;
doit drop_index --table sessions -c id -c created_time;

# End of sampling 10


# Beginning of sampling 11
doit create_index --table sources -c name -c created_time;
doit create_index --table types -c id -c name;
doit create_index --table sessions -c created_time;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 90 --rate 3727 -i sources_name_created_time -i types_id_name -i sessions_created_time
doit drop_index --table sources -c name -c created_time;
doit drop_index --table types -c id -c name;
doit drop_index --table sessions -c created_time;

# End of sampling 11


# Beginning of sampling 12
doit create_index --table sessions -c agent -c created_time;
doit create_index --table observations -c source_id -c type_id;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 90 --rate 47 -i sessions_agent_created_time -i observations_source_id_type_id
doit drop_index --table sessions -c agent -c created_time;
doit drop_index --table observations -c source_id -c type_id;

# End of sampling 12


# Beginning of sampling 13
doit create_index --table sources -c name -c created_time;
doit create_index --table types -c value_type;
doit create_index --table observations -c source_id -c session_id -c type_id;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 270 --rate 449 -i sources_name_created_time -i types_value_type -i observations_source_id_session_id_type_id
doit drop_index --table sources -c name -c created_time;
doit drop_index --table types -c value_type;
doit drop_index --table observations -c source_id -c session_id -c type_id;

# End of sampling 13


# Beginning of sampling 14
doit create_index --table sources -c id -c name -c created_time;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 300 --rate 1842 -i sources_id_name_created_time
doit drop_index --table sources -c id -c name -c created_time;

# End of sampling 14


# Beginning of sampling 15
doit create_index --table sources -c name;
doit create_index --table types -c id -c category -c name;
doit create_index --table sessions -c id -c created_time;
doit create_index --table observations -c type_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 120 --rate 23 -i sources_name -i types_id_category_name -i sessions_id_created_time -i observations_type_id_created_time
doit drop_index --table sources -c name;
doit drop_index --table types -c id -c category -c name;
doit drop_index --table sessions -c id -c created_time;
doit drop_index --table observations -c type_id -c created_time;

# End of sampling 15


# Beginning of sampling 16
doit create_index --table types -c id -c value_type -c name;
doit create_index --table sessions -c id -c agent -c created_time;
doit create_index --table observations -c source_id -c id -c value;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 210 --rate 1599 -i types_id_value_type_name -i sessions_id_agent_created_time -i observations_source_id_id_value
doit drop_index --table types -c id -c value_type -c name;
doit drop_index --table sessions -c id -c agent -c created_time;
doit drop_index --table observations -c source_id -c id -c value;

# End of sampling 16


# Beginning of sampling 17
doit create_index --table sources -c name -c created_time;
doit create_index --table types -c id -c category;
doit create_index --table sessions -c agent -c created_time;
doit create_index --table observations -c session_id -c type_id;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 90 --rate 390 -i sources_name_created_time -i types_id_category -i sessions_agent_created_time -i observations_session_id_type_id
doit drop_index --table sources -c name -c created_time;
doit drop_index --table types -c id -c category;
doit drop_index --table sessions -c agent -c created_time;
doit drop_index --table observations -c session_id -c type_id;

# End of sampling 17


# Beginning of sampling 18
doit create_index --table sources -c id -c created_time;
doit create_index --table sessions -c source_id -c agent;
doit create_index --table observations -c source_id -c type_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 120 --rate 910 -i sources_id_created_time -i sessions_source_id_agent -i observations_source_id_type_id_created_time
doit drop_index --table sources -c id -c created_time;
doit drop_index --table sessions -c source_id -c agent;
doit drop_index --table observations -c source_id -c type_id -c created_time;

# End of sampling 18


# Beginning of sampling 19
doit create_index --table observations -c source_id;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 210 --rate 145 -i observations_source_id
doit drop_index --table observations -c source_id;

# End of sampling 19


# Beginning of sampling 20
doit create_index --table sources -c id;
doit create_index --table sessions -c agent;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 90 --rate 126 -i sources_id -i sessions_agent
doit drop_index --table sources -c id;
doit drop_index --table sessions -c agent;

# End of sampling 20


# Beginning of sampling 21
doit create_index --table sources -c created_time;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 240 --rate 222 -i sources_created_time
doit drop_index --table sources -c created_time;

# End of sampling 21


# Beginning of sampling 22
doit create_index --table types -c id -c value_type;
doit create_index --table sessions -c created_time;
doit create_index --table observations -c source_id -c type_id -c value;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 270 --rate 10 -i types_id_value_type -i sessions_created_time -i observations_source_id_type_id_value
doit drop_index --table types -c id -c value_type;
doit drop_index --table sessions -c created_time;
doit drop_index --table observations -c source_id -c type_id -c value;

# End of sampling 22


# Beginning of sampling 23
doit create_index --table sources -c id;
doit create_index --table sessions -c id -c agent;
doit create_index --table observations -c id -c session_id -c value;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 210 --rate 8685 -i sources_id -i sessions_id_agent -i observations_id_session_id_value
doit drop_index --table sources -c id;
doit drop_index --table sessions -c id -c agent;
doit drop_index --table observations -c id -c session_id -c value;

# End of sampling 23


# Beginning of sampling 24
doit create_index --table types -c id -c value_type -c name;
doit create_index --table sessions -c id -c source_id -c created_time;
doit create_index --table observations -c session_id -c type_id -c value;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 240 --rate 3237 -i types_id_value_type_name -i sessions_id_source_id_created_time -i observations_session_id_type_id_value
doit drop_index --table types -c id -c value_type -c name;
doit drop_index --table sessions -c id -c source_id -c created_time;
doit drop_index --table observations -c session_id -c type_id -c value;

# End of sampling 24


# Beginning of sampling 25
doit create_index --table sources -c id -c name -c created_time;
doit create_index --table sessions -c id;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 300 --rate 54 -i sources_id_name_created_time -i sessions_id
doit drop_index --table sources -c id -c name -c created_time;
doit drop_index --table sessions -c id;

# End of sampling 25


# Beginning of sampling 26
doit create_index --table observations -c type_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 150 --rate 35 -i observations_type_id_created_time
doit drop_index --table observations -c type_id -c created_time;

# End of sampling 26


# Beginning of sampling 27
doit create_index --table types -c id;
doit create_index --table sessions -c id -c agent;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 180 --rate 13 -i types_id -i sessions_id_agent
doit drop_index --table types -c id;
doit drop_index --table sessions -c id -c agent;

# End of sampling 27


# Beginning of sampling 28
doit create_index --table sessions -c source_id -c agent -c created_time;
doit create_index --table observations -c id -c type_id;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 210 --rate 255 -i sessions_source_id_agent_created_time -i observations_id_type_id
doit drop_index --table sessions -c source_id -c agent -c created_time;
doit drop_index --table observations -c id -c type_id;

# End of sampling 28


# Beginning of sampling 29
doit create_index --table sessions -c source_id -c agent;
doit create_index --table observations -c value;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 240 --rate 10000 -i sessions_source_id_agent -i observations_value
doit drop_index --table sessions -c source_id -c agent;
doit drop_index --table observations -c value;

# End of sampling 29


# Beginning of sampling 30
doit create_index --table sessions -c source_id -c agent;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 180 --rate 15 -i sessions_source_id_agent
doit drop_index --table sessions -c source_id -c agent;

# End of sampling 30


# Beginning of sampling 31
doit create_index --table sources -c name;
doit create_index --table observations -c id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 300 --rate 2120 -i sources_name -i observations_id_created_time
doit drop_index --table sources -c name;
doit drop_index --table observations -c id -c created_time;

# End of sampling 31


# Beginning of sampling 32
doit create_index --table types -c id -c value_type;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 240 --rate 95 -i types_id_value_type
doit drop_index --table types -c id -c value_type;

# End of sampling 32


# Beginning of sampling 33
doit create_index --table sources -c id -c created_time;
doit create_index --table types -c category -c value_type -c name;
doit create_index --table sessions -c id -c source_id -c agent;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 150 --rate 596 -i sources_id_created_time -i types_category_value_type_name -i sessions_id_source_id_agent
doit drop_index --table sources -c id -c created_time;
doit drop_index --table types -c category -c value_type -c name;
doit drop_index --table sessions -c id -c source_id -c agent;

# End of sampling 33


# Beginning of sampling 34
doit create_index --table sources -c id -c name -c created_time;
doit create_index --table types -c id -c value_type -c name;
doit create_index --table sessions -c source_id;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 60 --rate 193 -i sources_id_name_created_time -i types_id_value_type_name -i sessions_source_id
doit drop_index --table sources -c id -c name -c created_time;
doit drop_index --table types -c id -c value_type -c name;
doit drop_index --table sessions -c source_id;

# End of sampling 34


# Beginning of sampling 35
doit create_index --table types -c category;
doit create_index --table observations -c type_id -c value -c created_time;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 120 --rate 686 -i types_category -i observations_type_id_value_created_time
doit drop_index --table types -c category;
doit drop_index --table observations -c type_id -c value -c created_time;

# End of sampling 35


# Beginning of sampling 36
doit create_index --table types -c name;
doit create_index --table observations -c id -c session_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 300 --rate 1206 -i types_name -i observations_id_session_id_created_time
doit drop_index --table types -c name;
doit drop_index --table observations -c id -c session_id -c created_time;

# End of sampling 36


# Beginning of sampling 37
doit create_index --table sources -c name -c created_time;
doit create_index --table observations -c source_id -c value;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 150 --rate 62 -i sources_name_created_time -i observations_source_id_value
doit drop_index --table sources -c name -c created_time;
doit drop_index --table observations -c source_id -c value;

# End of sampling 37


# Beginning of sampling 38
doit create_index --table sessions -c agent;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 270 --rate 517 -i sessions_agent
doit drop_index --table sessions -c agent;

# End of sampling 38


# Beginning of sampling 39
doit create_index --table sources -c id;
doit create_index --table types -c id -c category -c value_type;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 180 --rate 4941 -i sources_id -i types_id_category_value_type
doit drop_index --table sources -c id;
doit drop_index --table types -c id -c category -c value_type;

# End of sampling 39


# Beginning of sampling 40
doit create_index --table sources -c name;
doit create_index --table types -c id -c category;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 150 --rate 790 -i sources_name -i types_id_category
doit drop_index --table sources -c name;
doit drop_index --table types -c id -c category;

# End of sampling 40


# Beginning of sampling 41
doit create_index --table types -c category -c value_type -c name;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 300 --rate 7543 -i types_category_value_type_name
doit drop_index --table types -c category -c value_type -c name;

# End of sampling 41


# Beginning of sampling 42
doit create_index --table sources -c name -c created_time;
doit create_index --table types -c id -c category -c value_type;
doit create_index --table sessions -c agent -c created_time;
doit create_index --table observations -c source_id -c value -c created_time;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 90 --rate 339 -i sources_name_created_time -i types_id_category_value_type -i sessions_agent_created_time -i observations_source_id_value_created_time
doit drop_index --table sources -c name -c created_time;
doit drop_index --table types -c id -c category -c value_type;
doit drop_index --table sessions -c agent -c created_time;
doit drop_index --table observations -c source_id -c value -c created_time;

# End of sampling 42


# Beginning of sampling 43
doit create_index --table types -c value_type -c name;
doit create_index --table sessions -c id -c source_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 0.01 --time 150 --rate 40 -i types_value_type_name -i sessions_id_source_id_created_time
doit drop_index --table types -c value_type -c name;
doit drop_index --table sessions -c id -c source_id -c created_time;

# End of sampling 43


# Beginning of sampling 44
doit create_index --table sources -c id -c name;
doit create_index --table observations -c source_id -c type_id;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 300 --rate 30 -i sources_id_name -i observations_source_id_type_id
doit drop_index --table sources -c id -c name;
doit drop_index --table observations -c source_id -c type_id;

# End of sampling 44


# Beginning of sampling 45
doit create_index --table sources -c id -c created_time;
doit create_index --table types -c id -c name;
doit create_index --table observations -c type_id;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 60 --rate 6551 -i sources_id_created_time -i types_id_name -i observations_type_id
doit drop_index --table sources -c id -c created_time;
doit drop_index --table types -c id -c name;
doit drop_index --table observations -c type_id;

# End of sampling 45


# Beginning of sampling 46
doit create_index --table observations -c source_id -c session_id -c type_id;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 240 --rate 2811 -i observations_source_id_session_id_type_id
doit drop_index --table observations -c source_id -c session_id -c type_id;

# End of sampling 46


# Beginning of sampling 47
doit create_index --table sessions -c source_id;
doit run_workload --benchmark timeseries --scalefactor 0.1 --time 270 --rate 71 -i sessions_source_id
doit drop_index --table sessions -c source_id;

# End of sampling 47


# Beginning of sampling 48
doit create_index --table sources -c id;
doit create_index --table sessions -c agent;
doit run_workload --benchmark timeseries --scalefactor 10.0 --time 180 --rate 26 -i sources_id -i sessions_agent
doit drop_index --table sources -c id;
doit drop_index --table sessions -c agent;

# End of sampling 48


# Beginning of sampling 49
doit create_index --table types -c category;
doit create_index --table sessions -c id -c source_id;
doit create_index --table observations -c id -c value;
doit run_workload --benchmark timeseries --scalefactor 1.0 --time 150 --rate 294 -i types_category -i sessions_id_source_id -i observations_id_value
doit drop_index --table types -c category;
doit drop_index --table sessions -c id -c source_id;
doit drop_index --table observations -c id -c value;

# End of sampling 49


# Beginning of sampling 50
doit create_index --table sessions -c source_id -c agent;
doit create_index --table observations -c source_id -c session_id -c created_time;
doit run_workload --benchmark timeseries --scalefactor 100.0 --time 270 --rate 82 -i sessions_source_id_agent -i observations_source_id_session_id_created_time
doit drop_index --table sessions -c source_id -c agent;
doit drop_index --table observations -c source_id -c session_id -c created_time;

# End of sampling 50

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



