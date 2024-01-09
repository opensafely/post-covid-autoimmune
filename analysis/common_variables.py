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

def generate_common_variables(index_date_variable, exposure_end_date_variable, outcome_end_date_variable):
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

## Acute myocardial infarction
    ### Primary care
    tmp_cov_bin_ami_snomed=patients.with_these_clinical_events(
        ami_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_ami_prior_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=ami_prior_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    tmp_cov_bin_ami_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=ami_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_ami=patients.maximum_of(
        "tmp_cov_bin_ami_snomed", "tmp_cov_bin_ami_prior_hes", "tmp_cov_bin_ami_hes",
    ),

    ## All stroke
    ### Primary care
    tmp_cov_bin_stroke_isch_snomed=patients.with_these_clinical_events(
        stroke_isch_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    tmp_cov_bin_stroke_sah_hs_snomed=patients.with_these_clinical_events(
        stroke_sah_hs_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_stroke_isch_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=stroke_isch_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    tmp_cov_bin_stroke_sah_hs_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=stroke_sah_hs_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
        ### Combined
    cov_bin_all_stroke=patients.maximum_of(
        "tmp_cov_bin_stroke_isch_hes", "tmp_cov_bin_stroke_isch_snomed", "tmp_cov_bin_stroke_sah_hs_hes", "tmp_cov_bin_stroke_sah_hs_snomed",
    ),

    #     ### Combined Stroke Ischeamic
    # cov_bin_stroke_isch=patients.maximum_of(
    #     "tmp_cov_bin_stroke_isch_hes", "tmp_cov_bin_stroke_isch_snomed",
    # ),

    ## Dementia
    ### Primary care
    tmp_cov_bin_dementia_snomed=patients.with_these_clinical_events(
        dementia_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC (Hospital Episode Statistics Admitted Patient Care)
    tmp_cov_bin_dementia_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=dementia_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Primary care - vascular
    tmp_cov_bin_dementia_vascular_snomed=patients.with_these_clinical_events(
        dementia_vascular_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC - vascular
    tmp_cov_bin_dementia_vascular_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=dementia_vascular_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_dementia=patients.maximum_of(
        "tmp_cov_bin_dementia_snomed", "tmp_cov_bin_dementia_hes", "tmp_cov_bin_dementia_vascular_snomed", "tmp_cov_bin_dementia_vascular_hes",
    ),    

    ## Liver disease
     ### Primary care
    tmp_cov_bin_liver_disease_snomed=patients.with_these_clinical_events(
        liver_disease_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_liver_disease_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=liver_disease_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_liver_disease=patients.maximum_of(
        "tmp_cov_bin_liver_disease_snomed", "tmp_cov_bin_liver_disease_hes",
    ),

    ## Chronic kidney disease
    ### Primary care
    tmp_cov_bin_chronic_kidney_disease_snomed=patients.with_these_clinical_events(
        ckd_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_chronic_kidney_disease_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=ckd_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_chronic_kidney_disease=patients.maximum_of(
        "tmp_cov_bin_chronic_kidney_disease_snomed", "tmp_cov_bin_chronic_kidney_disease_hes",
    ),

    ## Cancer
    ### Primary care
    tmp_cov_bin_cancer_snomed=patients.with_these_clinical_events(
        cancer_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_cancer_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses=cancer_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_cancer=patients.maximum_of(
        "tmp_cov_bin_cancer_snomed", "tmp_cov_bin_cancer_hes",
    ),

    ## Hypertension
    ### Primary care
    tmp_cov_bin_hypertension_snomed=patients.with_these_clinical_events(
        hypertension_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_hypertension_hes=patients.admitted_to_hospital(
       returning='binary_flag',
       with_these_diagnoses=hypertension_icd10,
       on_or_before=f"{index_date_variable} - 1 day",
       return_expectations={"incidence": 0.1},
    ),
    ### DMD
    tmp_cov_bin_hypertension_drugs_dmd=patients.with_these_medications(
        hypertension_drugs_dmd,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_hypertension=patients.maximum_of(
        "tmp_cov_bin_hypertension_snomed", "tmp_cov_bin_hypertension_hes", "tmp_cov_bin_hypertension_drugs_dmd",
    ),

    ## Type 1 diabetes primary care
    cov_bin_diabetes_type1_snomed=patients.with_these_clinical_events(
        diabetes_type1_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ## Type 1 diabetes HES
    cov_bin_diabetes_type1_hes=patients.admitted_to_hospital(
       returning='binary_flag',
       with_these_diagnoses=diabetes_type1_icd10,
       on_or_before=f"{index_date_variable} - 1 day",
       return_expectations={"incidence": 0.1},
    ),
    ## Type 2 diabetes primary care
    cov_bin_diabetes_type2_snomed=patients.with_these_clinical_events(
        diabetes_type2_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ## Type 2 diabetes HES
    cov_bin_diabetes_type2_hes=patients.admitted_to_hospital(
       returning='binary_flag',
       with_these_diagnoses=diabetes_type2_icd10,
       on_or_before=f"{index_date_variable} - 1 day",
       return_expectations={"incidence": 0.1},
    ),
    ## Other or non-specific diabetes
    cov_bin_diabetes_other=patients.with_these_clinical_events(
        diabetes_other_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ## Gestational diabetes
    cov_bin_diabetes_gestational=patients.with_these_clinical_events(
        diabetes_gestational_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ## Diabetes medication
    tmp_cov_bin_insulin_snomed=patients.with_these_medications(
        insulin_snomed_clinical,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.05},
    ),

    tmp_cov_bin_antidiabetic_drugs_snomed=patients.with_these_medications(
        antidiabetic_drugs_snomed_clinical,
        returning="binary_flag",
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.05},
    ),

    ## Any diabetes covariate
    cov_bin_diabetes=patients.maximum_of(
        "cov_bin_diabetes_type1_snomed", "cov_bin_diabetes_type1_hes", 
        "cov_bin_diabetes_type2_snomed", "cov_bin_diabetes_type2_hes",
        "cov_bin_diabetes_other", "cov_bin_diabetes_gestational",
        "tmp_cov_bin_insulin_snomed", "tmp_cov_bin_antidiabetic_drugs_snomed",
    ),

        ## Prediabetes
    cov_bin_prediabetes=patients.with_these_clinical_events(
        prediabetes_snomed,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
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

## Chronic obstructive pulmonary disease
    ### Primary care
    tmp_cov_bin_chronic_obstructive_pulmonary_disease_snomed=patients.with_these_clinical_events(
        copd_snomed_clinical,
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### HES APC
    tmp_cov_bin_chronic_obstructive_pulmonary_disease_hes=patients.admitted_to_hospital(
        returning='binary_flag',
        with_these_diagnoses= copd_icd10,
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),
    ### Combined
    cov_bin_chronic_obstructive_pulmonary_disease=patients.maximum_of(
        "tmp_cov_bin_chronic_obstructive_pulmonary_disease_snomed", "tmp_cov_bin_chronic_obstructive_pulmonary_disease_hes",
    ),

    ## Combined oral contraceptive pill
    ### dmd: dictionary of medicines and devices
    cov_bin_combined_oral_contraceptive_pill=patients.with_these_medications(
        cocp_dmd, 
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
    ),

    ## Hormone replacement therapy
    cov_bin_hormone_replacement_therapy=patients.with_these_medications(
        hrt_dmd, 
        returning='binary_flag',
        on_or_before=f"{index_date_variable} - 1 day",
        return_expectations={"incidence": 0.1},
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

    ## 2019 outpatient rate
    cov_num_outpatient_rate = patients.outpatient_appointment_date(
        between = [days(study_dates["pandemic_start"], - 365), days(study_dates["pandemic_start"], -1)],
        returning = "number_of_matches_in_period",
        return_expectations ={
            "int": {"distribution": "poisson", "mean": 5},
        },
    ),

    ## Healthcare worker    
    cov_bin_healthcare_worker=patients.with_healthcare_worker_flag_on_covid_vaccine_record(
        returning='binary_flag', 
        return_expectations={"incidence": 0.01},
    ),

    # ## 2019 outpatient rate
    # cov_num_outpatient_rate = patients.outpatient_appointment_date(
    #     between = [days(study_dates["pandemic_start"], - 365), days(study_dates["pandemic_start"], -1)],
    #     returning = "number_of_matches_in_period",
    #     return_expectations ={
    #         "int": {"distribution": "poisson", "mean": 5},
    #     },
    # ),

    ##############################################################################################################################
    ## Define autoimune outcomes                                                                                                ##
    ##############################################################################################################################
    #################################################################################################
    ## Outcome group 1: Inflammatory arthritis                                                      ##
    #################################################################################################
    ## Reumatoid arthritis
    # Primary
    tmp_out_date_ra_snomed = patients.with_these_clinical_events(
        ra_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    # HES
    tmp_out_date_ra_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=ra_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    # ONS
    tmp_out_date_ra_death=patients.with_these_codes_on_death_certificate(
        ra_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    ## Reumatoid arthritis combining primary care and secondary care
    out_date_ra=patients.minimum_of(
        "tmp_out_date_ra_snomed", "tmp_out_date_ra_hes", "tmp_out_date_ra_death",
    ),
    ## Undifferentiated inflamatory arthritis - primary care
    tmp_out_date_undiff_eia = patients.with_these_clinical_events(
        undiff_eia_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    ## Undifferentiated inflamatory arthritis - no secondary care code

    ## Reumatoid arthritis combining primary care and secondary care
    out_date_undiff_eia=patients.minimum_of(
        "tmp_out_date_undiff_eia",
    ),

    ## Psoriatic arthritis - snomed
    tmp_out_date_psoa_snomed= patients.with_these_clinical_events(
        psoa_code_snomed,
        returning="date",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    ## Psoriatic arthritis - hes
    tmp_out_date_psoa_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=psoa_code_icd,
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    # ONS
   tmp_out_date_psoa_death=patients.with_these_codes_on_death_certificate(
       psoa_code_icd,
       returning="date_of_death",
       between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
       match_only_underlying_cause=True,
       date_format="YYYY-MM-DD",
       return_expectations={
           "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
           "rate": "uniform",
           "incidence": 0.5,
       },
   ),
    ## Psoriatic arthritis combining primary care and secondary care
    out_date_psoa=patients.minimum_of(
        "tmp_out_date_psoa_snomed", "tmp_out_date_psoa_hes", "tmp_out_date_psoa_death",
    ),
    ##  Axial spondyloarthritis - primary care
   tmp_out_date_axial_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_axial_hes=patients.admitted_to_hospital(
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
        # ONS
    tmp_out_date_axial_death=patients.with_these_codes_on_death_certificate(
        axial_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.5,
        },
    ),
    ## Axial spondyloarthritis -  combining primary care and secondary care
    out_date_axial=patients.minimum_of(
        "tmp_out_date_axial_snomed", 
        "tmp_out_date_axial_hes", "tmp_out_date_axial_death",
    ),
    ## Outcome group 1
    out_date_grp1_ifa=patients.minimum_of(
        "tmp_out_date_ra_snomed", "tmp_out_date_ra_hes", "tmp_out_date_ra_death",
        "tmp_out_date_undiff_eia",
        "tmp_out_date_psoa_snomed", 
        "tmp_out_date_psoa_hes", "tmp_out_date_psoa_death",
        "tmp_out_date_axial_snomed", 
        "tmp_out_date_axial_hes", "tmp_out_date_axial_death",
        # "out_date_ra", "out_date_undiff_eia", "out_date_psoa", "out_date_axial",
    ),
    #################################################################################################
    ## Outcome group 2: Connective tissue disorders                                                ##
    #################################################################################################
    ## Systematic lupus erythematosus - snomed
    tmp_out_date_sle_ctv= patients.with_these_clinical_events(
        sle_code_ctv,
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
    tmp_out_date_sle_hes=patients.admitted_to_hospital(
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
            # ONS
    tmp_out_date_sle_death=patients.with_these_codes_on_death_certificate(
        sle_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Systematic lupus erythematosus -  combining primary care and secondary care
    out_date_sle=patients.minimum_of(
        "tmp_out_date_sle_ctv", "tmp_out_date_sle_hes", "tmp_out_date_sle_death",
    ),
    ## Sjogren’s syndrome - snomed
    tmp_out_date_sjs_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_sjs_hes=patients.admitted_to_hospital(
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
                # ONS
    tmp_out_date_sjs_death=patients.with_these_codes_on_death_certificate(
        sjs_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Sjogren’s syndrome  -  combining primary care and secondary care
    out_date_sjs=patients.minimum_of(
        "tmp_out_date_sjs_snomed", "tmp_out_date_sjs_hes", "tmp_out_date_sjs_death",
    ),
    ## Systemic sclerosis/scleroderma - snomed
    tmp_out_date_sss_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_sss_hes=patients.admitted_to_hospital(
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
      # ONS
    tmp_out_date_sss_death=patients.with_these_codes_on_death_certificate(
        sss_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Systemic sclerosis/scleroderma -  combining primary care and secondary care
    out_date_sss=patients.minimum_of(
        "tmp_out_date_sss_snomed", "tmp_out_date_sss_hes", "tmp_out_date_sss_death",
    ),
    ## Inflammatory myositis/polymyositis/dermatolomyositis - snomed
    tmp_out_date_im_snomed = patients.with_these_clinical_events(
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
    tmp_out_date_im_hes=patients.admitted_to_hospital(
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
      # ONS
    tmp_out_date_im_death=patients.with_these_codes_on_death_certificate(
        im_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Inflammatory myositis/polymyositis/dermatolomyositis -  combining primary care and secondary care
    out_date_im=patients.minimum_of(
        "tmp_out_date_im_snomed", "tmp_out_date_im_hes", "tmp_out_date_im_death",
    ),
    ## Mixed Connective Tissue Disease - snomed
    tmp_out_date_mctd_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_mctd_hes=patients.admitted_to_hospital(
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
      # ONS
    tmp_out_date_mctd_death=patients.with_these_codes_on_death_certificate(
        mctd_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Mixed Connective Tissue Disease -  combining primary care and secondary care
    out_date_mctd=patients.minimum_of(
        "tmp_out_date_mctd_snomed", "tmp_out_date_mctd_hes", "tmp_out_date_mctd_death",
    ),
    ## Antiphospholipid syndrome - snomed
    tmp_out_date_as = patients.with_these_clinical_events(
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

    ## Mixed Connective Tissue Disease -  combining primary care and secondary care
    out_date_as=patients.minimum_of(
        "tmp_out_date_as",
    ),

    ## Outcome group 2
    out_date_grp2_ctd=patients.minimum_of(
        "tmp_out_date_sle_ctv", "tmp_out_date_sle_hes", "tmp_out_date_sle_death",
        "tmp_out_date_sjs_snomed", "tmp_out_date_sjs_hes", "tmp_out_date_sjs_death",
        "tmp_out_date_sss_snomed", "tmp_out_date_sss_hes", "tmp_out_date_sss_death", 
        "tmp_out_date_im_snomed", "tmp_out_date_im_hes", "tmp_out_date_im_death",
        "tmp_out_date_mctd_snomed", "tmp_out_date_mctd_hes", "tmp_out_date_mctd_death",
        "tmp_out_date_as",
        # "out_date_sle", "out_date_sjs", "out_date_sss", "out_date_im", "out_date_mctd", "out_date_as",
    ),
    #################################################################################################
    ## Outcome group 3: Inflammatory skin disease                                                  ##
    #################################################################################################
    ## Psoriasis - primary care - ctv3
    tmp_out_date_psoriasis_ctv= patients.with_these_clinical_events(
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
    tmp_out_date_psoriasis_hes=patients.admitted_to_hospital(
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
     # ONS
    tmp_out_date_psoriasis_death=patients.with_these_codes_on_death_certificate(
        psoriasis_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Psoriasis -  combining primary care and secondary care
    out_date_psoriasis=patients.minimum_of(
        "tmp_out_date_psoriasis_ctv", "tmp_out_date_psoriasis_hes", "tmp_out_date_psoriasis_death",
    ),
    ## Hydradenitis suppurativa - snomed
    tmp_out_date_hs_ctv= patients.with_these_clinical_events(
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
    tmp_out_date_hs_hes=patients.admitted_to_hospital(
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
     # ONS
    tmp_out_date_hs_death=patients.with_these_codes_on_death_certificate(
        hs_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Hydradenitis suppurativa -  combining primary care and secondary care
    out_date_hs =patients.minimum_of(
        "tmp_out_date_hs_ctv", "tmp_out_date_hs_hes", "tmp_out_date_hs_death",
    ),
    ## Outcome group 3: Inflammatory skin disease  
    out_date_grp3_isd=patients.minimum_of(
        "tmp_out_date_psoriasis_ctv", "tmp_out_date_psoriasis_hes", "tmp_out_date_psoriasis_death",
        "tmp_out_date_hs_ctv", "tmp_out_date_hs_hes", "tmp_out_date_hs_death",
        # "out_date_psoriasis",  "out_date_hs",
    ),
    ##################################################################################################
    ## Outcome group 4: Autoimmune GI / Inflammatory bowel disease                                  ##
    ##################################################################################################
    ## Inflammatory bowel disease (combined UC and Crohn's) - SNOMED
    tmp_out_date_ibd_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_ibd_ctv= patients.with_these_clinical_events(
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
    ## Inflammatory bowel disease (combined UC and Crohn's) - secondary care - hes
    tmp_out_date_ibd_hes=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_primary_diagnoses=ibd_code_icd,
        on_or_after=f"{index_date_variable}",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
      # ONS
    tmp_out_date_ibd_death=patients.with_these_codes_on_death_certificate(
        ibd_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Inflammatory bowel disease combined
    out_date_ibd=patients.minimum_of(
        "tmp_out_date_ibd_snomed", "tmp_out_date_ibd_ctv", "tmp_out_date_ibd_hes", "tmp_out_date_ibd_death",
    ),
    ## Crohn’s disease ctv
    tmp_out_date_crohn_ctv= patients.with_these_clinical_events(
        crohn_code_ctv,
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
    tmp_out_date_crohn_hes=patients.admitted_to_hospital(
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
      # ONS
    tmp_out_date_crohn_death=patients.with_these_codes_on_death_certificate(
        crohn_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Crohn’s disease combined
    out_date_crohn=patients.minimum_of(
        "tmp_out_date_crohn_ctv", "tmp_out_date_crohn_hes", "tmp_out_date_crohn_death",
    ),
    ## Ulcerative colitis - ctv
    tmp_out_date_uc_ctv= patients.with_these_clinical_events(
        uc_code_ctv,
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
    tmp_out_date_uc_hes=patients.admitted_to_hospital(
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
    # ONS
    tmp_out_date_uc_death=patients.with_these_codes_on_death_certificate(
        uc_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Ulcerative colitis combined
    out_date_uc=patients.minimum_of(
        "tmp_out_date_uc_ctv", "tmp_out_date_uc_hes", "tmp_out_date_uc_death",
    ),
    ## Celiac disease - snomed
    tmp_out_date_celiac_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_celiac_hes=patients.admitted_to_hospital(
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
        # ONS
    tmp_out_date_celiac_death=patients.with_these_codes_on_death_certificate(
        celiac_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Celiac disease combined
    out_date_celiac=patients.minimum_of(
        "tmp_out_date_celiac_snomed", "tmp_out_date_celiac_hes", "tmp_out_date_celiac_death",
    ),
    ## Outcome group 4: Autoimmune GI / Inflammatory bowel disease 
    out_date_grp4_agi_ibd=patients.minimum_of(
        "tmp_out_date_ibd_snomed", "tmp_out_date_ibd_ctv", "tmp_out_date_ibd_hes", "tmp_out_date_ibd_death",
        "tmp_out_date_crohn_ctv", "tmp_out_date_crohn_hes", "tmp_out_date_crohn_death",
        "tmp_out_date_uc_ctv", "tmp_out_date_uc_hes", "tmp_out_date_uc_death",
        "tmp_out_date_celiac_snomed", "tmp_out_date_celiac_hes", "tmp_out_date_celiac_death",
        # "out_date_ibd", "out_date_crohn", "out_date_uc", "out_date_celiac",
    ),
    ##################################################################################################
    ## Outcome group 5: Thyroid diseases                                                              #
    ##################################################################################################
    ## Addison’s disease - primary care
    tmp_out_date_addison_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_addison_hes=patients.admitted_to_hospital(
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
      # ONS
    tmp_out_date_addison_death=patients.with_these_codes_on_death_certificate(
        addison_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Addison’s disease combined
    out_date_addison=patients.minimum_of(
        "tmp_out_date_addison_snomed", "tmp_out_date_addison_hes", "tmp_out_date_addison_death",
    ),
    ## Grave’s disease - primary care
    tmp_out_date_grave_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_grave_hes=patients.admitted_to_hospital(
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
          # ONS
    tmp_out_date_grave_death=patients.with_these_codes_on_death_certificate(
        grave_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Grave’s disease combined
    out_date_grave=patients.minimum_of(
        "tmp_out_date_grave_snomed", "tmp_out_date_grave_hes", "tmp_out_date_grave_death",
    ),
    ## Hashimoto’s thyroiditis - snomed
    tmp_out_date_hashimoto_thyroiditis_snomed = patients.with_these_clinical_events(
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
    tmp_out_date_hashimoto_thyroiditis_hes =patients.admitted_to_hospital(
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
       # ONS
    tmp_out_date_hashimoto_thyroiditis_death=patients.with_these_codes_on_death_certificate(
        hashimoto_thyroiditis_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Hashimoto’s thyroiditis combined
    out_date_hashimoto_thyroiditis=patients.minimum_of(
        "tmp_out_date_hashimoto_thyroiditis_snomed", "tmp_out_date_hashimoto_thyroiditis_hes", "tmp_out_date_hashimoto_thyroiditis_death",
    ),
    ## Thyroid toxicosis / hyper thyroid - YW: This seems to have been taken out from the excel spreadsheet, 13/Dec/2022

    ## Outcome group 5: Thyroid diseases - to be expanded once the other outcome components are avilable
    out_date_grp5_atv=patients.minimum_of(
        "tmp_out_date_addison_snomed", "tmp_out_date_addison_hes","tmp_out_date_addison_death",
        "tmp_out_date_grave_snomed", "tmp_out_date_grave_hes", "tmp_out_date_grave_death",
        "tmp_out_date_hashimoto_thyroiditis_snomed", "tmp_out_date_hashimoto_thyroiditis_hes", "tmp_out_date_hashimoto_thyroiditis_death",
        # "out_date_addison", "out_date_grave", "out_date_hashimoto_thyroiditis",
    ),
    ##################################################################################################
    ## Outcome group 6: Autoimmune vasculitis                                                       ##
    ##################################################################################################
    ## ANCA-associated - snomed
    tmp_out_date_anca_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_anca_hes =patients.admitted_to_hospital(
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
    # ONS
    tmp_out_date_anca_death=patients.with_these_codes_on_death_certificate(
        anca_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## ANCA-associated  - combined
    out_date_anca =patients.minimum_of(
        "tmp_out_date_anca_snomed", "tmp_out_date_anca_hes", "tmp_out_date_anca_death",
    ),
    ## Giant cell arteritis - snomed
    tmp_out_date_gca_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_gca_hes =patients.admitted_to_hospital(
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
      # ONS
    tmp_out_date_gca_death=patients.with_these_codes_on_death_certificate(
        gca_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Giant cell arteritis - combined
    out_date_gca=patients.minimum_of(
        "tmp_out_date_gca_snomed", "tmp_out_date_gca_hes", "tmp_out_date_gca_death",
    ),
    ## IgA (immunoglobulin A) vasculitis - snomed
    tmp_out_date_iga_vasculitis_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_iga_vasculitis_hes =patients.admitted_to_hospital(
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
    # ONS
    tmp_out_date_iga_vasculitis_death=patients.with_these_codes_on_death_certificate(
        iga_vasculitis_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## IgA (immunoglobulin A) vasculitis - combined
    out_date_iga_vasculitis=patients.minimum_of(
        "tmp_out_date_iga_vasculitis_snomed", "tmp_out_date_iga_vasculitis_hes", "tmp_out_date_iga_vasculitis_death",
    ),
    ## Polymyalgia Rheumatica (PMR) - snomed
    tmp_out_date_pmr_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_pmr_hes =patients.admitted_to_hospital(
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
      # ONS
    tmp_out_date_pmr_death=patients.with_these_codes_on_death_certificate(
        pmr_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## IPolymyalgia Rheumatica (PMR) - combined
    out_date_pmr=patients.minimum_of(
        "tmp_out_date_pmr_snomed", "tmp_out_date_pmr_hes", "tmp_out_date_pmr_death",
    ),
    ##  Outcome group 6: Autoimmune vasculitis - to be expanded once the other outcome components are avilable
    out_date_grp6_trd=patients.minimum_of(
        "tmp_out_date_anca_snomed", "tmp_out_date_anca_hes", "tmp_out_date_anca_death",
        "tmp_out_date_gca_snomed", "tmp_out_date_gca_hes", "tmp_out_date_gca_death",
        "tmp_out_date_iga_vasculitis_snomed", "tmp_out_date_iga_vasculitis_hes", "tmp_out_date_iga_vasculitis_death",
        "tmp_out_date_pmr_snomed", "tmp_out_date_pmr_hes", "tmp_out_date_pmr_death",
        # "out_date_anca", "out_date_gca","out_date_iga_vasculitis","out_date_pmr",
    ),
    ##################################################################################################
    ## Outcome group 7: Hematologic Diseases                                                        ##
    ##################################################################################################
    ## Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - snomed
    tmp_out_date_immune_thromb_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_immune_thromb_hes =patients.admitted_to_hospital(
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
     # ONS
    tmp_out_date_immune_thromb_death=patients.with_these_codes_on_death_certificate(
        immune_thromb_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    # Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - combined
    out_date_immune_thromb=patients.minimum_of(
        "tmp_out_date_immune_thromb_snomed", "tmp_out_date_immune_thromb_hes", "tmp_out_date_immune_thromb_death",
    ),
    ## Pernicious anaemia - snomed
    tmp_out_date_pernicious_anaemia_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_pernicious_anaemia_hes =patients.admitted_to_hospital(
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
    # ONS
    tmp_out_date_pernicious_anaemia_death=patients.with_these_codes_on_death_certificate(
        pernicious_anaemia_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Pernicious anaemia combined
    out_date_pernicious_anaemia=patients.minimum_of(
        "tmp_out_date_pernicious_anaemia_snomed", "tmp_out_date_pernicious_anaemia_hes", "tmp_out_date_pernicious_anaemia_death",
    ),
    ## Aplastic Anaemia - snomed
    tmp_out_date_apa_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_apa_ctv= patients.with_these_clinical_events(
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
    tmp_out_date_apa_hes =patients.admitted_to_hospital(
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
       # ONS
    tmp_out_date_apa_death=patients.with_these_codes_on_death_certificate(
        apa_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Aplastic Anaemia combined
    out_date_apa=patients.minimum_of(
        "tmp_out_date_apa_snomed", "tmp_out_date_apa_ctv", "tmp_out_date_apa_hes", "tmp_out_date_apa_death",
    ),
    ## Autoimmune haemolytic anaemia - snomed
    tmp_out_date_aha_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_aha_hes =patients.admitted_to_hospital(
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
     # ONS
    tmp_out_date_aha_death=patients.with_these_codes_on_death_certificate(
        aha_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Autoimmune haemolytic anaemia combined
    out_date_aha =patients.minimum_of(
        "tmp_out_date_aha_snomed", "tmp_out_date_aha_hes", "tmp_out_date_aha_death",
    ),
    ## Outcome group 7: Hematologic Diseases - to be expanded once the other outcome components are avilable
    out_date_grp7_htd=patients.minimum_of(
        "tmp_out_date_immune_thromb_snomed", "tmp_out_date_immune_thromb_hes", "tmp_out_date_immune_thromb_death",
        "tmp_out_date_pernicious_anaemia_snomed", "tmp_out_date_pernicious_anaemia_hes", "tmp_out_date_pernicious_anaemia_death",
        "tmp_out_date_apa_snomed", "tmp_out_date_apa_ctv", "tmp_out_date_apa_hes", "tmp_out_date_apa_death",
        "tmp_out_date_aha_snomed", "tmp_out_date_aha_hes", "tmp_out_date_aha_death",
        # "out_date_immune_thromb", "out_date_pernicious_anaemia", "out_date_apa", "out_date_aha",
    ),
    ##################################################################################################
    ## Outcome group 8: Inflammatory neuromuscular disease                                          ##
    ##################################################################################################
    ## Guillain Barre - ctv
    tmp_out_date_glb_ctv= patients.with_these_clinical_events(
        glb_code_ctv,
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
    tmp_out_date_glb_hes= patients.admitted_to_hospital(
        with_these_diagnoses=glb_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
         # ONS
    tmp_out_date_glb_death=patients.with_these_codes_on_death_certificate(
        glb_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Guillain Barre combined
    out_date_glb=patients.minimum_of(
        "tmp_out_date_glb_ctv", "tmp_out_date_glb_hes", "tmp_out_date_glb_death",
    ),
    ## Multiple Sclerosis - ctv
    tmp_out_date_multiple_sclerosis_ctv= patients.with_these_clinical_events(
        multiple_sclerosis_code_ctv,
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
    tmp_out_date_multiple_sclerosis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=multiple_sclerosis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
     # ONS
    tmp_out_date_multiple_sclerosis_death=patients.with_these_codes_on_death_certificate(
        multiple_sclerosis_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Multiple Sclerosis combined
    out_date_multiple_sclerosis=patients.minimum_of(
        "tmp_out_date_multiple_sclerosis_ctv", "tmp_out_date_multiple_sclerosis_hes", "tmp_out_date_multiple_sclerosis_death",
    ),
    ## Myasthenia gravis - snomed
    tmp_out_date_myasthenia_gravis_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_myasthenia_gravis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=myasthenia_gravis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
      # ONS
    tmp_out_date_myasthenia_gravis_death=patients.with_these_codes_on_death_certificate(
        myasthenia_gravis_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Myasthenia gravis combined
    out_date_myasthenia_gravis=patients.minimum_of(
        "tmp_out_date_myasthenia_gravis_snomed", "tmp_out_date_myasthenia_gravis_hes", "tmp_out_date_myasthenia_gravis_death",
    ),
    ## Longitudinal myelitis - snomed
    tmp_out_date_longit_myelitis_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_longit_myelitis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=longit_myelitis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
     # ONS
    tmp_out_date_longit_myelitis_death=patients.with_these_codes_on_death_certificate(
        longit_myelitis_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Longitudinal myelitis combined
    out_date_longit_myelitis=patients.minimum_of(
        "tmp_out_date_longit_myelitis_snomed", "tmp_out_date_longit_myelitis_hes", "tmp_out_date_longit_myelitis_death",
    ),
    ## Clinically isolated syndrome - snomed
    tmp_out_date_cis_snomed= patients.with_these_clinical_events(
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
    tmp_out_date_cis_hes= patients.admitted_to_hospital(
        with_these_diagnoses=cis_code_icd,
        returning="date_admitted",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
      # ONS
    tmp_out_date_cis_death=patients.with_these_codes_on_death_certificate(
        cis_code_icd,
        returning="date_of_death",
        between=[f"{index_date_variable}",f"{outcome_end_date_variable}"],
        match_only_underlying_cause=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": study_dates["pandemic_start"], "latest" : "today"}, 
            "rate": "uniform",
            "incidence": 0.3,
        },
    ),
    ## Clinically isolated syndrome combined
    out_date_cis=patients.minimum_of(
        "tmp_out_date_cis_snomed", "tmp_out_date_cis_hes", "tmp_out_date_cis_death",
    ),
    ## Outcome group 8: Inflammatory neuromuscular disease - to be expanded once codelist for other outcome components are available
    out_date_grp8_ind=patients.minimum_of(
        "tmp_out_date_glb_ctv", "tmp_out_date_glb_hes", "tmp_out_date_glb_death",
        "tmp_out_date_multiple_sclerosis_ctv", "tmp_out_date_multiple_sclerosis_hes", "tmp_out_date_multiple_sclerosis_death",
        "tmp_out_date_myasthenia_gravis_snomed", "tmp_out_date_myasthenia_gravis_hes", "tmp_out_date_myasthenia_gravis_death",
        "tmp_out_date_longit_myelitis_snomed", "tmp_out_date_longit_myelitis_hes", "tmp_out_date_longit_myelitis_death",
        "tmp_out_date_cis_snomed", "tmp_out_date_cis_hes", "tmp_out_date_cis_death",
        # "out_date_glb", "out_date_multiple_sclerosis","out_date_myasthenia_gravis","out_date_longit_myelitis", "out_date_cis",
    ),
    
    # Define primary outcome: composite auto-immune outcome
    # out_date_composite_ai=patients.minimum_of(
    #     "out_date_grp1_ifa", "out_date_grp2_ctd", "out_date_grp3_isd", "out_date_grp4_agi_ibd",
    #     "out_date_grp5_atv", "out_date_grp6_trd", "out_date_grp7_htd", "out_date_grp8_ind"
    # ),
    ## Define primary outcome: composite auto-immune outcome
    out_date_composite_ai=patients.minimum_of(
        "tmp_out_date_ra_snomed", "tmp_out_date_ra_hes", 
        "tmp_out_date_undiff_eia",
        "tmp_out_date_psoa_snomed", 
        "tmp_out_date_psoa_hes", 
        "tmp_out_date_psoa_death",
        "tmp_out_date_axial_snomed", 
        "tmp_out_date_axial_hes", 
        "tmp_out_date_sle_ctv", "tmp_out_date_sle_hes", 
        "tmp_out_date_sjs_snomed", "tmp_out_date_sjs_hes", 
        "tmp_out_date_sss_snomed", "tmp_out_date_sss_hes", 
        "tmp_out_date_im_snomed", "tmp_out_date_im_hes", 
        "tmp_out_date_mctd_snomed", "tmp_out_date_mctd_hes", 
        "tmp_out_date_as",
        "tmp_out_date_psoriasis_ctv", "tmp_out_date_psoriasis_hes", 
        "tmp_out_date_hs_ctv", "tmp_out_date_hs_hes", 
        "tmp_out_date_ibd_snomed", "tmp_out_date_ibd_ctv", "tmp_out_date_ibd_hes", 
        "tmp_out_date_crohn_ctv", "tmp_out_date_crohn_hes", 
        "tmp_out_date_uc_ctv", "tmp_out_date_uc_hes", 
        "tmp_out_date_celiac_snomed", "tmp_out_date_celiac_hes", 
        "tmp_out_date_addison_snomed", "tmp_out_date_addison_hes",
        "tmp_out_date_grave_snomed", "tmp_out_date_grave_hes", 
        "tmp_out_date_hashimoto_thyroiditis_snomed", "tmp_out_date_hashimoto_thyroiditis_hes", 
        "tmp_out_date_anca_snomed", "tmp_out_date_anca_hes", 
        "tmp_out_date_gca_snomed", "tmp_out_date_gca_hes", 
        "tmp_out_date_iga_vasculitis_snomed", "tmp_out_date_iga_vasculitis_hes", 
        "tmp_out_date_pmr_snomed", "tmp_out_date_pmr_hes", 
        "tmp_out_date_immune_thromb_snomed", "tmp_out_date_immune_thromb_hes", 
        "tmp_out_date_pernicious_anaemia_snomed", "tmp_out_date_pernicious_anaemia_hes", 
        "tmp_out_date_apa_snomed", "tmp_out_date_apa_ctv", "tmp_out_date_apa_hes", 
        "tmp_out_date_aha_snomed", "tmp_out_date_aha_hes", 
        "tmp_out_date_glb_ctv", "tmp_out_date_glb_hes", 
        "tmp_out_date_multiple_sclerosis_ctv", "tmp_out_date_multiple_sclerosis_hes", 
        "tmp_out_date_myasthenia_gravis_snomed", "tmp_out_date_myasthenia_gravis_hes", 
        "tmp_out_date_longit_myelitis_snomed", "tmp_out_date_longit_myelitis_hes", 
        "tmp_out_date_cis_snomed", "tmp_out_date_cis_hes", 
        # "out_date_grp1_ifa", "out_date_grp2_ctd", "out_date_grp3_isd", "out_date_grp4_agi_ibd", 
        # "out_date_grp5_atv", "out_date_grp6_trd", "out_date_grp7_htd", "out_date_grp8_ind",
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
    # ONS

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
    # ONS

    ## Axial spondyloarthritis -  combining primary care and secondary care
    cov_bin_history_axial=patients.minimum_of(
        "tmp_cov_bin_history_axial_snomed", 
        "tmp_cov_bin_history_axial_hes", 
    ),

    ## History of Outcome group 1
    cov_bin_history_grp1_ifa=patients.minimum_of(
        "tmp_cov_bin_history_ra_snomed", "tmp_cov_bin_history_ra_hes", 
        "tmp_cov_bin_history_undiff_eia", "tmp_cov_bin_history_psoa_snomed", "tmp_cov_bin_history_psoa_hes", 
        "tmp_cov_bin_history_axial_snomed", 
        "tmp_cov_bin_history_axial_hes", 
        # "cov_bin_history_ra", "cov_bin_history_undiff_eia", "cov_bin_history_psoa", "cov_bin_history_axial",
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
    # ONS

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
    # ONS

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
      # ONS

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
      # ONS

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
      # ONS

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
        "tmp_cov_bin_history_sle_ctv", "tmp_cov_bin_history_sle_hes", 
        "tmp_cov_bin_history_sjs_snomed", "tmp_cov_bin_history_sjs_hes", 
        "tmp_cov_bin_history_sss_snomed", "tmp_cov_bin_history_sss_hes", 
        "tmp_cov_bin_history_im_snomed", "tmp_cov_bin_history_im_hes", 
        "tmp_cov_bin_history_mctd_snomed", "tmp_cov_bin_history_mctd_hes", 
        "tmp_cov_bin_history_as",
        # "cov_bin_history_sle", "cov_bin_history_sjs", "cov_bin_history_sss", "cov_bin_history_im", "cov_bin_history_mctd", "cov_bin_history_as",
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
     # ONS

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
     # ONS

    ## Hydradenitis suppurativa -  combining primary care and secondary care
    cov_bin_history_hs =patients.minimum_of(
        "tmp_cov_bin_history_hs_ctv", "tmp_cov_bin_history_hs_hes", 
    ),

    ## History of Outcome group 3: Inflammatory skin disease  
    cov_bin_history_grp3_isd=patients.minimum_of(
        "tmp_cov_bin_history_psoriasis_ctv", "tmp_cov_bin_history_psoriasis_hes", 
        "tmp_cov_bin_history_hs_ctv", "tmp_cov_bin_history_hs_hes", 
        # "cov_bin_history_psoriasis",  "cov_bin_history_hs"
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
      # ONS

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
      # ONS

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
    # ONS

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
        # ONS
    tmp_cov_bin_history_celiac_death=patients.with_these_codes_on_death_certificate(
        celiac_code_icd,
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
        "tmp_cov_bin_history_ibd_snomed", "tmp_cov_bin_history_ibd_ctv", "tmp_cov_bin_history_ibd_hes", 
        "tmp_cov_bin_history_crohn_ctv", "tmp_cov_bin_history_crohn_hes", 
        "tmp_cov_bin_history_uc_ctv", "tmp_cov_bin_history_uc_hes", 
        "tmp_cov_bin_history_celiac_snomed", "tmp_cov_bin_history_celiac_hes", 
        # "cov_bin_history_ibd", "cov_bin_history_crohn", "cov_bin_history_uc", "cov_bin_history_celiac",
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
      # ONS

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
          # ONS

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
       # ONS

    ## Hashimoto’s thyroiditis combined
    cov_bin_history_hashimoto_thyroiditis=patients.minimum_of(
        "tmp_cov_bin_history_hashimoto_thyroiditis_snomed", "tmp_cov_bin_history_hashimoto_thyroiditis_hes", 
    ),
    ## Thyroid toxicosis / hyper thyroid - YW: This seems to have been taken out from the excel spreadsheet, 13/Dec/2022

    ## History of Outcome group 5: Thyroid diseases - to be expanded once the other outcome components are avilable
    cov_bin_history_grp5_atv=patients.minimum_of(
        "tmp_cov_bin_history_addison_snomed", "tmp_cov_bin_history_addison_hes",
        "tmp_cov_bin_history_grave_snomed", "tmp_cov_bin_history_grave_hes", 
        "tmp_cov_bin_history_hashimoto_thyroiditis_snomed", "tmp_cov_bin_history_hashimoto_thyroiditis_hes", 
        # "cov_bin_history_addison", "cov_bin_history_grave", "cov_bin_history_hashimoto_thyroiditis",
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
    # ONS

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
      # ONS

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
    # ONS

    ## IgA (immunoglobulin A) vasculitis - combined
    cov_bin_history_iga_vasculitis=patients.minimum_of(
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
      # ONS

    ## IPolymyalgia Rheumatica (PMR) - combined
    cov_bin_history_pmr=patients.minimum_of(
        "tmp_cov_bin_history_pmr_snomed", "tmp_cov_bin_history_pmr_hes", 
    ),
    ##  History of Outcome group 6: Autoimmune vasculitis - to be expanded once the other outcome components are avilable
    cov_bin_history_grp6_trd=patients.minimum_of(
        "tmp_cov_bin_history_anca_snomed", "tmp_cov_bin_history_anca_hes", 
        "tmp_cov_bin_history_gca_snomed", "tmp_cov_bin_history_gca_hes", 
        "tmp_cov_bin_history_iga_vasculitis_snomed", "tmp_cov_bin_history_iga_vasculitis_hes", 
        "tmp_cov_bin_history_pmr_snomed", "tmp_cov_bin_history_pmr_hes", 
        # "cov_bin_history_anca", "cov_bin_history_gca","cov_bin_history_iga_vasculitis","cov_bin_history_pmr",
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
     # ONS

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
    # ONS

    ## Pernicious anaemia combined
    cov_bin_history_pernicious_anaemia=patients.minimum_of(
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
       # ONS

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
     # ONS

    ## Autoimmune haemolytic anaemia combined
    cov_bin_history_aha =patients.minimum_of(
        "tmp_out_date_aha_snomed", "tmp_out_date_aha_hes", 
    ),
    ## History of Outcome group 7: Hematologic Diseases - to be expanded once the other outcome components are avilable
    cov_bin_history_grp7_htd=patients.minimum_of(
        "tmp_cov_bin_history_immune_thromb_snomed", "tmp_cov_bin_history_immune_thromb_hes", 
        "tmp_cov_bin_history_pernicious_anaemia_snomed", "tmp_cov_bin_history_pernicious_anaemia_hes", 
        "tmp_cov_bin_history_apa_snomed", "tmp_cov_bin_history_apa_ctv", "tmp_cov_bin_history_apa_hes", 
        "tmp_cov_bin_history_aha_snomed", "tmp_cov_bin_history_aha_hes", 
        # "cov_bin_history_immune_thromb", "cov_bin_history_pernicious_anaemia", "cov_bin_history_apa", "cov_bin_history_aha",
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
         # ONS

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
     # ONS

    ## Multiple Sclerosis combined
    cov_bin_history_multiple_sclerosis=patients.minimum_of(
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
      # ONS

    ## Myasthenia gravis combined
    cov_bin_history_myasthenia_gravis=patients.minimum_of(
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
     # ONS

    ## Longitudinal myelitis combined
    cov_bin_history_longit_myelitis=patients.minimum_of(
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
      # ONS

    ## Clinically isolated syndrome combined
    cov_bin_history_cis=patients.minimum_of(
        "tmp_cov_bin_history_cis_snomed", "tmp_cov_bin_history_cis_hes", 
    ),
    ## Outcome group 8: Inflammatory neuromuscular disease - to be expanded once codelist for other outcome components are available
    cov_bin_history_grp8_ind=patients.minimum_of(
        "tmp_cov_bin_history_glb_ctv", "tmp_cov_bin_history_glb_hes", 
        "tmp_cov_bin_history_multiple_sclerosis_ctv", "tmp_cov_bin_history_multiple_sclerosis_hes", 
        "tmp_cov_bin_history_myasthenia_gravis_snomed", "tmp_cov_bin_history_myasthenia_gravis_hes", 
        "tmp_cov_bin_history_longit_myelitis_snomed", "tmp_cov_bin_history_longit_myelitis_hes", 
        "tmp_cov_bin_history_cis_snomed", "tmp_cov_bin_history_cis_hes", 
    #     "cov_bin_history_glb", "cov_bin_history_multiple_sclerosis", "cov_bin_history_myasthenia_gravis", 
    #     "cov_bin_history_longit_myelitis", "cov_bin_history_cis",
    # ),

#     ## Define primary outcome: composite auto-immune outcome
#     cov_bin_history_composite_ai=patients.minimum_of(
        "tmp_cov_bin_history_ra_snomed", "tmp_cov_bin_history_ra_hes", 
        "tmp_cov_bin_history_undiff_eia",
        "tmp_cov_bin_history_psoa_snomed", 
        "tmp_cov_bin_history_psoa_hes", 
        "tmp_cov_bin_history_axial_snomed", 
        "tmp_cov_bin_history_axial_hes", 
        "tmp_cov_bin_history_sle_ctv", "tmp_cov_bin_history_sle_hes", 
        "tmp_cov_bin_history_sjs_snomed", "tmp_cov_bin_history_sjs_hes", 
        "tmp_cov_bin_history_sss_snomed", "tmp_cov_bin_history_sss_hes", 
        "tmp_cov_bin_history_im_snomed", "tmp_cov_bin_history_im_hes", 
        "tmp_cov_bin_history_mctd_snomed", "tmp_cov_bin_history_mctd_hes", 
        "tmp_cov_bin_history_as",
        "tmp_cov_bin_history_psoriasis_ctv", "tmp_cov_bin_history_psoriasis_hes", 
        "tmp_cov_bin_history_hs_ctv", "tmp_cov_bin_history_hs_hes", 
        "tmp_cov_bin_history_ibd_snomed", "tmp_cov_bin_history_ibd_ctv", "tmp_cov_bin_history_ibd_hes", 
        "tmp_cov_bin_history_crohn_ctv", "tmp_cov_bin_history_crohn_hes", 
        "tmp_cov_bin_history_uc_ctv", "tmp_cov_bin_history_uc_hes", 
        "tmp_cov_bin_history_celiac_snomed", "tmp_cov_bin_history_celiac_hes", 
        "tmp_cov_bin_history_addison_snomed", "tmp_cov_bin_history_addison_hes",
        "tmp_cov_bin_history_grave_snomed", "tmp_cov_bin_history_grave_hes", 
        "tmp_cov_bin_history_hashimoto_thyroiditis_snomed", "tmp_cov_bin_history_hashimoto_thyroiditis_hes", 
        "tmp_cov_bin_history_anca_snomed", "tmp_cov_bin_history_anca_hes", 
        "tmp_cov_bin_history_gca_snomed", "tmp_cov_bin_history_gca_hes", 
        "tmp_cov_bin_history_iga_vasculitis_snomed", "tmp_cov_bin_history_iga_vasculitis_hes", 
        "tmp_cov_bin_history_pmr_snomed", "tmp_cov_bin_history_pmr_hes", 
        "tmp_cov_bin_history_immune_thromb_snomed", "tmp_cov_bin_history_immune_thromb_hes", 
        "tmp_cov_bin_history_pernicious_anaemia_snomed", "tmp_cov_bin_history_pernicious_anaemia_hes", 
        "tmp_cov_bin_history_apa_snomed", "tmp_cov_bin_history_apa_ctv", "tmp_cov_bin_history_apa_hes", 
        "tmp_cov_bin_history_aha_snomed", "tmp_cov_bin_history_aha_hes", 
        "tmp_cov_bin_history_glb_ctv", "tmp_cov_bin_history_glb_hes", 
        "tmp_cov_bin_history_multiple_sclerosis_ctv", "tmp_cov_bin_history_multiple_sclerosis_hes", 
        "tmp_cov_bin_history_myasthenia_gravis_snomed", "tmp_cov_bin_history_myasthenia_gravis_hes", 
        "tmp_cov_bin_history_longit_myelitis_snomed", "tmp_cov_bin_history_longit_myelitis_hes", 
        "tmp_cov_bin_history_cis_snomed", "tmp_cov_bin_history_cis_hes", 
#         "cov_bin_history_grp1_ifa", "cov_bin_history_grp2_ctd", "cov_bin_history_grp3_isd", "cov_bin_history_grp4_agi_ibd", 
#         "cov_bin_history_grp5_atv", "cov_bin_history_grp6_trd", "cov_bin_history_grp7_htd", "cov_bin_history_grp8_ind",
    ),

    )
    return dynamic_variables
