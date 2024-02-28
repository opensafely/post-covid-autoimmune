# Based on common_variables in https://github.com/opensafely/post-covid-vaccinated/blob/main/analysis/common_variables.py

# Import statements

## Cohort extractor
from cohortextractor import (
    patients,
    codelist,
    filter_codes_by_category,
    combine_codelists,
    codelist_from_csv,
)

#study dates
from grouping_variables import (
    study_dates,
    days)
## Codelists from codelist.py (which pulls them from the codelist folder)
from codelists import *

## Datetime functions
from datetime import date

## Study definition helper
import study_definition_helper_functions as helpers

# Define pandemic_start
pandemic_start = study_dates["pandemic_start"]
# Define common variables function

def generate_common_variables_history(index_date_variable, exposure_end_date_variable, outcome_end_date_variable):
    dynamic_variables = dict(
    
# DEFINE EXPOSURES ------------------------------------------------------

    ## Date of positive SARS-COV-2 PCR antigen test
    tmp_exp_date_covid19_confirmed_sgss=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
        between=[f"{index_date_variable}",f"{exposure_end_date_variable}"],
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.2,
        },
    ),
    ## First COVID-19 code (diagnosis, positive test or sequalae) in primary care
    tmp_exp_date_covid19_confirmed_snomed=patients.with_these_clinical_events(
        combine_codelists(
            covid_primary_care_code,
            covid_primary_care_positive_test,
            covid_primary_care_sequalae,
        ),
        returning="date",
        between=[f"{index_date_variable}",f"{exposure_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.2,
        },
    ),
    ## Start date of episode with confirmed diagnosis in any position
    tmp_exp_date_covid19_confirmed_hes=patients.admitted_to_hospital(
        with_these_diagnoses=covid_codes,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{exposure_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.1,
        },
    ),
    ## Date of death with SARS-COV-2 infection listed as primary or underlying cause
    tmp_exp_date_covid19_confirmed_death=patients.with_these_codes_on_death_certificate(
        covid_codes,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{exposure_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.2
        },
    ),
    ## Generate variable to identify first date of confirmed COVID
    exp_date_covid19_confirmed=patients.minimum_of(
        "tmp_exp_date_covid19_confirmed_sgss","tmp_exp_date_covid19_confirmed_snomed","tmp_exp_date_covid19_confirmed_hes","tmp_exp_date_covid19_confirmed_death"
    ),

    # POPULATION SELECTION VARIABLES ------------------------------------------------------

    has_follow_up_previous_6months=patients.registered_with_one_practice_between(
        start_date=f"{index_date_variable} - 6 months",
        end_date=f"{index_date_variable}",
        return_expectations={"incidence": 0.95},
    ),

    has_died = patients.died_from_any_cause(
        on_or_before = f"{index_date_variable}",
        returning="binary_flag",
        return_expectations={"incidence": 0.01}
    ),

    registered_at_start = patients.registered_as_of(f"{index_date_variable}",
    ),

    # Deregistration date
    dereg_date=patients.date_deregistered_from_all_supported_practices(
        
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format = 'YYYY-MM-DD',
        return_expectations={
        "date": {"earliest": study_dates["pandemic_start"], "latest": "today"},
        "rate": "uniform",
        "incidence": 0.01
        },
    ),

    # Define subgroups (for variables that don't have a corresponding covariate only)
    ## COVID-19 severity
    sub_date_covid19_hospital = patients.admitted_to_hospital(
        with_these_primary_diagnoses=covid_codes,
        returning="date_admitted",
        on_or_after="exp_date_covid19_confirmed",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    ## History of COVID-19 
    ### Positive SARS-COV-2 PCR antigen test
    tmp_sub_bin_covid19_confirmed_history_sgss=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.2},
    ),
    ### COVID-19 code (diagnosis, positive test or sequalae) in primary care
    tmp_sub_bin_covid19_confirmed_history_snomed=patients.with_these_clinical_events(
        combine_codelists(
            covid_primary_care_code,
            covid_primary_care_positive_test,
            covid_primary_care_sequalae,
        ),
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.2},
    ),
    ### Hospital episode with confirmed diagnosis in any position
    tmp_sub_bin_covid19_confirmed_history_hes=patients.admitted_to_hospital(
        with_these_diagnoses=covid_codes,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.2},
    ),
    ## Generate variable to identify first date of confirmed COVID
    sub_bin_covid19_confirmed_history=patients.maximum_of(
        "tmp_sub_bin_covid19_confirmed_history_sgss","tmp_sub_bin_covid19_confirmed_history_snomed","tmp_sub_bin_covid19_confirmed_history_hes"
    ),

    ########################
    # History of variables #
    ########################
    ############################################
    ## Outcome group 1: Inflammatory arthritis #
    ############################################

    ## History of Reumatoid arthritis
    # Primary
    tmp_cov_bin_history_ra_snomed = patients.with_these_clinical_events(
        ra_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    # HES
    tmp_cov_bin_history_ra_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=ra_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),

    ## Reumatoid arthritis combining primary care and secondary care
    cov_bin_history_ra=patients.minimum_of(
        "tmp_cov_bin_history_ra_snomed", "tmp_cov_bin_history_ra_hes",
    ),
    ## History of Undifferentiated inflamatory arthritis - primary care
    tmp_cov_bin_history_undiff_eia = patients.with_these_clinical_events(
        undiff_eia_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## History of Undifferentiated inflamatory arthritis - primary care
    cov_bin_history_undiff_eia=patients.minimum_of(
        "tmp_cov_bin_history_undiff_eia",
    ),

    ## History of Psoriatic arthritis - snomed
    tmp_cov_bin_history_psoa_snomed= patients.with_these_clinical_events(
        psoa_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Psoriatic arthritis - hes
    tmp_cov_bin_history_psoa_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=psoa_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    # History of Psoriatic arthritis combining primary care and secondary care
    cov_bin_history_psoa=patients.minimum_of(
        "tmp_cov_bin_history_psoa_snomed", "tmp_cov_bin_history_psoa_hes",
    ),

    ##  History of Axial spondyloarthritis - primary care
   tmp_cov_bin_history_axial_snomed= patients.with_these_clinical_events(
       axial_code_snomed,
       returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
   ),
    ## Axial spondyloarthritis -  hes
    tmp_cov_bin_history_axial_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=axial_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Axial spondyloarthritis -  combining primary care and secondary care
    cov_bin_history_axial=patients.minimum_of(
        "tmp_cov_bin_history_axial_snomed",
        "tmp_cov_bin_history_axial_hes",
    ),

    ## History of Outcome group 1
    cov_bin_history_grp1_ifa=patients.minimum_of(
        "cov_bin_history_ra", "cov_bin_history_undiff_eia", "cov_bin_history_psoa", "cov_bin_history_axial",
    ),

    ############################################################
    ## History of Outcome group 2: Connective tissue disorders #
    ############################################################
    ## History of Systematic lupus erythematosus - snomed
    tmp_cov_bin_history_sle_ctv= patients.with_these_clinical_events(
        sle_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Systematic lupus erythematosus - hes
    tmp_cov_bin_history_sle_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=sle_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Systematic lupus erythematosus -  combining primary care and secondary care
    cov_bin_history_sle=patients.minimum_of(
        "tmp_cov_bin_history_sle_ctv", "tmp_cov_bin_history_sle_hes",
    ),

    ## History of Sjogren’s syndrome - snomed
    tmp_cov_bin_history_sjs_snomed= patients.with_these_clinical_events(
        sjs_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Sjogren’s syndrome - hes
    tmp_cov_bin_history_sjs_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=sjs_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Sjogren’s syndrome  -  combining primary care and secondary care
    cov_bin_history_sjs=patients.minimum_of(
        "tmp_cov_bin_history_sjs_snomed", "tmp_cov_bin_history_sjs_hes",
    ),

    ## History of Systemic sclerosis/scleroderma - snomed
    tmp_cov_bin_history_sss_snomed= patients.with_these_clinical_events(
        sss_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Systemic sclerosis/scleroderma - hes
    tmp_cov_bin_history_sss_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=sss_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Systemic sclerosis/scleroderma -  combining primary care and secondary care
    cov_bin_history_sss=patients.minimum_of(
        "tmp_cov_bin_history_sss_snomed", "tmp_cov_bin_history_sss_hes",
    ),

    ## History of Inflammatory myositis/polymyositis/dermatolomyositis - snomed
    tmp_cov_bin_history_im_snomed = patients.with_these_clinical_events(
        im_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Inflammatory myositis/polymyositis/dermatolomyositis - hes
    tmp_cov_bin_history_im_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=im_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Inflammatory myositis/polymyositis/dermatolomyositis -  combining primary care and secondary care
    cov_bin_history_im=patients.minimum_of(
        "tmp_cov_bin_history_im_snomed", "tmp_cov_bin_history_im_hes",
    ),

    ## History of Mixed Connective Tissue Disease - snomed
    tmp_cov_bin_history_mctd_snomed= patients.with_these_clinical_events(
        mctd_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Mixed Connective Tissue Disease - hes
    tmp_cov_bin_history_mctd_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=mctd_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Mixed Connective Tissue Disease -  combining primary care and secondary care
    cov_bin_history_mctd=patients.minimum_of(
        "tmp_cov_bin_history_mctd_snomed", "tmp_cov_bin_history_mctd_hes",
    ),

    ## History of Antiphospholipid syndrome - snomed
    tmp_cov_bin_history_as = patients.with_these_clinical_events(
        as_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
        ## Mixed Connective Tissue Disease -  combining primary care and secondary care
    cov_bin_history_as=patients.minimum_of(
        "tmp_cov_bin_history_as",
    ),

    ## History of Outcome group 2
    cov_bin_history_grp2_ctd=patients.minimum_of(
        "cov_bin_history_sle", "cov_bin_history_sjs", "cov_bin_history_sss", "cov_bin_history_im", "cov_bin_history_mctd", "cov_bin_history_as",
    ),

    ###############################################
    ## History of Outcome group 3: Inflammatory skin disease #
    ###############################################
    ## Psoriasis - primary care - ctv3
    tmp_cov_bin_history_psoriasis_ctv= patients.with_these_clinical_events(
        psoriasis_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Psoriasis - primary care - hes
    tmp_cov_bin_history_psoriasis_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=psoriasis_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Psoriasis -  combining primary care and secondary care
    cov_bin_history_psoriasis=patients.minimum_of(
        "tmp_cov_bin_history_psoriasis_ctv", "tmp_cov_bin_history_psoriasis_hes",
    ),

    ## Hydradenitis suppurativa - snomed
    tmp_cov_bin_history_hs_ctv= patients.with_these_clinical_events(
        hs_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Hydradenitis suppurativa - secondary care - hes
    tmp_cov_bin_history_hs_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=hs_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Hydradenitis suppurativa -  combining primary care and secondary care
    cov_bin_history_hs =patients.minimum_of(
        "tmp_cov_bin_history_hs_ctv", "tmp_cov_bin_history_hs_hes",
    ),

    ## History of Outcome group 3: Inflammatory skin disease
    cov_bin_history_grp3_isd=patients.minimum_of(
        "cov_bin_history_psoriasis",  "cov_bin_history_hs",
    ),

    ###########################################################################
    ## History of Outcome group 4: Autoimmune GI / Inflammatory bowel disease #
    ###########################################################################
    ## Inflammatory bowel disease (combined UC and Crohn's) - SNOMED
    tmp_cov_bin_history_ibd_snomed= patients.with_these_clinical_events(
        ibd_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Inflammatory bowel disease (combined UC and Crohn's) - CTV3
    tmp_cov_bin_history_ibd_ctv= patients.with_these_clinical_events(
        ibd_code_ctv3,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Inflammatory bowel disease (combined UC and Crohn's) - secondary care - hes
    tmp_cov_bin_history_ibd_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=ibd_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Inflammatory bowel disease combined
    cov_bin_history_ibd=patients.minimum_of(
        "tmp_cov_bin_history_ibd_snomed", "tmp_cov_bin_history_ibd_ctv", "tmp_cov_bin_history_ibd_hes",
    ),
    ## Crohn’s disease ctv
    tmp_cov_bin_history_crohn_ctv= patients.with_these_clinical_events(
        crohn_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Crohn’s disease - secondary care - hes
    tmp_cov_bin_history_crohn_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=crohn_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Crohn’s disease combined
    cov_bin_history_crohn=patients.minimum_of(
        "tmp_cov_bin_history_crohn_ctv", "tmp_cov_bin_history_crohn_hes",
    ),
    ## Ulcerative colitis - ctv
    tmp_cov_bin_history_uc_ctv= patients.with_these_clinical_events(
        uc_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Ulcerative colitis - secondary care - hes
    tmp_cov_bin_history_uc_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=uc_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Ulcerative colitis combined
    cov_bin_history_uc=patients.minimum_of(
        "tmp_cov_bin_history_uc_ctv", "tmp_cov_bin_history_uc_hes",
    ),
    ## Celiac disease - snomed
    tmp_cov_bin_history_celiac_snomed= patients.with_these_clinical_events(
        celiac_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Celiac disease - hes
    tmp_cov_bin_history_celiac_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=celiac_code_icd ,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Celiac disease combined
    cov_bin_history_celiac=patients.minimum_of(
        "tmp_cov_bin_history_celiac_snomed", "tmp_cov_bin_history_celiac_hes",
    ),
    ## History of Outcome group 4: Autoimmune GI / Inflammatory bowel disease
    cov_bin_history_grp4_agi_ibd=patients.minimum_of(
        "cov_bin_history_ibd", "cov_bin_history_crohn", "cov_bin_history_uc", "cov_bin_history_celiac",
    ),

    #################################################
    ## History of Outcome group 5: Thyroid diseases #
    #################################################
    ## Addison’s disease - primary care
    tmp_cov_bin_history_addison_snomed= patients.with_these_clinical_events(
        addison_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
     ## Addison’s disease - hes
    tmp_cov_bin_history_addison_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=addison_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Addison’s disease combined
    cov_bin_history_addison=patients.minimum_of(
        "tmp_cov_bin_history_addison_snomed", "tmp_cov_bin_history_addison_hes",
    ),
    ## Grave’s disease - primary care
    tmp_cov_bin_history_grave_snomed= patients.with_these_clinical_events(
        grave_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Grave’s disease - hes
    tmp_cov_bin_history_grave_hes=patients.admitted_to_hospital(
        with_these_primary_diagnoses=grave_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Grave’s disease combined
    cov_bin_history_grave=patients.minimum_of(
        "tmp_cov_bin_history_grave_snomed", "tmp_cov_bin_history_grave_hes",
    ),
    ## Hashimoto’s thyroiditis - snomed
    tmp_cov_bin_history_hashimoto_thyroiditis_snomed = patients.with_these_clinical_events(
        hashimoto_thyroiditis_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Hashimoto’s thyroiditis - hes
    tmp_cov_bin_history_hashimoto_thyroiditis_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses=hashimoto_thyroiditis_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Hashimoto’s thyroiditis combined - hashimoto_thyroiditis
    cov_bin_history_hashimoto=patients.minimum_of(
        "tmp_cov_bin_history_hashimoto_thyroiditis_snomed", "tmp_cov_bin_history_hashimoto_thyroiditis_hes",
    ),
    ## Thyroid toxicosis / hyper thyroid - YW: This seems to have been taken out from the excel spreadsheet, 13/Dec/2022

    ## History of Outcome group 5: Thyroid diseases - to be expanded once the other outcome components are avilable
    cov_bin_history_grp5_atv=patients.minimum_of(
        "cov_bin_history_addison", "cov_bin_history_grave", "cov_bin_history_hashimoto",
    ),

    ######################################################
    ## History of Outcome group 6: Autoimmune vasculitis #
    ######################################################
    ## ANCA-associated - snomed
    tmp_cov_bin_history_anca_snomed= patients.with_these_clinical_events(
        anca_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## ANCA-associated - hes
    tmp_cov_bin_history_anca_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= anca_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## ANCA-associated  - combined
    cov_bin_history_anca =patients.minimum_of(
        "tmp_cov_bin_history_anca_snomed", "tmp_cov_bin_history_anca_hes",
    ),
    ## Giant cell arteritis - snomed
    tmp_cov_bin_history_gca_snomed= patients.with_these_clinical_events(
        gca_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Giant cell arteritis - hes
    tmp_cov_bin_history_gca_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= gca_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Giant cell arteritis - combined
    cov_bin_history_gca=patients.minimum_of(
        "tmp_cov_bin_history_gca_snomed", "tmp_cov_bin_history_gca_hes",
    ),
    ## IgA (immunoglobulin A) vasculitis - snomed
    tmp_cov_bin_history_iga_vasculitis_snomed= patients.with_these_clinical_events(
        iga_vasculitis_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## IgA (immunoglobulin A) vasculitis - hes
    tmp_cov_bin_history_iga_vasculitis_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= iga_vasculitis_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## IgA (immunoglobulin A) vasculitis - combined - iga_vasculitis
    cov_bin_history_iga_vasc=patients.minimum_of(
        "tmp_cov_bin_history_iga_vasculitis_snomed", "tmp_cov_bin_history_iga_vasculitis_hes",
    ),
    ## Polymyalgia Rheumatica (PMR) - snomed
    tmp_cov_bin_history_pmr_snomed= patients.with_these_clinical_events(
        pmr_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ##  Polymyalgia Rheumatica (PMR) - hes
    tmp_cov_bin_history_pmr_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= pmr_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## IPolymyalgia Rheumatica (PMR) - combined
    cov_bin_history_pmr=patients.minimum_of(
        "tmp_cov_bin_history_pmr_snomed", "tmp_cov_bin_history_pmr_hes",
    ),
    ##  History of Outcome group 6: Autoimmune vasculitis - to be expanded once the other outcome components are avilable
    cov_bin_history_grp6_trd=patients.minimum_of(
        "cov_bin_history_anca", "cov_bin_history_gca","cov_bin_history_iga_vasc","cov_bin_history_pmr",
    ),

    #####################################################
    ## History of Outcome group 7: Hematologic Diseases #
    #####################################################
    ## Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - snomed
    tmp_cov_bin_history_immune_thromb_snomed= patients.with_these_clinical_events(
        immune_thromb_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - hes
    tmp_cov_bin_history_immune_thromb_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= immune_thromb_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    # Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - combined
    cov_bin_history_immune_thromb=patients.minimum_of(
        "tmp_cov_bin_history_immune_thromb_snomed", "tmp_cov_bin_history_immune_thromb_hes",
    ),
    ## Pernicious anaemia - snomed
    tmp_cov_bin_history_pernicious_anaemia_snomed= patients.with_these_clinical_events(
        pernicious_anaemia_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Pernicious anaemia - hes
    tmp_cov_bin_history_pernicious_anaemia_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= pernicious_anaemia_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Pernicious anaemia combined - pernicious_anaemia
    cov_bin_history_pern_anaemia=patients.minimum_of(
        "tmp_cov_bin_history_pernicious_anaemia_snomed", "tmp_cov_bin_history_pernicious_anaemia_hes",
    ),
    ## Aplastic Anaemia - snomed
    tmp_cov_bin_history_apa_snomed= patients.with_these_clinical_events(
        apa_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Aplastic Anaemia - ctv3
    tmp_cov_bin_history_apa_ctv= patients.with_these_clinical_events(
        apa_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Aplastic Anaemia - hes
    tmp_cov_bin_history_apa_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= apa_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Aplastic Anaemia combined
    cov_bin_history_apa=patients.minimum_of(
        "tmp_cov_bin_history_apa_snomed", "tmp_cov_bin_history_apa_ctv", "tmp_cov_bin_history_apa_hes",
    ),
    ## Autoimmune haemolytic anaemia - snomed
    tmp_cov_bin_history_aha_snomed= patients.with_these_clinical_events(
        aha_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Autoimmune haemolytic anaemia - hes
    tmp_cov_bin_history_aha_hes =patients.admitted_to_hospital(
        with_these_primary_diagnoses= aha_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Autoimmune haemolytic anaemia combined
    cov_bin_history_aha =patients.minimum_of(
        "tmp_cov_bin_history_aha_snomed", "tmp_cov_bin_history_aha_hes",
    ),
    ## History of Outcome group 7: Hematologic Diseases - to be expanded once the other outcome components are avilable
    cov_bin_history_grp7_htd=patients.minimum_of(
        "cov_bin_history_immune_thromb", "cov_bin_history_pern_anaemia", "cov_bin_history_apa", "cov_bin_history_aha",
    ),

    ###################################################################
    ## History of Outcome group 8: Inflammatory neuromuscular disease #
    ###################################################################
    ## Guillain Barre - ctv
    tmp_cov_bin_history_glb_ctv= patients.with_these_clinical_events(
        glb_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Guillain Barre - icd10
    tmp_cov_bin_history_glb_hes= patients.admitted_to_hospital(
        with_these_diagnoses=glb_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Guillain Barre combined
    cov_bin_history_glb=patients.minimum_of(
        "tmp_cov_bin_history_glb_ctv", "tmp_cov_bin_history_glb_hes", #"tmp_cov_bin_history_glb_death",
    ),
    ## Multiple Sclerosis - ctv
    tmp_cov_bin_history_multiple_sclerosis_ctv= patients.with_these_clinical_events(
        multiple_sclerosis_code_ctv,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Multiple Sclerosis - hes
    tmp_cov_bin_history_multiple_sclerosis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=multiple_sclerosis_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Multiple Sclerosis combined - multiple_sclerosis
    cov_bin_history_ms=patients.minimum_of(
        "tmp_cov_bin_history_multiple_sclerosis_ctv", "tmp_cov_bin_history_multiple_sclerosis_hes",
    ),
    ## Myasthenia gravis - snomed
    tmp_cov_bin_history_myasthenia_gravis_snomed= patients.with_these_clinical_events(
        myasthenia_gravis_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Myasthenia gravis - hes
    tmp_cov_bin_history_myasthenia_gravis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=myasthenia_gravis_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Myasthenia gravis combined - myasthenia_gravis
    cov_bin_history_myasthenia=patients.minimum_of(
        "tmp_cov_bin_history_myasthenia_gravis_snomed", "tmp_cov_bin_history_myasthenia_gravis_hes",
    ),
    ## Longitudinal myelitis - snomed
    tmp_cov_bin_history_longit_myelitis_snomed= patients.with_these_clinical_events(
        longit_myelitis_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Longitudinal myelitis - hes
    tmp_cov_bin_history_longit_myelitis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=longit_myelitis_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Longitudinal myelitis combined - longit_myelitis
    cov_bin_history_long_myelitis=patients.minimum_of(
        "tmp_cov_bin_history_longit_myelitis_snomed", "tmp_cov_bin_history_longit_myelitis_hes",
    ),
    ## Clinically isolated syndrome - snomed
    tmp_cov_bin_history_cis_snomed= patients.with_these_clinical_events(
        cis_code_snomed,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Clinically isolated syndrome - hes
    tmp_cov_bin_history_cis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=cis_code_icd,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1,
        },
    ),
    ## Clinically isolated syndrome combined
    cov_bin_history_cis=patients.minimum_of(
        "tmp_cov_bin_history_cis_snomed", "tmp_cov_bin_history_cis_hes",
    ),
    ## Outcome group 8: Inflammatory neuromuscular disease - to be expanded once codelist for other outcome components are available
    cov_bin_history_grp8_ind=patients.minimum_of(
        "cov_bin_history_glb", "cov_bin_history_ms", "cov_bin_history_myasthenia",
        "cov_bin_history_long_myelitis", "cov_bin_history_cis",
    ),

    ## Define primary outcome: composite auto-immune outcome
    cov_bin_history_composite_ai=patients.minimum_of(
        "cov_bin_history_grp1_ifa", "cov_bin_history_grp2_ctd", "cov_bin_history_grp3_isd", "cov_bin_history_grp4_agi_ibd",
        "cov_bin_history_grp5_atv", "cov_bin_history_grp6_trd", "cov_bin_history_grp7_htd", "cov_bin_history_grp8_ind",
    ),

    )
    return dynamic_variables
