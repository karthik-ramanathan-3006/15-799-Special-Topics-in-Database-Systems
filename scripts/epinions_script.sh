#!/bin/bash
source ~/project/bin/activate;
# Beginning of sampling 1
doit create_index --table useracct -c creation_date;
doit create_index --table item -c title -c description;
doit create_index --table review -c a_id -c i_id;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 210 --rate 1048 -i useracct_creation_date -i item_title_description -i review_a_id_i_id
doit drop_index --table useracct -c creation_date;
doit drop_index --table item -c title -c description;
doit drop_index --table review -c a_id -c i_id;

# End of sampling 1


# Beginning of sampling 2
doit create_index --table review -c u_id -c rank -c creation_date;
doit create_index --table review_rating -c u_id -c a_id -c creation_date;
doit create_index --table trust -c target_u_id -c trust;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 90 --rate 17 -i review_u_id_rank_creation_date -i review_rating_u_id_a_id_creation_date -i trust_target_u_id_trust
doit drop_index --table review -c u_id -c rank -c creation_date;
doit drop_index --table review_rating -c u_id -c a_id -c creation_date;
doit drop_index --table trust -c target_u_id -c trust;

# End of sampling 2


# Beginning of sampling 3
doit create_index --table useracct -c name -c creation_date;
doit create_index --table review_rating -c status -c last_mod_date -c vertical_id;
doit create_index --table trust -c trust;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 120 --rate 1206 -i useracct_name_creation_date -i review_rating_status_last_mod_date_vertical_id -i trust_trust
doit drop_index --table useracct -c name -c creation_date;
doit drop_index --table review_rating -c status -c last_mod_date -c vertical_id;
doit drop_index --table trust -c trust;

# End of sampling 3


# Beginning of sampling 4
doit create_index --table useracct -c u_id -c name;
doit create_index --table item -c title -c description;
doit create_index --table review -c a_id -c u_id -c rating;
doit create_index --table review_rating -c a_id -c status;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 150 --rate 2442 -i useracct_u_id_name -i item_title_description -i review_a_id_u_id_rating -i review_rating_a_id_status
doit drop_index --table useracct -c u_id -c name;
doit drop_index --table item -c title -c description;
doit drop_index --table review -c a_id -c u_id -c rating;
doit drop_index --table review_rating -c a_id -c status;

# End of sampling 4


# Beginning of sampling 5
doit create_index --table useracct -c u_id -c name -c email;
doit create_index --table trust -c source_u_id -c target_u_id -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 210 --rate 40 -i useracct_u_id_name_email -i trust_source_u_id_target_u_id_creation_date
doit drop_index --table useracct -c u_id -c name -c email;
doit drop_index --table trust -c source_u_id -c target_u_id -c creation_date;

# End of sampling 5


# Beginning of sampling 6
doit create_index --table item -c i_id -c description -c creation_date;
doit create_index --table trust -c target_u_id -c trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 60 --rate 126 -i item_i_id_description_creation_date -i trust_target_u_id_trust_creation_date
doit drop_index --table item -c i_id -c description -c creation_date;
doit drop_index --table trust -c target_u_id -c trust -c creation_date;

# End of sampling 6


# Beginning of sampling 7
doit create_index --table item -c title -c description -c creation_date;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 270 --rate 35 -i item_title_description_creation_date
doit drop_index --table item -c title -c description -c creation_date;

# End of sampling 7


# Beginning of sampling 8
doit create_index --table review -c u_id -c rank -c creation_date;
doit create_index --table review_rating -c u_id -c rating -c status;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 180 --rate 95 -i review_u_id_rank_creation_date -i review_rating_u_id_rating_status
doit drop_index --table review -c u_id -c rank -c creation_date;
doit drop_index --table review_rating -c u_id -c rating -c status;

# End of sampling 8


# Beginning of sampling 9
doit create_index --table item -c i_id;
doit create_index --table review_rating -c u_id -c a_id;
doit create_index --table trust -c source_u_id -c trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 300 --rate 10 -i item_i_id -i review_rating_u_id_a_id -i trust_source_u_id_trust_creation_date
doit drop_index --table item -c i_id;
doit drop_index --table review_rating -c u_id -c a_id;
doit drop_index --table trust -c source_u_id -c trust -c creation_date;

# End of sampling 9


# Beginning of sampling 10
doit create_index --table review -c a_id -c u_id -c i_id;
doit create_index --table trust -c target_u_id -c trust;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 210 --rate 1842 -i review_a_id_u_id_i_id -i trust_target_u_id_trust
doit drop_index --table review -c a_id -c u_id -c i_id;
doit drop_index --table trust -c target_u_id -c trust;

# End of sampling 10


# Beginning of sampling 11
doit create_index --table useracct -c u_id -c name -c email;
doit create_index --table item -c i_id -c creation_date;
doit create_index --table trust -c source_u_id -c target_u_id -c creation_date;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 240 --rate 7543 -i useracct_u_id_name_email -i item_i_id_creation_date -i trust_source_u_id_target_u_id_creation_date
doit drop_index --table useracct -c u_id -c name -c email;
doit drop_index --table item -c i_id -c creation_date;
doit drop_index --table trust -c source_u_id -c target_u_id -c creation_date;

# End of sampling 11


# Beginning of sampling 12
doit create_index --table item -c i_id -c title -c description;
doit create_index --table review -c a_id -c i_id -c rating;
doit create_index --table review_rating -c rating -c vertical_id;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 90 --rate 339 -i item_i_id_title_description -i review_a_id_i_id_rating -i review_rating_rating_vertical_id
doit drop_index --table item -c i_id -c title -c description;
doit drop_index --table review -c a_id -c i_id -c rating;
doit drop_index --table review_rating -c rating -c vertical_id;

# End of sampling 12


# Beginning of sampling 13
doit create_index --table item -c title -c creation_date;
doit create_index --table review -c a_id -c i_id -c rank;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 210 --rate 54 -i item_title_creation_date -i review_a_id_i_id_rank
doit drop_index --table item -c title -c creation_date;
doit drop_index --table review -c a_id -c i_id -c rank;

# End of sampling 13


# Beginning of sampling 14
doit create_index --table useracct -c u_id -c name -c creation_date;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 60 --rate 13 -i useracct_u_id_name_creation_date
doit drop_index --table useracct -c u_id -c name -c creation_date;

# End of sampling 14


# Beginning of sampling 15
doit create_index --table review -c a_id -c rank -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 120 --rate 8685 -i review_a_id_rank_creation_date
doit drop_index --table review -c a_id -c rank -c creation_date;

# End of sampling 15


# Beginning of sampling 16
doit create_index --table review -c rating -c rank;
doit create_index --table review_rating -c u_id -c last_mod_date;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 240 --rate 11 -i review_rating_rank -i review_rating_u_id_last_mod_date
doit drop_index --table review -c rating -c rank;
doit drop_index --table review_rating -c u_id -c last_mod_date;

# End of sampling 16


# Beginning of sampling 17
doit create_index --table useracct -c u_id -c email;
doit create_index --table item -c title -c description -c creation_date;
doit create_index --table review_rating -c u_id -c last_mod_date -c vertical_id;
doit create_index --table trust -c source_u_id -c target_u_id -c trust;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 300 --rate 2120 -i useracct_u_id_email -i item_title_description_creation_date -i review_rating_u_id_last_mod_date_vertical_id -i trust_source_u_id_target_u_id_trust
doit drop_index --table useracct -c u_id -c email;
doit drop_index --table item -c title -c description -c creation_date;
doit drop_index --table review_rating -c u_id -c last_mod_date -c vertical_id;
doit drop_index --table trust -c source_u_id -c target_u_id -c trust;

# End of sampling 17


# Beginning of sampling 18
doit create_index --table item -c i_id -c title -c description;
doit create_index --table review_rating -c status -c creation_date -c vertical_id;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 270 --rate 109 -i item_i_id_title_description -i review_rating_status_creation_date_vertical_id
doit drop_index --table item -c i_id -c title -c description;
doit drop_index --table review_rating -c status -c creation_date -c vertical_id;

# End of sampling 18


# Beginning of sampling 19
doit create_index --table useracct -c u_id -c name -c email;
doit create_index --table item -c title -c description;
doit create_index --table review -c a_id -c rating;
doit create_index --table review_rating -c u_id -c rating -c last_mod_date;
doit create_index --table trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 240 --rate 910 -i useracct_u_id_name_email -i item_title_description -i review_a_id_rating -i review_rating_u_id_rating_last_mod_date -i trust_creation_date
doit drop_index --table useracct -c u_id -c name -c email;
doit drop_index --table item -c title -c description;
doit drop_index --table review -c a_id -c rating;
doit drop_index --table review_rating -c u_id -c rating -c last_mod_date;
doit drop_index --table trust -c creation_date;

# End of sampling 19


# Beginning of sampling 20
doit create_index --table useracct -c creation_date;
doit create_index --table review -c a_id -c u_id -c rank;
doit create_index --table review_rating -c status;
doit create_index --table trust -c source_u_id;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 270 --rate 15 -i useracct_creation_date -i review_a_id_u_id_rank -i review_rating_status -i trust_source_u_id
doit drop_index --table useracct -c creation_date;
doit drop_index --table review -c a_id -c u_id -c rank;
doit drop_index --table review_rating -c status;
doit drop_index --table trust -c source_u_id;

# End of sampling 20


# Beginning of sampling 21
doit create_index --table item -c title -c description;
doit create_index --table review -c creation_date;
doit create_index --table review_rating -c a_id -c status;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 210 --rate 1599 -i item_title_description -i review_creation_date -i review_rating_a_id_status
doit drop_index --table item -c title -c description;
doit drop_index --table review -c creation_date;
doit drop_index --table review_rating -c a_id -c status;

# End of sampling 21


# Beginning of sampling 22
doit create_index --table useracct -c name -c email -c creation_date;
doit create_index --table item -c i_id -c title -c description;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 180 --rate 3727 -i useracct_name_email_creation_date -i item_i_id_title_description
doit drop_index --table useracct -c name -c email -c creation_date;
doit drop_index --table item -c i_id -c title -c description;

# End of sampling 22


# Beginning of sampling 23
doit create_index --table useracct -c name -c email -c creation_date;
doit create_index --table review -c u_id -c i_id -c rating;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 300 --rate 6551 -i useracct_name_email_creation_date -i review_u_id_i_id_rating
doit drop_index --table useracct -c name -c email -c creation_date;
doit drop_index --table review -c u_id -c i_id -c rating;

# End of sampling 23


# Beginning of sampling 24
doit create_index --table item -c title -c description -c creation_date;
doit create_index --table review -c a_id -c u_id -c rating;
doit create_index --table trust -c source_u_id -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 210 --rate 390 -i item_title_description_creation_date -i review_a_id_u_id_rating -i trust_source_u_id_creation_date
doit drop_index --table item -c title -c description -c creation_date;
doit drop_index --table review -c a_id -c u_id -c rating;
doit drop_index --table trust -c source_u_id -c creation_date;

# End of sampling 24


# Beginning of sampling 25
doit create_index --table item -c title -c creation_date;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 150 --rate 1389 -i item_title_creation_date
doit drop_index --table item -c title -c creation_date;

# End of sampling 25


# Beginning of sampling 26
doit create_index --table useracct -c name -c email -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 300 --rate 167 -i useracct_name_email_creation_date
doit drop_index --table useracct -c name -c email -c creation_date;

# End of sampling 26


# Beginning of sampling 27
doit create_index --table useracct -c u_id -c email -c creation_date;
doit create_index --table review_rating -c status -c creation_date -c vertical_id;
doit create_index --table trust -c target_u_id -c trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 270 --rate 10000 -i useracct_u_id_email_creation_date -i review_rating_status_creation_date_vertical_id -i trust_target_u_id_trust_creation_date
doit drop_index --table useracct -c u_id -c email -c creation_date;
doit drop_index --table review_rating -c status -c creation_date -c vertical_id;
doit drop_index --table trust -c target_u_id -c trust -c creation_date;

# End of sampling 27


# Beginning of sampling 28
doit create_index --table trust -c target_u_id;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 60 --rate 20 -i trust_target_u_id
doit drop_index --table trust -c target_u_id;

# End of sampling 28


# Beginning of sampling 29
doit create_index --table useracct -c u_id -c creation_date;
doit create_index --table trust -c target_u_id -c trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 90 --rate 5689 -i useracct_u_id_creation_date -i trust_target_u_id_trust_creation_date
doit drop_index --table useracct -c u_id -c creation_date;
doit drop_index --table trust -c target_u_id -c trust -c creation_date;

# End of sampling 29


# Beginning of sampling 30
doit create_index --table review_rating -c status -c creation_date;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 90 --rate 4941 -i review_rating_status_creation_date
doit drop_index --table review_rating -c status -c creation_date;

# End of sampling 30


# Beginning of sampling 31
doit create_index --table useracct -c creation_date;
doit create_index --table review -c rank;
doit create_index --table trust -c target_u_id -c creation_date;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 150 --rate 686 -i useracct_creation_date -i review_rank -i trust_target_u_id_creation_date
doit drop_index --table useracct -c creation_date;
doit drop_index --table review -c rank;
doit drop_index --table trust -c target_u_id -c creation_date;

# End of sampling 31


# Beginning of sampling 32
doit create_index --table useracct -c u_id -c email -c creation_date;
doit create_index --table review -c i_id -c rating -c creation_date;
doit create_index --table review_rating -c a_id -c status -c last_mod_date;
doit create_index --table trust -c target_u_id -c trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 60 --rate 71 -i useracct_u_id_email_creation_date -i review_i_id_rating_creation_date -i review_rating_a_id_status_last_mod_date -i trust_target_u_id_trust_creation_date
doit drop_index --table useracct -c u_id -c email -c creation_date;
doit drop_index --table review -c i_id -c rating -c creation_date;
doit drop_index --table review_rating -c a_id -c status -c last_mod_date;
doit drop_index --table trust -c target_u_id -c trust -c creation_date;

# End of sampling 32


# Beginning of sampling 33
doit create_index --table useracct -c u_id;
doit create_index --table item -c title;
doit create_index --table review -c i_id -c rank -c creation_date;
doit create_index --table trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 150 --rate 62 -i useracct_u_id -i item_title -i review_i_id_rank_creation_date -i trust_creation_date
doit drop_index --table useracct -c u_id;
doit drop_index --table item -c title;
doit drop_index --table review -c i_id -c rank -c creation_date;
doit drop_index --table trust -c creation_date;

# End of sampling 33


# Beginning of sampling 34
doit create_index --table item -c i_id -c description -c creation_date;
doit create_index --table review -c u_id -c rank -c creation_date;
doit create_index --table review_rating -c u_id -c rating -c vertical_id;
doit create_index --table trust -c source_u_id -c target_u_id;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 300 --rate 596 -i item_i_id_description_creation_date -i review_u_id_rank_creation_date -i review_rating_u_id_rating_vertical_id -i trust_source_u_id_target_u_id
doit drop_index --table item -c i_id -c description -c creation_date;
doit drop_index --table review -c u_id -c rank -c creation_date;
doit drop_index --table review_rating -c u_id -c rating -c vertical_id;
doit drop_index --table trust -c source_u_id -c target_u_id;

# End of sampling 34


# Beginning of sampling 35
doit create_index --table useracct -c u_id -c email;
doit create_index --table item -c creation_date;
doit create_index --table review -c a_id -c rating -c rank;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 120 --rate 3237 -i useracct_u_id_email -i item_creation_date -i review_a_id_rating_rank
doit drop_index --table useracct -c u_id -c email;
doit drop_index --table item -c creation_date;
doit drop_index --table review -c a_id -c rating -c rank;

# End of sampling 35


# Beginning of sampling 36
doit create_index --table useracct -c name;
doit create_index --table item -c creation_date;
doit create_index --table review -c a_id -c i_id;
doit create_index --table review_rating -c creation_date -c last_mod_date;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 180 --rate 30 -i useracct_name -i item_creation_date -i review_a_id_i_id -i review_rating_creation_date_last_mod_date
doit drop_index --table useracct -c name;
doit drop_index --table item -c creation_date;
doit drop_index --table review -c a_id -c i_id;
doit drop_index --table review_rating -c creation_date -c last_mod_date;

# End of sampling 36


# Beginning of sampling 37
doit create_index --table useracct -c name;
doit create_index --table item -c i_id -c title -c creation_date;
doit create_index --table trust -c source_u_id -c target_u_id -c creation_date;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 60 --rate 449 -i useracct_name -i item_i_id_title_creation_date -i trust_source_u_id_target_u_id_creation_date
doit drop_index --table useracct -c name;
doit drop_index --table item -c i_id -c title -c creation_date;
doit drop_index --table trust -c source_u_id -c target_u_id -c creation_date;

# End of sampling 37


# Beginning of sampling 38
doit create_index --table review -c u_id;
doit create_index --table trust -c source_u_id -c trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 240 --rate 294 -i review_u_id -i trust_source_u_id_trust_creation_date
doit drop_index --table review -c u_id;
doit drop_index --table trust -c source_u_id -c trust -c creation_date;

# End of sampling 38


# Beginning of sampling 39
doit create_index --table item -c i_id -c title -c description;
doit create_index --table review_rating -c last_mod_date;
doit create_index --table trust -c source_u_id -c target_u_id -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 270 --rate 82 -i item_i_id_title_description -i review_rating_last_mod_date -i trust_source_u_id_target_u_id_creation_date
doit drop_index --table item -c i_id -c title -c description;
doit drop_index --table review_rating -c last_mod_date;
doit drop_index --table trust -c source_u_id -c target_u_id -c creation_date;

# End of sampling 39


# Beginning of sampling 40
doit create_index --table useracct -c u_id -c name -c creation_date;
doit create_index --table review -c a_id -c u_id -c rating;
doit create_index --table review_rating -c vertical_id;
doit run_workload --benchmark epinions --scalefactor 100.0 --time 90 --rate 255 -i useracct_u_id_name_creation_date -i review_a_id_u_id_rating -i review_rating_vertical_id
doit drop_index --table useracct -c u_id -c name -c creation_date;
doit drop_index --table review -c a_id -c u_id -c rating;
doit drop_index --table review_rating -c vertical_id;

# End of sampling 40


# Beginning of sampling 41
doit create_index --table useracct -c u_id -c name -c email;
doit create_index --table review_rating -c a_id -c rating -c status;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 180 --rate 790 -i useracct_u_id_name_email -i review_rating_a_id_rating_status
doit drop_index --table useracct -c u_id -c name -c email;
doit drop_index --table review_rating -c a_id -c rating -c status;

# End of sampling 41


# Beginning of sampling 42
doit create_index --table review_rating -c status -c creation_date;
doit create_index --table trust -c trust;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 120 --rate 4291 -i review_rating_status_creation_date -i trust_trust
doit drop_index --table review_rating -c status -c creation_date;
doit drop_index --table trust -c trust;

# End of sampling 42


# Beginning of sampling 43
doit create_index --table useracct -c u_id -c name -c email;
doit create_index --table review_rating -c u_id -c a_id -c vertical_id;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 120 --rate 145 -i useracct_u_id_name_email -i review_rating_u_id_a_id_vertical_id
doit drop_index --table useracct -c u_id -c name -c email;
doit drop_index --table review_rating -c u_id -c a_id -c vertical_id;

# End of sampling 43


# Beginning of sampling 44
doit create_index --table review_rating -c creation_date;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 60 --rate 26 -i review_rating_creation_date
doit drop_index --table review_rating -c creation_date;

# End of sampling 44


# Beginning of sampling 45
doit create_index --table item -c title -c description;
doit create_index --table review -c u_id -c rating -c rank;
doit create_index --table review_rating -c creation_date;
doit create_index --table trust -c source_u_id;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 180 --rate 222 -i item_title_description -i review_u_id_rating_rank -i review_rating_creation_date -i trust_source_u_id
doit drop_index --table item -c title -c description;
doit drop_index --table review -c u_id -c rating -c rank;
doit drop_index --table review_rating -c creation_date;
doit drop_index --table trust -c source_u_id;

# End of sampling 45


# Beginning of sampling 46
doit create_index --table useracct -c creation_date;
doit create_index --table review -c rating -c rank;
doit create_index --table trust -c source_u_id -c target_u_id;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 300 --rate 23 -i useracct_creation_date -i review_rating_rank -i trust_source_u_id_target_u_id
doit drop_index --table useracct -c creation_date;
doit drop_index --table review -c rating -c rank;
doit drop_index --table trust -c source_u_id -c target_u_id;

# End of sampling 46


# Beginning of sampling 47
doit create_index --table useracct -c u_id -c name -c creation_date;
doit create_index --table item -c title -c description -c creation_date;
doit create_index --table review_rating -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.01 --time 150 --rate 517 -i useracct_u_id_name_creation_date -i item_title_description_creation_date -i review_rating_creation_date
doit drop_index --table useracct -c u_id -c name -c creation_date;
doit drop_index --table item -c title -c description -c creation_date;
doit drop_index --table review_rating -c creation_date;

# End of sampling 47


# Beginning of sampling 48
doit create_index --table item -c creation_date;
doit create_index --table review_rating -c a_id -c rating;
doit run_workload --benchmark epinions --scalefactor 1.0 --time 120 --rate 193 -i item_creation_date -i review_rating_a_id_rating
doit drop_index --table item -c creation_date;
doit drop_index --table review_rating -c a_id -c rating;

# End of sampling 48


# Beginning of sampling 49
doit create_index --table useracct -c u_id -c email;
doit create_index --table item -c i_id -c title -c creation_date;
doit create_index --table review -c u_id -c i_id -c rating;
doit create_index --table trust -c source_u_id -c trust -c creation_date;
doit run_workload --benchmark epinions --scalefactor 10.0 --time 210 --rate 47 -i useracct_u_id_email -i item_i_id_title_creation_date -i review_u_id_i_id_rating -i trust_source_u_id_trust_creation_date
doit drop_index --table useracct -c u_id -c email;
doit drop_index --table item -c i_id -c title -c creation_date;
doit drop_index --table review -c u_id -c i_id -c rating;
doit drop_index --table trust -c source_u_id -c trust -c creation_date;

# End of sampling 49


# Beginning of sampling 50
doit create_index --table useracct -c u_id -c email -c creation_date;
doit create_index --table item -c title -c description -c creation_date;
doit run_workload --benchmark epinions --scalefactor 0.1 --time 240 --rate 2811 -i useracct_u_id_email_creation_date -i item_title_description_creation_date
doit drop_index --table useracct -c u_id -c email -c creation_date;
doit drop_index --table item -c title -c description -c creation_date;

# End of sampling 50

