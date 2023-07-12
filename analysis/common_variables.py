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

def generate_common_variables(index_date_variable,exposure_end_date_variable,outcome_end_date_variable):
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
            "incidence": 0.1,
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
            "incidence": 0.1,
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
            "incidence": 0.1
        },
    ),
    ## Generate variable to identify first date of confirmed COVID
    exp_date_covid19_confirmed=patients.minimum_of(
        "tmp_exp_date_covid19_confirmed_sgss","tmp_exp_date_covid19_confirmed_snomed","tmp_exp_date_covid19_confirmed_hes","tmp_exp_date_covid19_confirmed_death"
    ),

    ## POPULATION SELECTION VARIABLES ------------------------------------------------------
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
    dereg_date=patients.date_deregistered_from_all_supported_practices(
        
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format = 'YYYY-MM-DD',
        return_expectations={
        "date": {"earliest": study_dates["pandemic_start"], "latest": "today"},
        "rate": "uniform",
        "incidence": 0.01
    },
    ),
    ## Define subgroups (for variables that don't have a corresponding covariate only)
    ## COVID-19 severity
    sub_date_covid19_hospital=patients.admitted_to_hospital(
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
        return_expectations={"incidence": 0.1},
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
        return_expectations={"incidence": 0.1},
    ),
    ### Hospital episode with confirmed diagnosis in any position
    tmp_sub_bin_covid19_confirmed_history_hes=patients.admitted_to_hospital(
        with_these_diagnoses=covid_codes,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ## Generate variable to identify first date of confirmed COVID
    sub_bin_covid19_confirmed_history=patients.maximum_of(
        "tmp_sub_bin_covid19_confirmed_history_sgss","tmp_sub_bin_covid19_confirmed_history_snomed","tmp_sub_bin_covid19_confirmed_history_hes"
    ),

# DEFINE COVARIATES ------------------------------------------------------

    ## Age
    cov_num_age = patients.age_as_of(
        f"{index_date_variable} - 1 day",
        return_expectations = {
        "rate": "universal",
        "int": {"distribution": "population_ages"},
        "incidence" : 0.001
        },
    ),
    ## Ethnicity 
    cov_cat_ethnicity=patients.categorised_as(
        helpers.generate_ethnicity_dictionary(6),
        cov_ethnicity_sus=patients.with_ethnicity_from_sus(
            returning="group_6", use_most_frequent_code=True
        ),
        cov_ethnicity_gp_opensafely=patients.with_these_clinical_events(
            opensafely_ethnicity_codes_6,
            on_or_before=f"{index_date_variable} - 1 day",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_primis=patients.with_these_clinical_events(
            primis_covid19_vacc_update_ethnicity,
            on_or_before=f"{index_date_variable} -1 day",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_opensafely_date=patients.with_these_clinical_events(
            opensafely_ethnicity_codes_6,
            on_or_before=f"{index_date_variable} -1 day",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_primis_date=patients.with_these_clinical_events(
            primis_covid19_vacc_update_ethnicity,
            on_or_before=f"{index_date_variable} - 1 day",
            returning="category",
            find_last_match_in_period=True,
        ),
        return_expectations=helpers.generate_universal_expectations(5,True),
    ),

    ## Deprivation
    cov_cat_deprivation=patients.categorised_as(
        helpers.generate_deprivation_ntile_dictionary(10),
        index_of_multiple_deprivation=patients.address_as_of(
            f"{index_date_variable} - 1 day",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations=helpers.generate_universal_expectations(10,False),
    ),

    ## Region
    cov_cat_region=patients.registered_practice_as_of(
        f"{index_date_variable} - 1 day",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and The Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East": 0.1,
                    "London": 0.2,
                    "South East": 0.1,
                    "South West": 0.1,
                },
            },
        },
    ),

    ## Smoking status
    cov_cat_smoking_status=patients.categorised_as(
        {
            "S": "most_recent_smoking_code = 'S'",
            "E": """
                most_recent_smoking_code = 'E' OR (
                most_recent_smoking_code = 'N' AND ever_smoked
                )
            """,
            "N": "most_recent_smoking_code = 'N' AND NOT ever_smoked",
            "M": "DEFAULT",
        },
        return_expectations={
            "category": {"ratios": {"S": 0.6, "E": 0.1, "N": 0.2, "M": 0.1}}
        },
        most_recent_smoking_code=patients.with_these_clinical_events(
            smoking_clear,
            find_last_match_in_period=True,
            on_or_before=f"{index_date_variable} -1 day",
            returning="category",
        ),
        ever_smoked=patients.with_these_clinical_events(
            filter_codes_by_category(smoking_clear, include=["S", "E"]),
            on_or_before=f"{index_date_variable} -1 day",
        ),
    ),

    ## Combined oral contraceptive pill
    ### dmd: dictionary of medicines and devices
    cov_bin_combined_oral_contraceptive_pill=patients.with_these_medications(
        cocp_dmd, 
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.3},
    ),

    ## Hormone replacement therapy
    cov_bin_hormone_replacement_therapy=patients.with_these_medications(
        hrt_dmd, 
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",

        return_expectations={"incidence": 0.3},
    ),
    ## Care home status
    cov_bin_carehome_status=patients.care_home_status_as_of(
        f"{index_date_variable} -1 day", 
        categorised_as={
            "TRUE": """
              IsPotentialCareHome
              AND LocationDoesNotRequireNursing='Y'
              AND LocationRequiresNursing='N'
            """,
            "TRUE": """
              IsPotentialCareHome
              AND LocationDoesNotRequireNursing='N'
              AND LocationRequiresNursing='Y'
            """,
            "TRUE": "IsPotentialCareHome",
            "FALSE": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"TRUE": 0.30, "FALSE": 0.70},},
        },
    ),

    ## Obesity
    ### Primary care
    tmp_cov_bin_obesity_snomed=patients.with_these_clinical_events(
        bmi_obesity_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} -1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_obesity_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=bmi_obesity_icd10,
        on_or_before=f"{index_date_variable} -1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_obesity=patients.maximum_of(
        "tmp_cov_bin_obesity_snomed", "tmp_cov_bin_obesity_hes",
    ),
  

    ## Total Cholesterol
    tmp_cov_num_cholesterol=patients.max_recorded_value(
        cholesterol_snomed,
        on_most_recent_day_of_measurement=True, 
        between=[f"{index_date_variable} - 5years", f"{index_date_variable} -1 day"],
        date_format="YYYY-MM-DD",
        return_expectations={
            "float": {"distribution": "normal", "mean": 5.0, "stddev": 2.5},
            "date": {"earliest":study_dates["earliest_expec"], "latest": "today"}, ##return_expectations can't take dynamic variable se default are kept here! 
            "incidence": 0.80,
        },
    ),

    ## HDL Cholesterol
    tmp_cov_num_hdl_cholesterol=patients.max_recorded_value(
        hdl_cholesterol_snomed,
        on_most_recent_day_of_measurement=True, 
        between=[f"{index_date_variable}- 5years", f"{index_date_variable} -1 day"],
        date_format="YYYY-MM-DD",
        return_expectations={
            "float": {"distribution": "normal", "mean": 2.0, "stddev": 1.5},
            "date": {"earliest": study_dates["earliest_expec"] , "latest": "today"},
            "incidence": 0.80,
        },
    ),

    ## BMI
    # taken from: https://github.com/opensafely/BMI-and-Metabolic-Markers/blob/main/analysis/common_variables.py 
    cov_num_bmi=patients.most_recent_bmi(
        on_or_before=f"{index_date_variable} -1 day",
        minimum_age_at_measurement=18,
        include_measurement_date=True,
        date_format="YYYY-MM",
        return_expectations={
            "date": {"earliest": "2010-02-01", "latest": "2022-02-01"}, ##How do we obtain these dates ? 
            "float": {"distribution": "normal", "mean": 28, "stddev": 8},
            "incidence": 0.7,
        },
    ),
     ### Categorising BMI
    cov_cat_bmi_groups = patients.categorised_as(
        {
            "Underweight": "cov_num_bmi < 18.5 AND cov_num_bmi > 12", 
            "Healthy_weight": "cov_num_bmi >= 18.5 AND cov_num_bmi < 25", 
            "Overweight": "cov_num_bmi >= 25 AND cov_num_bmi < 30",
            "Obese": "cov_num_bmi >=30 AND cov_num_bmi <70", 
            "Missing": "DEFAULT", 
        }, 
        return_expectations = {
            "rate": "universal", 
            "category": {
                "ratios": {
                    "Underweight": 0.05, 
                    "Healthy_weight": 0.25, 
                    "Overweight": 0.4,
                    "Obese": 0.3, 
                }
            },
        },
        
    ),
# Define quality assurances

    ## Prostate cancer
        ### Primary care
        prostate_cancer_snomed=patients.with_these_clinical_events(
            prostate_cancer_snomed_clinical,
            returning='binary_flag',
            return_expectations={
                "incidence": 0.03,
            },
        ),
        ### HES APC
        prostate_cancer_hes=patients.admitted_to_hospital(
            with_these_diagnoses=prostate_cancer_icd10,
            returning='binary_flag',
            return_expectations={
                "incidence": 0.03,
            },
        ),
        ### ONS
        prostate_cancer_death=patients.with_these_codes_on_death_certificate(
            prostate_cancer_icd10,
            returning='binary_flag',
            return_expectations={
                "incidence": 0.02
            },
        ),
        ### Combined
        qa_bin_prostate_cancer=patients.maximum_of(
            "prostate_cancer_snomed", "prostate_cancer_hes", "prostate_cancer_death"
        ),

    ## Pregnancy
        qa_bin_pregnancy=patients.with_these_clinical_events(
            pregnancy_snomed_clinical,
            returning='binary_flag',
            return_expectations={
                "incidence": 0.03,
            },
        ),
    
    ## Year of birth
        qa_num_birth_year=patients.date_of_birth(
            date_format="YYYY",
            return_expectations={
                "date": {"earliest": study_dates["earliest_expec"], "latest": "today"},
                "rate": "uniform",
            },
        ),
        # Define fixed covariates other than sex
# NB: sex is required to determine vaccine eligibility covariates so is defined in study_definition_electively_unvaccinated.py

    ## 2019 consultation rate
        cov_num_consulation_rate=patients.with_gp_consultations(
            between=[days(study_dates["pandemic_start"],-365), days(study_dates["pandemic_start"],-1)],
            returning="number_of_matches_in_period",
            return_expectations={
                "int": {"distribution": "poisson", "mean": 5},
            },
        ),

    ## Healthcare worker
    cov_bin_healthcare_worker=patients.with_healthcare_worker_flag_on_covid_vaccine_record(
        returning='binary_flag',
        return_expectations={"incidence": 0.01},
    ),
    ##############################################################################################################################
    ## Define autoimune outcomes                                                                                                ##
    ##############################################################################################################################
    #################################################################################################
    ## Outcome group 1: Inflammatory arthritis                                                      ##
    #################################################################################################
    ## Reumatoid arthritis
    temp_out_date_ra_snomed = patients.with_these_clinical_events(
        ra_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    temp_out_date_ra_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=ra_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Reumatoid arthritis combining primary care and secondary care
    out_date_ra=patients.minimum_of(
        "temp_out_date_ra_snomed", "temp_out_date_ra_hes"
    ),
    ## Undifferentiated inflamatory arthritis - primary care
    out_date_undiff_eia = patients.with_these_clinical_events(
        undiff_eia_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Undifferentiated inflamatory arthritis - no secondary care code

    ## Psoriatic arthritis - snomed
    temp_out_date_pa_snomed= patients.with_these_clinical_events(
        pa_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Psoriatic arthritis - hes
    temp_out_date_pa_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=pa_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Psoriatic arthritis combining primary care and secondary care
    out_date_pa=patients.minimum_of(
        "temp_out_date_pa_snomed", "temp_out_date_pa_hes"
    ),
    ##  Axial spondyloarthritis - primary care
    temp_out_date_axial_snomed= patients.with_these_clinical_events(
        axial_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Axial spondyloarthritis -  hes
    temp_out_date_axial_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=axial_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Axial spondyloarthritis -  combining primary care and secondary care
    out_date_axial=patients.minimum_of(
        "temp_out_date_axial_snomed", "temp_out_date_axial_hes"
    ),
    ## Outcome group 1
    out_date_grp1_ifa=patients.minimum_of(
        "out_date_ra", "out_date_undiff_eia", "out_date_pa", "out_date_axial"
    ),
    #################################################################################################
    ## Outcome group 2: Connective tissue disorders                                                ##
    #################################################################################################
    ## Systematic lupus erythematosus - snomed
    temp_out_date_sle_snomed= patients.with_these_clinical_events(
        sle_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Systematic lupus erythematosus - hes
    temp_out_date_sle_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=sle_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Systematic lupus erythematosus -  combining primary care and secondary care
    out_date_sle=patients.minimum_of(
        "temp_out_date_sle_snomed", "temp_out_date_sle_hes"
    ),
    ## Sjogren’s syndrome - snomed
    temp_out_date_sjs_snomed= patients.with_these_clinical_events(
        sjs_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Sjogren’s syndrome - hes
    temp_out_date_sjs_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=sjs_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Sjogren’s syndrome  -  combining primary care and secondary care
    out_date_sjs=patients.minimum_of(
        "temp_out_date_sjs_snomed", "temp_out_date_sjs_hes"
    ),
    ## Systemic sclerosis/scleroderma - snomed
    temp_out_date_sss_snomed= patients.with_these_clinical_events(
        sss_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Systemic sclerosis/scleroderma - hes
    temp_out_date_sss_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=sss_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Systemic sclerosis/scleroderma -  combining primary care and secondary care
    out_date_sss=patients.minimum_of(
        "temp_out_date_sss_snomed", "temp_out_date_sss_hes"
    ),
    ## Inflammatory myositis/polymyositis/dermatolomyositis - snomed
    temp_out_date_im_snomed = patients.with_these_clinical_events(
        im_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Inflammatory myositis/polymyositis/dermatolomyositis - hes
    temp_out_date_im_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=im_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Inflammatory myositis/polymyositis/dermatolomyositis -  combining primary care and secondary care
    out_date_im=patients.minimum_of(
        "temp_out_date_im_snomed", "temp_out_date_im_hes"
    ),
    ## Mixed Connective Tissue Disease - snomed
    temp_out_date_mctd_snomed= patients.with_these_clinical_events(
        mctd_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Mixed Connective Tissue Disease - hes
    temp_out_date_mctd_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=mctd_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Mixed Connective Tissue Disease -  combining primary care and secondary care
    out_date_mctd=patients.minimum_of(
        "temp_out_date_mctd_snomed", "temp_out_date_mctd_hes"
    ),
    ## Antiphospholipid syndrome - snomed
    out_date_as = patients.with_these_clinical_events(
        as_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Antiphospholipid syndrome - no icd10 code
    ## Outcome group 2
    out_date_grp2_ctd=patients.minimum_of(
        "out_date_sle", "out_date_sjs", "out_date_sss", "out_date_im", "out_date_mctd", "out_date_as"
    ),
    #################################################################################################
    ## Outcome group 3: Inflammatory skin disease                                                  ##
    #################################################################################################
    ## Psoriasis - primary care - ctv3
    temp_out_date_psoriasis_ctv= patients.with_these_clinical_events(
        psoriasis_code_ctv,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Psoriasis - primary care - hes
    temp_out_date_psoriasis_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=psoriasis_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Psoriasis -  combining primary care and secondary care
    out_date_psoriasis=patients.minimum_of(
        "temp_out_date_psoriasis_ctv", "temp_out_date_psoriasis_hes"
    ),
    ## Hydradenitis suppurativa - snomed
    temp_out_date_hs_ctv= patients.with_these_clinical_events(
        hs_code_ctv,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Hydradenitis suppurativa - secondary care - hes
    temp_out_date_hs_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=hs_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Hydradenitis suppurativa -  combining primary care and secondary care
    out_date_hs =patients.minimum_of(
        "temp_out_date_hs_ctv", "temp_out_date_hs_hes"
    ),
    ## Outcome group 3: Inflammatory skin disease  
    out_date_grp3_isd=patients.minimum_of(
        "out_date_psoriasis",  "out_date_hs"
    ),
    ##################################################################################################
    ## Outcome group 4: Autoimmune GI / Inflammatory bowel disease                                  ##
    ##################################################################################################
    ## Inflammatory bowel disease (combined UC and Crohn's) - SNOMED
    temp_out_date_ibd_snomed= patients.with_these_clinical_events(
        ibd_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Inflammatory bowel disease (combined UC and Crohn's) - CTV3
    temp_out_date_ibd_ctv= patients.with_these_clinical_events(
        ibd_code_ctv3,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    # ## Inflammatory bowel disease (combined UC and Crohn's) - secondary care - hes
    # temp_out_date_ibd_hes=patients.admitted_to_hospital(
    #     returning="date_admitted",
    #     with_these_primary_diagnoses=ibd_code_hes,
    #     on_or_after=f"{index_date_variable}",
    #     date_format="YYYY-MM-DD",
    #     find_first_match_in_period=True,
    #     return_expectations={
    #         "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
    #         "rate": "uniform",
    #         "incidence": 0.3,
    #     },
    # ),
    ## Inflammatory bowel disease combined
    out_date_ibd=patients.minimum_of(
        "temp_out_date_ibd_snomed", "temp_out_date_ibd_ctv"
    ),
    ## Crohn’s disease snomed
    temp_out_date_crohn_snomed= patients.with_these_clinical_events(
        crohn_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Crohn’s disease - secondary care - hes
    temp_out_date_crohn_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=crohn_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Crohn’s disease combined
    out_date_crohn=patients.minimum_of(
        "temp_out_date_crohn_snomed", "temp_out_date_crohn_hes"
    ),
    ## Ulcerative colitis - snomed
    temp_out_date_uc_snomed= patients.with_these_clinical_events(
        uc_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Ulcerative colitis - secondary care - hes
    temp_out_date_uc_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=uc_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Ulcerative colitis combined
    out_date_uc=patients.minimum_of(
        "temp_out_date_uc_snomed", "temp_out_date_uc_hes"
    ),
    ## Celiac disease - snomed
    temp_out_date_celiac_snomed= patients.with_these_clinical_events(
        celiac_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Celiac disease - hes
    temp_out_date_celiac_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=celiac_code_icd ,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Celiac disease combined
    out_date_celiac=patients.minimum_of(
        "temp_out_date_celiac_snomed", "temp_out_date_celiac_hes"
    ),
    ## Outcome group 4: Autoimmune GI / Inflammatory bowel disease 
    out_date_grp4_agi_ibd=patients.minimum_of(
        "out_date_crohn", "out_date_uc", "out_date_celiac"
    ),
    ##################################################################################################
    ## Outcome group 5: Thyroid diseases                                                              #
    ##################################################################################################
    ## Addison’s disease - primary care
    temp_out_date_addison_snomed= patients.with_these_clinical_events(
        addison_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
     ## Addison’s disease - hes
    temp_out_date_addison_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=addison_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Addison’s disease combined
    out_date_addison=patients.minimum_of(
        "temp_out_date_addison_snomed", "temp_out_date_addison_hes"
    ),
    ## Grave’s disease - primary care
    temp_out_date_grave_snomed= patients.with_these_clinical_events(
        grave_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Grave’s disease - hes
    temp_out_date_grave_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=grave_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Grave’s disease combined
    out_date_grave=patients.minimum_of(
        "temp_out_date_grave_snomed", "temp_out_date_grave_hes"
    ),
    ## Hashimoto’s thyroiditis - snomed
    temp_out_date_hashimoto_thyroiditis_snomed = patients.with_these_clinical_events(
        hashimoto_thyroiditis_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Hashimoto’s thyroiditis - hes
    temp_out_date_hashimoto_thyroiditis_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=hashimoto_thyroiditis_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Hashimoto’s thyroiditis combined
    out_date_hashimoto_thyroiditis=patients.minimum_of(
        "temp_out_date_hashimoto_thyroiditis_snomed", "temp_out_date_hashimoto_thyroiditis_hes"
    ),
    ## Thyroid toxicosis / hyper thyroid - YW: This seems to have been taken out from the excel spreadsheet, 13/Dec/2022

    ## Outcome group 5: Thyroid diseases - to be expanded once the other outcome components are avilable
    out_date_grp5_atv=patients.minimum_of(
        "out_date_addison", "out_date_grave", "out_date_hashimoto_thyroiditis"
    ),
    ##################################################################################################
    ## Outcome group 6: Autoimmune vasculitis                                                       ##
    ##################################################################################################
    ## ANCA-associated - snomed
    temp_out_date_anca_snomed= patients.with_these_clinical_events(
        anca_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## ANCA-associated - hes
    temp_out_date_anca_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= anca_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## ANCA-associated  - combined
    out_date_anca =patients.minimum_of(
        "temp_out_date_anca_snomed", "temp_out_date_anca_hes"
    ),
    ## Giant cell arteritis - snomed
    temp_out_date_gca_snomed= patients.with_these_clinical_events(
        gca_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Giant cell arteritis - hes
    temp_out_date_gca_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= gca_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Giant cell arteritis - combined
    out_date_gca=patients.minimum_of(
        "temp_out_date_gca_snomed", "temp_out_date_gca_hes"
    ),
    ## IgA (immunoglobulin A) vasculitis - snomed
    temp_out_date_iga_vasculitis_snomed= patients.with_these_clinical_events(
        iga_vasculitis_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## IgA (immunoglobulin A) vasculitis - hes
    temp_out_date_iga_vasculitis_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= iga_vasculitis_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## IgA (immunoglobulin A) vasculitis - combined
    out_date_iga_vasculitis=patients.minimum_of(
        "temp_out_date_iga_vasculitis_snomed", "temp_out_date_iga_vasculitis_hes"
    ),
    ## Polymyalgia Rheumatica (PMR) - snomed
    temp_out_date_pmr_snomed= patients.with_these_clinical_events(
        pmr_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ##  Polymyalgia Rheumatica (PMR) - hes
    temp_out_date_pmr_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= pmr_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## IPolymyalgia Rheumatica (PMR) - combined
    out_date_pmr=patients.minimum_of(
        "temp_out_date_pmr_snomed", "temp_out_date_pmr_hes"
    ),
    ##  Outcome group 6: Autoimmune vasculitis - to be expanded once the other outcome components are avilable
    out_date_grp6_trd=patients.minimum_of(
        "out_date_anca", "out_date_gca","out_date_iga_vasculitis","out_date_pmr"
    ),
    ##################################################################################################
    ## Outcome group 7: Hematologic Diseases                                                        ##
    ##################################################################################################
    ## Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - snomed
    temp_out_date_immune_thromb_snomed= patients.with_these_clinical_events(
        immune_thromb_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - hes
    temp_out_date_immune_thromb_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= immune_thromb_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    # Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - combined
    out_date_immune_thromb=patients.minimum_of(
        "temp_out_date_immune_thromb_snomed", "temp_out_date_immune_thromb_hes"
    ),
    ## Pernicious anaemia - snomed
    temp_out_date_pernicious_anaemia_snomed= patients.with_these_clinical_events(
        pernicious_anaemia_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Pernicious anaemia - hes
    temp_out_date_pernicious_anaemia_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= pernicious_anaemia_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Pernicious anaemia combined
    out_date_pernicious_anaemia=patients.minimum_of(
        "temp_out_date_pernicious_anaemia_snomed", "temp_out_date_pernicious_anaemia_hes"
    ),
    ## Aplastic Anaemia - snomed
    temp_out_date_apa_snomed= patients.with_these_clinical_events(
        apa_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Aplastic Anaemia - ctv3
    temp_out_date_apa_ctv= patients.with_these_clinical_events(
        apa_code_ctv,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Aplastic Anaemia - hes
    temp_out_date_apa_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= apa_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Aplastic Anaemia combined
    out_date_apa=patients.minimum_of(
        "temp_out_date_apa_snomed", "temp_out_date_apa_ctv", "temp_out_date_apa_hes"
    ),
    ## Autoimmune haemolytic anaemia - snomed
    temp_out_date_aha_snomed= patients.with_these_clinical_events(
        aha_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Autoimmune haemolytic anaemia - hes
    temp_out_date_aha_hes =patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses= aha_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Autoimmune haemolytic anaemia combined
    out_date_aha =patients.minimum_of(
        "temp_out_date_aha_snomed", "temp_out_date_aha_hes"
    ),
    ## Outcome group 7: Hematologic Diseases - to be expanded once the other outcome components are avilable
    out_date_grp7_htd=patients.minimum_of(
        "out_date_immune_thromb", "out_date_pernicious_anaemia", "out_date_apa", "out_date_aha"
    ),
    ##################################################################################################
    ## Outcome group 8: Inflammatory neuromuscular disease                                          ##
    ##################################################################################################
    ## Guillain Barre - snomed
    temp_out_date_glb_snomed= patients.with_these_clinical_events(
        glb_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Guillain Barre - icd10
    temp_out_date_glb_hes= patients.admitted_to_hospital(
        with_these_diagnoses=glb_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.1,
        },
    ),
    ## Guillain Barre combined
    out_date_glb=patients.minimum_of(
        "temp_out_date_glb_snomed", "temp_out_date_glb_hes"
    ),
    ## Multiple Sclerosis - snomed
    temp_out_date_multiple_sclerosis_snomed= patients.with_these_clinical_events(
        multiple_sclerosis_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Multiple Sclerosis - hes
    temp_out_date_multiple_sclerosis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=multiple_sclerosis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.1,
        },
    ),
    ## Multiple Sclerosis combined
    out_date_multiple_sclerosis=patients.minimum_of(
        "temp_out_date_multiple_sclerosis_snomed", "temp_out_date_multiple_sclerosis_hes"
    ),
    ## Myasthenia gravis - snomed
    temp_out_date_myasthenia_gravis_snomed= patients.with_these_clinical_events(
        myasthenia_gravis_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Myasthenia gravis - hes
    temp_out_date_myasthenia_gravis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=myasthenia_gravis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.1,
        },
    ),
    ## Myasthenia gravis combined
    out_date_myasthenia_gravis=patients.minimum_of(
        "temp_out_date_myasthenia_gravis_snomed", "temp_out_date_myasthenia_gravis_hes"
    ),
    ## Longitudinal myelitis - snomed
    temp_out_date_longit_myelitis_snomed= patients.with_these_clinical_events(
        longit_myelitis_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Longitudinal myelitis - hes
    temp_out_date_longit_myelitis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=longit_myelitis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.1,
        },
    ),
    ## Longitudinal myelitis combined
    out_date_longit_myelitis=patients.minimum_of(
        "temp_out_date_longit_myelitis_snomed", "temp_out_date_longit_myelitis_hes"
    ),
    ## Clinically isolated syndrome - snomed
    temp_out_date_cis_snomed= patients.with_these_clinical_events(
        cis_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Clinically isolated syndrome - hes
    temp_out_date_cis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=cis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.1,
        },
    ),
    ## Clinically isolated syndrome combined
    out_date_cis=patients.minimum_of(
        "temp_out_date_cis_snomed", "temp_out_date_cis_hes"
    ),
    ## Outcome group 8: Inflammatory neuromuscular disease - to be expanded once codelist for other outcome components are available
    out_date_grp8_ind=patients.minimum_of(
        "out_date_glb", "out_date_multiple_sclerosis","out_date_myasthenia_gravis","out_date_longit_myelitis", "out_date_cis"
    ),
    ## Define primary outcome: composite auto-immune outcome
    out_date_composite_ai=patients.minimum_of(
        "out_date_grp1_ifa", "out_date_grp2_ctd", "out_date_grp3_isd", "out_date_grp4_agi_ibd", 
        "out_date_grp5_atv", "out_date_grp6_trd", "out_date_grp7_htd", "out_date_grp8_ind"
    ),
    )
    return dynamic_variables
