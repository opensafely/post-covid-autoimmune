# Create output directory ------------------------------------------------------

fs::dir_create(here::here("lib"))

# Create empty data frame ------------------------------------------------------

df <- data.frame(cohort = character(),
                 exposure = character(), 
                 outcome = character(), 
                 ipw = logical(), 
                 strata = character(),
                 covariate_sex = character(),
                 covariate_age = character(),
                 covariate_other = character(),
                 cox_start = character(),
                 cox_stop = character(),
                 study_start = character(),
                 study_stop = character(),
                 cut_points = character(),
                 controls_per_case = numeric(),
                 total_event_threshold = numeric(),
                 episode_event_threshold = numeric(),
                 covariate_threshold = numeric(),
                 age_spline = logical(),
                 analysis = character(),
                 stringsAsFactors = FALSE)

# Set constant values ----------------------------------------------------------

ipw <- TRUE
age_spline <- TRUE
exposure <- "exp_date_covid19_confirmed"
strata <- "cov_cat_region"
covariate_sex <- "cov_cat_sex"
covariate_age <- "cov_num_age"
cox_start <- "index_date"
cox_stop <- "end_date_outcome"
controls_per_case <- 20L
total_event_threshold <- 50L
episode_event_threshold <- 5L
covariate_threshold <- 5L
##Dates
study_dates <- fromJSON("output/study_dates.json")

prevax_start <- "2020-01-01"
prevax_stop<- "2021-12-14"
vax_unvax_start<-"2021-06-01"
vax_unvax_stop <-"2021-12-14"
##Cut points 
prevax_cuts <- "1;28;197;365;714"
vax_unvax_cuts <- "1;28;197"

# all_covars <- paste0("cov_cat_ethnicity;cov_cat_deprivation;cov_cat_smoking_status;cov_bin_carehome_status;",
#                      "cov_num_consulation_rate;cov_bin_healthcare_worker;cov_bin_obesity;")

# Specify cohorts --------------------------------------------------------------

cohorts <- c("vax","unvax","prevax")

# Specify outcomes -------------------------------------------------------------

outcomes_runall <- c("out_date_composite_ai",
                     "out_date_grp1_ifa",
                     "out_date_grp2_ctd",
                     "out_date_grp3_isd",
                     "out_date_grp4_agi_ibd",
                     "out_date_grp5_atv",
                     "out_date_grp6_trd",
                     "out_date_grp7_htd",
                     "out_date_grp8_ind",
                     "out_date_ra",
                     "out_date_psoa",#change to psoa/pa
                     "out_date_axial",
                     "out_date_psoriasis",
                     "out_date_hs",
                     "out_date_ibd",
                     "out_date_crohn",
                     "out_date_uc",
                     "out_date_celiac",
                     "out_date_addison",
                     "out_date_grave",
                     "out_date_pmr",
                     "out_date_immune_thromb",
                     "out_date_pern_anaemia",
                     "out_date_apa",
                     "out_date_ms",
                     "out_date_myasthenia"
                     )

outcomes_runmain <- c("out_date_undiff_eia",
                      "out_date_as",
                     "out_date_sle",
                     "out_date_sjs",
                     "out_date_sss",
                     "out_date_im",
                     "out_date_mctd",
                     "out_date_hashimoto",
                     "out_date_anca",
                     "out_date_gca",
                     "out_date_iga_vasc",
                     "out_date_aha",
                     "out_date_glb",
                     "out_date_long_myelitis",
                     "out_date_cis")

#cov_num_outpatient_rate;
#cov_cat_ethnicity;

all_covars <- c("cov_cat_ethnicity;cov_cat_deprivation;cov_num_consulation_rate;cov_num_outpatient_rate;cov_cat_smoking_status;cov_bin_healthcare_worker;cov_bin_carehome_status;cov_bin_dementia;cov_bin_liver_disease;cov_bin_ckd;cov_bin_cancer;cov_bin_hypertension;cov_bin_diabetes;cov_bin_obesity;cov_bin_copd;cov_bin_ami;cov_bin_isch_stroke")
#history variables
#cov_bin_history_ra;cov_bin_history_undiff_eia;cov_bin_history_psoa;cov_bin_history_axial;cov_bin_history_grp1_ifa;cov_bin_history_sle;cov_bin_history_sjs;cov_bin_history_sss;cov_bin_history_im;cov_bin_history_mctd;cov_bin_history_as;cov_bin_history_grp2_ctd;cov_bin_history_psoriasis;cov_bin_history_hs;cov_bin_history_grp3_isd;cov_bin_history_ibd;cov_bin_history_crohn;cov_bin_history_uc;cov_bin_history_celiac;cov_bin_history_grp4_agi_ibd;cov_bin_history_addison;cov_bin_history_grave;cov_bin_history_hashimoto;cov_bin_history_grp5_atv;cov_bin_history_anca;cov_bin_history_gca;cov_bin_history_iga_vasc;cov_bin_history_pmr;cov_bin_history_grp6_trd;cov_bin_history_immune_thromb;cov_bin_history_pern_anaemia;cov_bin_history_apa;cov_bin_history_aha;cov_bin_history_grp7_htd;cov_bin_history_glb;cov_bin_history_ms;cov_bin_history_myasthenia;cov_bin_history_long_myelitis;cov_bin_history_cis;cov_bin_history_grp8_ind;cov_bin_history_composite_ai

# Remove cov_bin_history_composite_ai
composite_ai_sub_out <- c("out_date_composite_ai")

# Add active analyses ----------------------------------------------------------

for (c in cohorts) {
  
  for (i in c(outcomes_runmain, outcomes_runall)) {
  # for (i in c( outcomes_runall)) {
    
    ## analysis: main ----------------------------------------------------------
    
    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure, 
                         outcome = i,
                         ipw = ipw, 
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "main")
    
    ## analysis: sub_covid_hospitalised ----------------------------------------
    
    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure, 
                         outcome = i,
                         ipw = ipw, 
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_covid_hospitalised")
    
    ## analysis: sub_covid_nonhospitalised -------------------------------------
    
    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure, 
                         outcome = i,
                         ipw = ipw, 
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_covid_nonhospitalised")
    
    ## analysis: sub_covid_history ---------------------------------------------
    
    if (c!="prevax") {

      df[nrow(df)+1,] <- c(cohort = c,
                           exposure = exposure,
                           outcome = i,
                           ipw = ipw,
                           strata = strata,
                           covariate_sex = covariate_sex,
                           covariate_age = covariate_age,
                           covariate_other = all_covars,
                           cox_start = cox_start,
                           cox_stop = cox_stop,
                           study_start =  vax_unvax_start,
                           study_stop =  vax_unvax_stop,
                           cut_points = vax_unvax_cuts,
                           controls_per_case = controls_per_case,
                           total_event_threshold = total_event_threshold,
                           episode_event_threshold = episode_event_threshold,
                           covariate_threshold = covariate_threshold,
                           age_spline = TRUE,
                           analysis = "sub_covid_history")

    }

  }

  for (i in outcomes_runall) {

    ## analysis: sub_sex_female ------------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = "NULL",
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_sex_female")

    ## analysis: sub_sex_male --------------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = "NULL",
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_sex_male")

    ## analysis: sub_age_18_39 ------------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = FALSE,
                         analysis = "sub_age_18_39")

    ## analysis: sub_age_40_59 ------------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = FALSE,
                         analysis = "sub_age_40_59")

    ## analysis: sub_age_60_79 ------------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = FALSE,
                         analysis = "sub_age_60_79")

    ## analysis: sub_age_80_110 ------------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars,
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = FALSE,
                         analysis = "sub_age_80_110")

    ## analysis: sub_ethnicity_white -------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = gsub("cov_cat_ethnicity;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_ethnicity_white")

    ## analysis: sub_ethnicity_black -------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = gsub("cov_cat_ethnicity;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_ethnicity_black")

    ## analysis: sub_ethnicity_mixed -------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = gsub("cov_cat_ethnicity;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_ethnicity_mixed")

    ## analysis: sub_ethnicity_asian -------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = gsub("cov_cat_ethnicity;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_ethnicity_asian")

    ## analysis: sub_ethnicity_other -------------------------------------------

    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = gsub("cov_cat_ethnicity;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_ethnicity_other")
    
    ## analysis: sub_ethnicity_asian -------------------------------------------
    
    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = gsub("cov_cat_ethnicity;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_ethnicity_asian")
    
#  }
  
#  for (i in c(outcomes_runmain, outcomes_runall)) { #in composite_ai_sub_out
    
    ## analysis: sub_history_composite_ai_true ---------------------------------
    
    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars, #gsub("cov_bin_history_composite_ai;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_bin_history_composite_ai_true")
    
    ## analysis: sub_history_composite_ai_false --------------------------------
    
    df[nrow(df)+1,] <- c(cohort = c,
                         exposure = exposure,
                         outcome = i,
                         ipw = ipw,
                         strata = strata,
                         covariate_sex = covariate_sex,
                         covariate_age = covariate_age,
                         covariate_other = all_covars, #gsub("cov_bin_history_composite_ai;","",all_covars),
                         cox_start = cox_start,
                         cox_stop = cox_stop,
                         study_start = ifelse(c=="prevax", prevax_start, vax_unvax_start),
                         study_stop = ifelse(c=="prevax", prevax_stop, vax_unvax_stop),
                         cut_points = ifelse(c=="prevax", prevax_cuts, vax_unvax_cuts),
                         controls_per_case = controls_per_case,
                         total_event_threshold = total_event_threshold,
                         episode_event_threshold = episode_event_threshold,
                         covariate_threshold = covariate_threshold,
                         age_spline = TRUE,
                         analysis = "sub_bin_history_composite_ai_false")
  }
}


# Assign unique name -----------------------------------------------------------

df$name <- paste0("cohort_",df$cohort, "-", 
                  df$analysis, "-", 
                  gsub("out_date_","",df$outcome))

# Select certain models --------------------------------------------------------

df <- df[df$analysis == "main" | df$analysis == "sub_covid_hospitalised" | df$analysis == "sub_covid_nonhospitalised",]

#df <- df[df$analysis == "main" | df$analysis == "sub_bin_history_composite_ai_true" | df$analysis == "sub_bin_history_composite_ai_false",]

# df <- df[df$analysis == "sub_covid_history" | df$analysis == "sub_sex_male" | df$analysis == "sub_sex_female",]
# 
# df <- df[df$analysis == "sub_age_18_39" | df$analysis == "sub_age_40_59" | df$analysis == "sub_age_60_79" | df$analysis == "sub_age_80_110",]
# 
# df <- df[df$analysis == "sub_ethnicity_white" | df$analysis == "sub_ethnicity_black" | df$analysis == "sub_ethnicity_mixed" | df$analysis == "sub_ethnicity_asian" | df$analysis == "sub_ethnicity_other",]

# Check names are unique and save active analyses list -------------------------

if (length(unique(df$name))==nrow(df)) {
  saveRDS(df, file = "lib/active_analyses.rds", compress = "gzip")
} else {
  stop(paste0("ERROR: names must be unique in active analyses table"))
}