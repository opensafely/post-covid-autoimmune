# Load library -----------------------------------------------------------------

library(readr)
library(dplyr)

# Specify command arguments ----------------------------------------------------
print('Specify command arguments')

args <- commandArgs(trailingOnly=TRUE)

if(length(args)==0){
  cohort <- "unvax"
} else {
  cohort <- args[[1]]
}

# Load data set ----------------------------------------------------------------
print("Load data sets")

# outcomes data set
print("Load outcomes data set")

input_outcome <- read_csv(paste0("output/input_",cohort,".csv.gz"))

# history outcomes data set
print("Load history outcomes data set")

input_history <- read_csv(paste0("output/input_",cohort,"_history.csv.gz"))

# input_history <- input_history %>%
#   select(-c("index_date_cohort", "end_date_outcome", "end_date_exposure", "cov_cat_sex", "vax_date_covid_1", 
#             "tmp_exp_date_covid19_confirmed_sgss", "tmp_exp_date_covid19_confirmed_snomed", "tmp_exp_date_covid19_confirmed_hes", "tmp_exp_date_covid19_confirmed_death",  
#             "dereg_date", "sub_date_covid19_hospital", "vax_jcvi_age_1", "vax_jcvi_age_2", "vax_cat_jcvi_group", "vax_date_eligible", "has_follow_up_previous_6months", "has_died", 
#             "registered_at_start", "tmp_sub_bin_covid19_confirmed_history_sgss", "tmp_sub_bin_covid19_confirmed_history_snomed", "tmp_sub_bin_covid19_confirmed_history_hes", 
#             "exp_date_covid19_confirmed", "sub_bin_covid19_confirmed_history"))

input_history <- input_history %>%
  select(matches("patient_id|^cov_bin_history_"))
  

# merge data sets --------------------------------------------------------------
print("Merge data sets")

input <- inner_join(input_outcome, input_history, 
               by = c("patient_id"))#, "index_date_cohort", "end_date_outcome", "end_date_exposure", "cov_cat_sex", "vax_date_covid_1", 
                  # "tmp_exp_date_covid19_confirmed_sgss", "tmp_exp_date_covid19_confirmed_snomed", "tmp_exp_date_covid19_confirmed_hes", "tmp_exp_date_covid19_confirmed_death",
                  # "dereg_date", "sub_date_covid19_hospital", "vax_jcvi_age_1", "vax_jcvi_age_2", "vax_cat_jcvi_group", "vax_date_eligible", "has_follow_up_previous_6months", "has_died",
                  # "registered_at_start", "tmp_sub_bin_covid19_confirmed_history_sgss", "tmp_sub_bin_covid19_confirmed_history_snomed", "tmp_sub_bin_covid19_confirmed_history_hes",
                  # "exp_date_covid19_confirmed", "sub_bin_covid19_confirmed_history")) #left_join

# merge(input_outcome, input_history, 
#            by = c("patient_id"))

rm(input_outcome, input_history)

# Save -------------------------------------------------------------------------
print("Save final data set")

#saveRDS(input, file = paste0("output/input_",cohort,"_final.csv.gz"), compress = "gzip")

write_csv(input, paste0("output/input_",cohort,"_final.csv.gz"))