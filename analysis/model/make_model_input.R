# Load packages ----------------------------------------------------------------
print('Load packages')

library(magrittr)
library(data.table)
library(dplyr)

# Source functions -------------------------------------------------------------
print('Source functions')

source("analysis/model/fn-check_vitals.R")

# Make directory ---------------------------------------------------------------
print('Make directory')

fs::dir_create(here::here("output", "model_input"))

# Specify arguments ------------------------------------------------------------
print('Specify arguments')

args <- commandArgs(trailingOnly=TRUE)

if(length(args)==0){
   name <- "all"#"prevax-sub_bin_history_composite_" # prevax-main- prepare datasets for all active analyses 
 # name <- "cohort_vax-main-grp1_ifa" # prepare datasets for all active analyses whose name contains X
} else {
  name <- args[[1]]
}

# Load active analyses ---------------------------------------------------------
print('Load active analyses')

active_analyses <- readr::read_rds("lib/active_analyses.rds")

# Identify model inputs to be prepared -----------------------------------------
print('Identify model inputs to be prepared')

if (name=="all") {
  prepare <- active_analyses$name
} else if(grepl(";",name)) {
  prepare <- stringr::str_split(as.vector(name), ";")[[1]]
} else {
  prepare <- active_analyses[grepl(name,active_analyses$name),]$name
}

# Filter active_analyses to model inputs to be prepared ------------------------
print('Filter active_analyses to model inputs to be prepared')

active_analyses <- active_analyses[active_analyses$name %in% prepare,]

for (i in 1:nrow(active_analyses)) {
  print(paste0("i=", i))
  # Load data --------------------------------------------------------------------
  print(paste0("Load data for ",active_analyses$name[i]))
  
  
  input <- dplyr::as_tibble(readr::read_rds(paste0("output/input_",active_analyses$cohort[i],"_new_stage1.rds")))
  
  # Restrict to required variables -----------------------------------------------
  print('Restrict to required variables')
  
    input <- input[,unique(c("patient_id",
                           "index_date",
                           "end_date_exposure",
                           "end_date_outcome",
                           active_analyses$exposure[i], 
                           active_analyses$outcome[i],
                           unlist(strsplit(active_analyses$strata[i], split = ";")),
                           unlist(strsplit(active_analyses$covariate_other[i], split = ";")),#[!grepl("_history_",unlist(strsplit(active_analyses$covariate_other[i], split = ";")))],
                           "sub_cat_covid19_hospital",
                           "sub_bin_covid19_confirmed_history",
                           "cov_cat_sex",
                           "cov_num_age",
                           "cov_cat_ethnicity",
                           "cov_bin_history_composite_ai",
                           "cov_bin_history_ra",
                           "cov_bin_history_undiff_eia",
                           "cov_bin_history_psoa",
                           "cov_bin_history_axial",
                           "cov_bin_history_grp1_ifa",
                           "cov_bin_history_sle",
                           "cov_bin_history_sjs",
                           "cov_bin_history_sss",
                           "cov_bin_history_im",
                           "cov_bin_history_mctd",
                           "cov_bin_history_as",
                           "cov_bin_history_grp2_ctd",
                           "cov_bin_history_psoriasis",
                           "cov_bin_history_hs",
                           "cov_bin_history_grp3_isd",
                           "cov_bin_history_ibd",
                           "cov_bin_history_crohn",
                           "cov_bin_history_uc",
                           "cov_bin_history_celiac",
                           "cov_bin_history_grp4_agi_ibd",
                           "cov_bin_history_addison",
                           "cov_bin_history_grave",
                           "cov_bin_history_hashimoto",
                           "cov_bin_history_grp5_atv",
                           "cov_bin_history_anca",
                           "cov_bin_history_gca",
                           "cov_bin_history_iga_vasc",
                           "cov_bin_history_pmr",
                           "cov_bin_history_grp6_trd",
                           "cov_bin_history_immune_thromb",
                           "cov_bin_history_pern_anaemia",
                           "cov_bin_history_apa",
                           "cov_bin_history_aha",
                           "cov_bin_history_grp7_htd",
                           "cov_bin_history_glb",
                           "cov_bin_history_ms",
                           "cov_bin_history_myasthenia",
                           "cov_bin_history_long_myelitis",
                           "cov_bin_history_cis",
                           "cov_bin_history_grp8_ind",
                           "sub_bin_history_composite_ai"))] 
 #   ))]
  
  # Remove outcomes outside of follow-up time ------------------------------------
  print('Remove outcomes outside of follow-up time')
  
  input <- dplyr::rename(input, 
                         "out_date" =active_analyses$outcome[i],
                         "exp_date" = active_analyses$exposure[i])
  
  input <- input %>% 
    dplyr::mutate(out_date = replace(out_date, which(out_date>end_date_outcome | out_date<index_date), NA),
                  exp_date =  replace(exp_date, which(exp_date>end_date_exposure | exp_date<index_date), NA),
                  sub_cat_covid19_hospital = replace(sub_cat_covid19_hospital, which(is.na(exp_date)),"no_infection"))
  
  # Update end date to be outcome date where applicable ------------------------
  print('Update end date to be outcome date where applicable')
  
  input <- input %>% 
    dplyr::rowwise() %>% 
    dplyr::mutate(end_date_outcome = min(end_date_outcome, out_date, na.rm = TRUE))
  
  # Exclude individuals at index date ------------------------------------------
  print("Apply exclusion criteria according to each outcome")
  
  outcome <- active_analyses$outcome[i]
  
  # Outcome group 1
  
  if (outcome == "out_date_ra") {

    input <- input[input$cov_bin_history_ra == FALSE,]
    input$cov_bin_history_ra <- NULL 

  } else if (outcome == "out_date_undiff_eia") {

    input <- input[input$cov_bin_history_undiff_eia == FALSE,]
    input$cov_bin_history_undiff_eia <- NULL 
    
  } else if (outcome == "out_date_psoa") {

    input <- input[input$cov_bin_history_psoa == FALSE,]
    input$cov_bin_history_psoa <- NULL 

  } else if (outcome == "out_date_axial") {

    input <- input[input$cov_bin_history_axial == FALSE,]
    input$cov_bin_history_axial <- NULL 

  } else if (outcome == "out_date_grp1_ifa") {

    input <- input[input$cov_bin_history_grp1_ifa == FALSE,]
    input$cov_bin_history_grp1_ifa <- NULL 

  # Outcome group 2  

  } else if (outcome == "out_date_sle") {

    input <- input[input$cov_bin_history_sle == FALSE,]
    input$cov_bin_history_sle <- NULL 

  } else if (outcome == "out_date_sjs") {

    input <- input[input$cov_bin_history_sjs == FALSE,]
    input$cov_bin_history_sjs <- NULL 

  } else if (outcome == "out_date_sss") {

    input <- input[input$cov_bin_history_sss == FALSE,]
    input$cov_bin_history_sss <- NULL 

  } else if (outcome == "out_date_im") {

    input <- input[input$cov_bin_history_im == FALSE,]
    input$cov_bin_history_im <- NULL 

  } else if (outcome == "out_date_mctd") {

    input <- input[input$cov_bin_history_mctd == FALSE,]
    input$cov_bin_history_mctd <- NULL 

  } else if (outcome == "out_date_as") {

    input <- input[input$cov_bin_history_as == FALSE,]
    input$cov_bin_history_as <- NULL 

  } else if (outcome == "out_date_grp2_ctd") {
    
    input <- input[input$cov_bin_history_grp2_ctd == FALSE,]
    input$cov_bin_history_grp2_ctd <- NULL 

  # Outcome group 3
    
  } else if (outcome == "out_date_psoriasis") {
    
    input <- input[input$cov_bin_history_psoriasis == FALSE,]
    input$cov_bin_history_psoriasis <- NULL 

  } else if (outcome == "out_date_hs") {
    
    input <- input[input$cov_bin_history_hs == FALSE,]
    input$cov_bin_history_hs <- NULL 

  } else if (outcome == "out_date_grp3_isd") {
    
    input <- input[input$cov_bin_history_grp3_isd == FALSE,]
    input$cov_bin_history_grp3_isd <- NULL 

  # Outcome group 4
    
  } else if (outcome == "out_date_ibd") {
    
    input <- input[input$cov_bin_history_ibd == FALSE,]
    input$cov_bin_history_ibd <- NULL 

  } else if (outcome == "out_date_crohn") {
    
    input <- input[input$cov_bin_history_crohn == FALSE,]
    input$cov_bin_history_crohn <- NULL 

  } else if (outcome == "out_date_uc") {
    
    input <- input[input$cov_bin_history_uc == FALSE,]
    input$cov_bin_history_uc <- NULL 

  } else if (outcome == "out_date_celiac") {
    
    input <- input[input$cov_bin_history_celiac == FALSE,]
    input$cov_bin_history_celiac <- NULL 

  } else if (outcome == "out_date_grp4_agi_ibd") {
    
    input <- input[input$cov_bin_history_grp4_agi_ibd == FALSE,]
    input$cov_bin_history_grp4_agi_ibd <- NULL 

  # Outcome group 5
    
  } else if (outcome == "out_date_addison") {
    
    input <- input[input$cov_bin_history_addison == FALSE,]
    input$cov_bin_history_addison <- NULL 

  } else if (outcome == "out_date_grave") {
    
    input <- input[input$cov_bin_history_grave == FALSE,]
    input$cov_bin_history_grave <- NULL 

  } else if (outcome == "out_date_hashimoto") {

    input <- input[input$cov_bin_history_hashimoto == FALSE,]
    input$cov_bin_history_hashimoto <- NULL 

  } else if (outcome == "out_date_grp5_atv") {
    
    input <- input[input$cov_bin_history_grp5_atv == FALSE,]
    input$cov_bin_history_grp5_atv <- NULL 

  # Outcome group 6
    
  } else if (outcome == "out_date_anca") {

    input <- input[input$cov_bin_history_anca == FALSE,]
    input$cov_bin_history_anca <- NULL 

  } else if (outcome == "out_date_gca") {

    input <- input[input$cov_bin_history_gca == FALSE,]
    input$cov_bin_history_gca <- NULL 

  } else if (outcome == "out_date_iga_vasc") {

    input <- input[input$cov_bin_history_iga_vasc == FALSE,]
    input$cov_bin_history_iga_vasc <- NULL 

  } else if (outcome == "out_date_pmr") {
    
    input <- input[input$cov_bin_history_pmr == FALSE,]
    input$cov_bin_history_pmr <- NULL 

  } else if (outcome == "out_date_grp6_trd") {
    
    input <- input[input$cov_bin_history_grp6_trd == FALSE,]
    input$cov_bin_history_grp6_trd <- NULL 

  # Outcome group 7
    
  } else if (outcome == "out_date_immune_thromb") {
    
    input <- input[input$cov_bin_history_immune_thromb == FALSE,]
    input$cov_bin_history_immune_thromb <- NULL 

  } else if (outcome == "out_date_pern_anaemia") {
    
    input <- input[input$cov_bin_history_pern_anaemia == FALSE,]
    input$cov_bin_history_pern_anaemia <- NULL 

  } else if (outcome == "out_date_apa") {
    
    input <- input[input$cov_bin_history_apa == FALSE,]
    input$cov_bin_history_apa <- NULL 

  } else if (outcome == "out_date_aha") {

    input <- input[input$cov_bin_history_aha == FALSE,]
    input$cov_bin_history_aha <- NULL 

  } else if (outcome == "out_date_grp7_htd") {
    
    input <- input[input$cov_bin_history_grp7_htd == FALSE,]
    input$cov_bin_history_grp7_htd <- NULL 

  # Outcome group 8
    
  } else if (outcome == "out_date_glb") {

    input <- input[input$cov_bin_history_glb == FALSE,]
    input$cov_bin_history_glb <- NULL 

  } else if (outcome == "out_date_ms") {
    
    input <- input[input$cov_bin_history_ms == FALSE,]
    input$cov_bin_history_ms <- NULL 

  } else if (outcome == "out_date_myasthenia") {
    
    input <- input[input$cov_bin_history_myasthenia == FALSE,]
    input$cov_bin_history_myasthenia <- NULL 

  } else if (outcome == "out_date_long_myelitis") {

    input <- input[input$cov_bin_history_long_myelitis == FALSE,]
    input$cov_bin_history_long_myelitis <- NULL 

  } else if (outcome == "out_date_cis") {

    input <- input[input$cov_bin_history_cis == FALSE,]
    input$cov_bin_history_cis <- NULL 

  } else if (outcome == "out_date_grp8_ind") {
    
    input <- input[input$cov_bin_history_grp8_ind == FALSE,]
    input$cov_bin_history_grp8_ind <- NULL 

  # Composite outcome
    
  } else if (outcome == "out_date_composite_ai") {

    input <- input[input$cov_bin_history_composite_ai == FALSE,]
    input$cov_bin_history_composite_ai <- NULL 

  }
  
  # # Remove all history variables
  # print("Remove history variables from input file")
  # 
  # input[,colnames(input)[grepl("_history_",colnames(input))]] <- NULL
  
  # Make model input: main -------------------------------------------------------
  
  if (active_analyses$analysis[i]=="main") {
    
    print('Make model input: main')
    df <- input[input$sub_bin_covid19_confirmed_history==FALSE,]
    df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
    check_vitals(df)
    
    readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
    print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
    rm(df)
    
  }
  
  # Make model input: sub_covid_hospitalised -------------------------------------
  
  if (active_analyses$analysis[i]=="sub_covid_hospitalised") {

    print('Make model input: sub_covid_hospitalised')

    df <- input[input$sub_bin_covid19_confirmed_history==FALSE,]

    df <- df %>%
      dplyr::mutate(end_date_outcome = replace(end_date_outcome, which(sub_cat_covid19_hospital=="non_hospitalised"), exp_date-1),
                    exp_date = replace(exp_date, which(sub_cat_covid19_hospital=="non_hospitalised"), NA),
                    out_date = replace(out_date, which(out_date>end_date_outcome), NA))

    df <- df[df$end_date_outcome>=df$index_date,]

    df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL

    check_vitals(df)

    readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")), compress = "gz")
    print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
    rm(df)

  }

  # Make model input: sub_covid_nonhospitalised ----------------------------------

  if (active_analyses$analysis[i]=="sub_covid_nonhospitalised") {

    print('Make model input: sub_covid_nonhospitalised')

    df <- input[input$sub_bin_covid19_confirmed_history==FALSE,]

    df <- df %>%
      dplyr::mutate(end_date_outcome = replace(end_date_outcome, which(sub_cat_covid19_hospital=="hospitalised"), exp_date-1),
                    exp_date = replace(exp_date, which(sub_cat_covid19_hospital=="hospitalised"), NA),
                    out_date = replace(out_date, which(out_date>end_date_outcome), NA))

    df <- df[df$end_date_outcome>=df$index_date,]
    df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL

    check_vitals(df)
    readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")), compress = "gz")
    print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
    rm(df)

  }

  # Make model input: sub_covid_history ------------------------------------------

  # if (active_analyses$analysis[i]=="sub_covid_history") {
  # 
  #   print('Make model input: sub_covid_history')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==TRUE,]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")), compress = "gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_sex_female ---------------------------------------------
  # 
  # 
  # if (active_analyses$analysis[i]=="sub_sex_female") {
  # 
  #   print('Make model input: sub_sex_female')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_cat_sex=="Female",]
  # 
  #   df[,c(colnames(df)[grepl("sub_",colnames(df))],"cov_cat_sex")] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")), compress = "gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_sex_male -----------------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_sex_male") {
  # 
  #   print('Make model input: sub_sex_male')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_cat_sex=="Male",]
  # 
  #   df[,c(colnames(df)[grepl("sub_",colnames(df))],"cov_cat_sex")] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_age_18_39 ----------------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_age_18_39") {
  # 
  #   print('Make model input: sub_age_18_39')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_num_age>=18 &
  #                 input$cov_num_age<40,]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_age_40_59 ----------------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_age_40_59") {
  # 
  #   print('Make model input: sub_age_40_59')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_num_age>=40 &
  #                 input$cov_num_age<60,]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_age_60_79 ----------------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_age_60_79") {
  # 
  #   print('Make model input: sub_age_60_79')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_num_age>=60 &
  #                 input$cov_num_age<80,]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_age_80_110 ---------------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_age_80_110") {
  # 
  #   print('Make model input: sub_age_80_110')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_num_age>=80 &
  #                 input$cov_num_age<111,]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_ethnicity_white --------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_ethnicity_white") {
  # 
  #   print('Make model input: sub_ethnicity_white')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_cat_ethnicity=="White",]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_ethnicity_black --------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_ethnicity_black") {
  # 
  #   print('Make model input: sub_ethnicity_black')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_cat_ethnicity=="Black",]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_ethnicity_mixed ----------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_ethnicity_mixed") {
  # 
  #   print('Make model input: sub_ethnicity_mixed')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_cat_ethnicity=="Mixed",]
  # 
  #   df[,c(colnames(df)[grepl("sub_",colnames(df))],"cov_cat_ethnicity")] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_ethnicity_asian --------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_ethnicity_asian") {
  # 
  #   print('Make model input: sub_ethnicity_asian')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_cat_ethnicity=="South Asian",]
  # 
  #   df[,c(colnames(df)[grepl("sub_",colnames(df))],"cov_cat_ethnicity")] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: sub_ethnicity_other ----------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_ethnicity_other") {
  # 
  #   print('Make model input: sub_ethnicity_other')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$cov_cat_ethnicity=="Other",]
  # 
  #   df[,c(colnames(df)[grepl("sub_",colnames(df))],"cov_cat_ethnicity")] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  
  # Make model input: sub_history_composite_ai_true --------------------------------------

  # if (active_analyses$analysis[i]=="sub_bin_history_composite_ai_true") {
  # 
  #   print('Make model input: sub_bin_history_composite_ai_true')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$sub_bin_history_composite_ai==TRUE,]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  # 
  # # Make model input: ssub_history_composite_ai_false ----------------------------------------
  # 
  # if (active_analyses$analysis[i]=="sub_bin_history_composite_ai_false") {
  # 
  #   print('Make model input: sub_bin_history_composite_ai_false')
  # 
  #   df <- input[input$sub_bin_covid19_confirmed_history==FALSE &
  #                 input$sub_bin_history_composite_ai==FALSE,]
  # 
  #   df[,colnames(df)[grepl("sub_",colnames(df))]] <- NULL
  # 
  #   check_vitals(df)
  #   readr::write_rds(df, file.path("output", paste0("model_input-",active_analyses$name[i],".rds")),compress="gz")
  #   print(paste0("Saved: output/model_input-",active_analyses$name[i],".rds"))
  #   rm(df)
  # 
  # }
  
}
