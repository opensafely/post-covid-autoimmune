# Load libraries ---------------------------------------------------------------
print('Load libraries')

library(data.table)
library(readr)
library(dplyr)

# Specify redaction threshold --------------------------------------------------

threshold <- 6

# Source common functions ------------------------------------------------------
print('Source common functions')

source("analysis/utility.R")

# Specify arguments ------------------------------------------------------------
print('Specify arguments')

args <- commandArgs(trailingOnly=TRUE)

if(length(args)==0){
  cohort <- "vax"
} else {
  cohort <- args[[1]]
}

# Identify outcomes ------------------------------------------------------------
print('Identify outcomes')

active_analyses <- readr::read_rds("lib/active_analyses.rds")

outcomes <- gsub("out_date_","",
                 unique(active_analyses[active_analyses$cohort==cohort &
                                          active_analyses$analysis=="main",]$outcome))

# Load Venn data ---------------------------------------------------------------
print('Load Venn data')

venn <- readr::read_rds(paste0("output/venn_",cohort,".rds"))

# Create empty output table ----------------------------------------------------
print('Create empty output table')

df <- data.frame(outcome = character(),
                 only_snomed = numeric(),
                 only_hes = numeric(),
                 only_death = numeric(),
                 snomed_hes = numeric(),
                 snomed_death = numeric(),
                 hes_death = numeric(),
                 snomed_hes_death = numeric(),
                 total_snomed = numeric(),
                 total_hes = numeric(),
                 total_death = numeric(),
                 total = numeric(),
                 error = character(),
                 stringsAsFactors = FALSE)

# Populate Venn table for each outcome -----------------------------------------
print('Populate Venn table for each outcome')

for (outcome in outcomes) {
  
  print(paste0("Outcome: ", outcome))
  
  # Load model input data ------------------------------------------------------
  print('Load model input data')
  
  model_input <- readr::read_rds(paste0("output/model_input-cohort_",cohort,"-main-",outcome,".rds"))  
  model_input <- model_input[!is.na(model_input$out_date),c("patient_id","out_date")]
  
  if (nrow(model_input)>0) {
    
    # Filter Venn data based on model input --------------------------------------
    print('Filter Venn data based on model input')
    
    tmp <- venn[venn$patient_id %in% model_input$patient_id,
                c("patient_id",colnames(venn)[grepl(outcome,colnames(venn))])]
    
    colnames(tmp) <- gsub(paste0("tmp_out_date_",outcome,"_"),"",colnames(tmp))
    
    # Identify and add missing columns -------------------------------------------
    print('Identify and add missing columns')
    
    complete <- data.frame(patient_id = tmp$patient_id,
                           snomed = as.Date(NA),
                           hes = as.Date(NA),
                           death = as.Date(NA))
    
    complete[,setdiff(colnames(tmp),"patient_id")] <- NULL
    notused <- NULL
    
    if (ncol(complete)>1) {
      tmp <- merge(tmp, complete, by = c("patient_id"))
      notused <- setdiff(colnames(complete),"patient_id")
    }
    
    # Calculate the number contributing to each source combination ---------------
    print('Calculate the number contributing to each source combination')
    
    tmp$snomed_contributing <- !is.na(tmp$snomed) & 
      is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$hes_contributing <- is.na(tmp$snomed) & 
      !is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$death_contributing <- is.na(tmp$snomed) & 
      is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    tmp$snomed_hes_contributing <- !is.na(tmp$snomed) & 
      !is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$hes_death_contributing <- is.na(tmp$snomed) & 
      !is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    tmp$snomed_death_contributing <- !is.na(tmp$snomed) & 
      is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    tmp$snomed_hes_death_contributing <- !is.na(tmp$snomed) & 
      !is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    # Record the number contributing to each source combination ------------------
    print('Record the number contributing to each source combination')
    
    df[nrow(df)+1,] <- c(outcome,
                         only_snomed = nrow(tmp %>% filter(snomed_contributing==T)),
                         only_hes = nrow(tmp %>% filter(hes_contributing==T)),
                         only_death = nrow(tmp %>% filter(death_contributing==T)),
                         snomed_hes = nrow(tmp %>% filter(snomed_hes_contributing==T)),
                         snomed_death = nrow(tmp %>% filter(snomed_death_contributing==T)),
                         hes_death = nrow(tmp %>% filter(hes_death_contributing==T)),
                         snomed_hes_death = nrow(tmp %>% filter(snomed_hes_death_contributing==T)),
                         total_snomed = nrow(tmp %>% filter(!is.na(snomed))),
                         total_hes = nrow(tmp %>% filter(!is.na(hes))),
                         total_death = nrow(tmp %>% filter(!is.na(death))),
                         total = nrow(tmp),
                         error = "")
    
    # Fix source contribution for grouped outcomes -----------------------------
    
    # character to numeric
    # df <- df %>%
    #   mutate_at(vars(matches("snomed|hes|death|total")),function(x) as.numeric(as.character(x)))
    # 
    # # grp1_ifa -----------------------------------------------------------------
    # df_temp1 <- df[!grepl("grp1_ifa", df$outcome),]
    # # Select grp1_ifa components
    # df_temp1 <- df[grep("_ra_|_undiff_eia|_pa_|_axial_", df$outcome),] 
    # # Summarise
    # df_temp1 <- df_temp1 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp1$outcome <- "grp1_ifa"
    # df_temp1$error <- "" #NA
    # # relocate
    # df_temp1 <- relocate(df_temp1, outcome)
    # 
    # # grp2_ctd -----------------------------------------------------------------
    # df_temp2 <- df[!grepl("grp2_ctd", df$outcome),]
    # # Select grp1_ifa components
    # df_temp2 <- df[grep("_sle_|_sjs_|_sss_|_im_|_mctd_|_as", df$outcome),] 
    # # Summarise
    # df_temp2 <- df_temp2 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp2$outcome <- "grp2_ctd"
    # df_temp2$error <- "" #NA
    # # relocate
    # df_temp2 <- relocate(df_temp2, outcome)
    # 
    # # grp3_isd -----------------------------------------------------------------
    # df_temp3 <- df[!grepl("grp3_isd", df$outcome),]
    # # Select grp1_ifa components
    # df_temp3 <- df[grep("_psoriasis_|_hs_", df$outcome),] 
    # # Summarise
    # df_temp3 <- df_temp3 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp3$outcome <- "grp3_isd"
    # df_temp3$error <- "" #NA
    # # relocate
    # df_temp3 <- relocate(df_temp3, outcome)
    # 
    # # grp4_agi_ibd -------------------------------------------------------------
    # df_temp4 <- df[!grepl("grp4_agi_ibd", df$outcome),]
    # # Select grp1_ifa components
    # df_temp4 <- df[grep("_ibd_|_crohn_|_uc_|_celiac_", df$outcome),] 
    # # Summarise
    # df_temp4 <- df_temp4 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp4$outcome <- "grp4_agi_ibd"
    # df_temp4$error <- "" #NA
    # # relocate
    # df_temp4 <- relocate(df_temp4, outcome)
    # 
    # # grp5_atv -----------------------------------------------------------------
    # df_temp5 <- df[!grepl("grp5_atv", df$outcome),]
    # # Select grp1_ifa components
    # df_temp5 <- df[grep("_addison_|_grave_|_hashimoto_thyroiditis_", df$outcome),] 
    # # Summarise
    # df_temp5 <- df_temp5 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp5$outcome <- "grp5_atv"
    # df_temp5$error <- "" #NA
    # # relocate
    # df_temp5 <- relocate(df_temp5, outcome)
    # 
    # # grp6_trd -----------------------------------------------------------------
    # df_temp6 <- df[!grepl("grp6_trd", df$outcome),]
    # # Select grp1_ifa components
    # df_temp6 <- df[grep("_anca_|_gca_|_iga_vasculitis_|_pmr_", df$outcome),] 
    # # Summarise
    # df_temp6 <- df_temp6 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp6$outcome <- "grp6_trd"
    # df_temp6$error <- "" #NA
    # # relocate
    # df_temp6 <- relocate(df_temp6, outcome)
    # 
    # # grp7_htd -----------------------------------------------------------------
    # df_temp7 <- df[!grepl("grp7_htd", df$outcome),]
    # # Select grp1_ifa components
    # df_temp7 <- df[grep("_immune_thromb_|_pernicious_anaemia_|_apa_|_aha_", df$outcome),] 
    # # Summarise
    # df_temp7 <- df_temp7 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp7$outcome <- "grp7_htd"
    # df_temp7$error <- "" #NA
    # # relocate
    # df_temp7 <- relocate(df_temp7, outcome)
    # 
    # # grp8_ind -----------------------------------------------------------------
    # df_temp8 <- df[!grepl("grp8_ind", df$outcome),]
    # # Select grp1_ifa components
    # df_temp8 <- df[grep("_glb_|_multiple_sclerosis_|_myasthenia_gravis_|_longit_myelitis_|_cis_", df$outcome),] 
    # # Summarise
    # df_temp8 <- df_temp8 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp8$outcome <- "grp8_ind"
    # df_temp8$error <- "" #NA
    # # relocate
    # df_temp8 <- relocate(df_temp8, outcome)
    # 
    # # composite ai -------------------------------------------------------------
    # df_temp9 <- df[!grepl("composite_ai", df$outcome),]
    # # Select grp1_ifa components
    # df_temp9 <- df[grep("_ra_|_undiff_eia|_pa_|_axial_|_sle_|_sjs_|_sss_|_im_|_mctd_|_as|_psoriasis_|_hs_|_ibd_|_crohn_|_uc_|_celiac_|
    #                     _addison_|_grave_|_hashimoto_thyroiditis_|_anca_|_gca_|_iga_vasculitis_|_pmr_|_immune_thromb_|_pernicious_anaemia_|_apa_|_aha_|
    #                     _glb_|_multiple_sclerosis_|_myasthenia_gravis_|_longit_myelitis_|_cis_", df$outcome),] 
    # # Summarise
    # df_temp9 <- df_temp9 %>%
    #   summarise_if(is.numeric, sum, na.rm = T)
    # # add columns  
    # df_temp9$outcome <- "composite_ai"
    # df_temp9$error <- "" #NA
    # # relocate
    # df_temp9 <- relocate(df_temp9, outcome)
    # 
    # # remove grouped outcomes
    # df <- df[!grepl("grp1_ifa|grp2_ctd|grp3_isd|grp4_agi_ibd|grp5_atv|grp6_trd|grp7_htd|grp8_ind|composite_ai", df$outcome),]
    # 
    # # --------------------------------------------------------------------------
    # # add columns  
    # # df_temp$outcome <- c("grp1_ifa", "grp2_ctd", "grp3_isd", "grp4_agi_ibd", "grp5_atv", "grp6_trd", "grp7_htd", "grp8_ind", "composite_ai")
    # # df_temp$error <- "" #NA
    # 
    # # bind data frames
    # df <- bind_rows(df, df_temp1, df_temp2, df_temp3, df_temp4, df_temp5, df_temp6, df_temp7, df_temp8, df_temp9)
    
    # remove temporary df
    # rm(df_temp1, df_temp2, df_temp3, df_temp4, df_temp5, df_temp6, df_temp7, df_temp8, df_temp9)
    
    # Replace source combinations with NA if not in study definition -----------
    print('Replace source combinations with NA if not in study definition')
    
    source_combos <- c("only_snomed","only_hes","only_death","snomed_hes","snomed_death","hes_death","snomed_hes_death","total_snomed","total_hes","total_death")
    source_consid <- source_combos
    
    if (!is.null(notused)) {
      for (i in notused) {
        
        # Add variables to consider for Venn plot to vector
        source_consid <- source_combos[!grepl(i,source_combos)]
        
        # Replace unused sources with NA in summary table
        for (j in setdiff(source_combos,source_consid)) {
          df[df$outcome==outcome,j] <- NA
        }
        
      }
    }
    
  } else {
    
    # Record empty outcome -----------------------------------------------------
    print('Record empty outcome')
    
    df[nrow(df)+1,] <- c(outcome,
                         only_snomed = NA,
                         only_hes = NA,
                         only_death = NA,
                         snomed_hes = NA,
                         snomed_death = NA,
                         hes_death = NA,
                         snomed_hes_death = NA,
                         total_snomed = NA,
                         total_hes = NA,
                         total_death = NA,
                         total = NA,
                         error = "No outcomes in model input")
    
    
  }
  
}

# Record cohort ----------------------------------------------------------------
print('Record cohort')

df$cohort <- cohort

# Save Venn data -----------------------------------------------------------------
print('Save Venn data')

write.csv(df, paste0("output/venn_",cohort,".csv"), row.names = FALSE)

# Perform redaction ------------------------------------------------------------
print('Perform redaction')

df[,setdiff(colnames(df),c("outcome"))] <- lapply(df[,setdiff(colnames(df),c("outcome"))],
                                                  FUN=function(y){roundmid_any(as.numeric(y), to=threshold)})

# Rename columns (output redaction) --------------------------------------------

names(df)[names(df) == "only_snomed"] <- "only_snomed_midpoint6"
names(df)[names(df) == "only_hes"] <- "only_hes_midpoint6"
names(df)[names(df) == "only_death"] <- "only_death_midpoint6"
names(df)[names(df) == "snomed_hes"] <- "snomed_hes_midpoint6"
names(df)[names(df) == "snomed_death"] <- "snomed_death_midpoint6"
names(df)[names(df) == "hes_death"] <- "hes_death_midpoint6"
names(df)[names(df) == "snomed_hes_death"] <- "snomed_hes_death_midpoint6"
names(df)[names(df) == "total_snomed"] <- "total_snomed_midpoint6"
names(df)[names(df) == "total_hes"] <- "total_hes_midpoint6"
names(df)[names(df) == "total_death"] <- "total_death_midpoint6"
names(df)[names(df) == "total"] <- "total_midpoint6_derived"

# Save rounded Venn data -------------------------------------------------------
print('Save rounded Venn data')

write.csv(df, paste0("output/venn_",cohort,"_midpoint6.csv"), row.names = FALSE)