from os import system
from cohortextractor import codelist_from_csv, combine_codelists, codelist

#Covid
covid_codes = codelist_from_csv(
    "codelists/user-RochelleKnight-confirmed-hospitalised-covid-19.csv",
    system="icd10",
    column="code",
)

covid_primary_care_positive_test = codelist_from_csv(
    "codelists/opensafely-covid-identification-in-primary-care-probable-covid-positive-test.csv",
    system="ctv3",
    column="CTV3ID",
)

covid_primary_care_code = codelist_from_csv(
    "codelists/opensafely-covid-identification-in-primary-care-probable-covid-clinical-code.csv",
    system="ctv3",
    column="CTV3ID",
)

covid_primary_care_sequalae = codelist_from_csv(
    "codelists/opensafely-covid-identification-in-primary-care-probable-covid-sequelae.csv",
    system="ctv3",
    column="CTV3ID",
)
#Ethnicity
opensafely_ethnicity_codes_6 = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_6",
)

primis_covid19_vacc_update_ethnicity = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-eth2001.csv",
    system="snomed",
    column="code",
    category_column="grouping_6_id",
)
#Smoking
smoking_clear = codelist_from_csv(
    "codelists/opensafely-smoking-clear.csv",
    system="ctv3",
    column="CTV3Code",
    category_column="Category",
)

smoking_unclear = codelist_from_csv(
    "codelists/opensafely-smoking-unclear.csv",
    system="ctv3",
    column="CTV3Code",
    category_column="Category",
)

# AMI
ami_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-ami_snomed.csv",
    system="snomed",
    column="code",
)
ami_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-ami_icd10.csv",
    system="icd10",
    column="code",
)
ami_prior_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-ami_prior_icd10.csv",
    system="icd10",
    column="code",
)
artery_dissect_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-artery_dissect_icd10.csv",
    system="icd10",
    column="code",
)

# Cancer
cancer_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-cancer_snomed.csv",
    system="snomed",
    column="code",
)
cancer_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-cancer_icd10.csv",
    system="icd10",
    column="code",
)

# Cardiomyopathy
cardiomyopathy_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-cardiomyopathy_snomed.csv",
    system="snomed",
    column="code",
)
cardiomyopathy_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-cardiomyopathy_icd10.csv",
    system="icd10",
    column="code",
)

# COPD
copd_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-copd_snomed.csv",
    system="snomed",
    column="code",
)
copd_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-copd_icd10.csv",
    system="icd10",
    column="code",
)

# Dementia
dementia_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-dementia_snomed.csv",
    system="snomed",
    column="code",
)
dementia_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-dementia_icd10.csv",
    system="icd10",
    column="code",
)

#Disseminated intravascular coagulation
dic_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-dic_icd10.csv",
    system="icd10",
    column="code",
)

# Pulmonary embolism
pe_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-pe_icd10.csv",
    system="icd10",
    column="code",
)
pe_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-pe_snomed.csv",
    system="snomed",
    column="code",
)

# Deep vein thrombosis
dvt_dvt_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-dvt_dvt_icd10.csv",
    system="icd10",
    column="code",
)
dvt_icvt_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-dvt_icvt_icd10.csv",
    system="icd10",
    column="code",
)
dvt_icvt_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-dvt_icvt_snomed.csv",
    system="snomed",
    column="code",
)
dvt_pregnancy_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-dvt_pregnancy_icd10.csv",
    system="icd10",
    column="code",
)
other_dvt_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-other_dvt_icd10.csv",
    system="icd10",
    column="code",
)
# DVT
dvt_dvt_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-dvt_main.csv",
    system="snomed",
    column="code",
)
# ICVT
dvt_icvt_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-dvt_icvt.csv",
    system="snomed",
    column="code",
)
# DVT in pregnancy
dvt_pregnancy_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-dvt-preg.csv",
    system="snomed",
    column="code",
)
# Other DVT
other_dvt_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-dvt-other.csv",
    system="snomed",
    column="code",
)

# Portal vein thrombosis
portal_vein_thrombosis_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-pvt.csv",
    system="snomed",
    column="code",
)
portal_vein_thrombosis_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-portal_vein_thrombosis_icd10.csv",
    system="icd10",
    column="code",
)

icvt_pregnancy_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-icvt_pregnancy_icd10.csv",
    system="icd10",
    column="code",
)

# Other arterial embolism
other_arterial_embolism_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-other_art_embol.csv",
    system="snomed",
    column="code",
)

stroke_isch_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-stroke_isch_snomed.csv",
    system="snomed",
    column="code",
)

other_arterial_embolism_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-other_arterial_embolism_icd10.csv",
    system="icd10",
    column="code",
)

stroke_isch_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-stroke_isch_icd10.csv",
    system="icd10",
    column="code",
)

# All DVT in SNOMED
all_dvt_codes_snomed_clinical = combine_codelists(
    dvt_dvt_snomed_clinical, 
    dvt_pregnancy_snomed_clinical
)

# All DVT in ICD10
all_dvt_codes_icd10 = combine_codelists(
    dvt_dvt_icd10, 
    dvt_pregnancy_icd10
)

# All VTE in SNOMED
all_vte_codes_snomed_clinical = combine_codelists(
    portal_vein_thrombosis_snomed_clinical, 
    dvt_dvt_snomed_clinical, 
    dvt_icvt_snomed_clinical, 
    dvt_pregnancy_snomed_clinical, 
    other_dvt_snomed_clinical, 
    pe_snomed_clinical
)

# All VTE in ICD10
all_vte_codes_icd10 = combine_codelists(
    portal_vein_thrombosis_icd10, 
    dvt_dvt_icd10, 
    dvt_icvt_icd10, 
    dvt_pregnancy_icd10, 
    other_dvt_icd10, 
    icvt_pregnancy_icd10, 
    pe_icd10
)

# All ATE in SNOMED
all_ate_codes_snomed_clinical = combine_codelists(
    ami_snomed_clinical, 
    other_arterial_embolism_snomed_clinical, 
    stroke_isch_snomed_clinical
)

# All ATE in ICD10
all_ate_codes_icd10 = combine_codelists(
    ami_icd10, 
    other_arterial_embolism_icd10, 
    stroke_isch_icd10
)

# Intracranial venous thrombosis
icvt_pregnancy_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-icvt_pregnancy_icd10.csv",
    system="icd10",
    column="code",
)

# Vein thrombosis
portal_vein_thrombosis_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-portal_vein_thrombosis_icd10.csv",
    system="icd10",
    column="code",
)
vt_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-vt_icd10.csv",
    system="icd10",
    column="code",
)
thrombophilia_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-thrombophilia_icd10.csv",
    system="icd10",
    column="code",
)
thrombophilia_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-thrombophilia_snomed.csv",
    system="snomed",
    column="code",
)
tcp_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-tcp_snomed.csv",
    system="snomed",
    column="code",
)
ttp_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-ttp_icd10.csv",
    system="icd10",
    column="code",
)
thrombocytopenia_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-thrombocytopenia_icd10.csv",
    system="icd10",
    column="code",
)
# Portal vein thrombosis
portal_vein_thrombosis_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-pvt.csv",
    system="snomed",
    column="code",
)

# Dementia vascular 
dementia_vascular_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-dementia_vascular_snomed.csv",
    system="snomed",
    column="code",
)

dementia_vascular_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-dementia_vascular_icd10.csv",
    system="icd10",
    column="code",
)

# Liver disease
liver_disease_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-liver_disease_snomed.csv",
    system="snomed",
    column="code",
)
liver_disease_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-liver_disease_icd10.csv",
    system="icd10",
    column="code",
)

# Antiplatelet 
antiplatelet_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-antiplatelet_dmd.csv",
    system="snomed",
    column="code",
)

# Lipid Lowering
lipid_lowering_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-lipid_lowering_dmd.csv",
    system="snomed",
    column="code",
)

# Anticoagulant
anticoagulant_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-anticoagulant_dmd.csv",
    system="snomed",
    column="code",
)

# COCP
cocp_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-cocp_dmd.csv",
    system="snomed",
    column="code",
)

# HRT
hrt_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-hrt_dmd.csv",
    system="snomed",
    column="code",
)

# Arterial Embolism
other_arterial_embolism_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-other_arterial_embolism_icd10.csv",
    system="icd10",
    column="code",
)
# Other arterial embolism
other_arterial_embolism_snomed_clinical = codelist_from_csv(
    "codelists/user-tomsrenin-other_art_embol.csv",
    system="snomed",
    column="code",
)

# Mesenteric Thrombus
mesenteric_thrombus_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-mesenteric_thrombus_icd10.csv",
    system="icd10",
    column="code",
)

# Arrhytmia
life_arrhythmia_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-life_arrhythmia_icd10.csv",
    system="icd10",
    column="code",
)

# Pericarditis
pericarditis_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-pericarditis_icd10.csv",
    system="icd10",
    column="code",
)

# Myocarditis
myocarditis_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-myocarditis_icd10.csv",
    system="icd10",
    column="code",
)

# HYpertension
hypertension_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-hypertension_icd10.csv",
    system="icd10",
    column="code",
)
hypertension_drugs_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-hypertension_drugs_dmd.csv",
    system="snomed",
    column="code",
)
hypertension_snomed_clinical = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv",
    system="snomed",
    column="code",
)

# TIA
tia_snomed_clinical = codelist_from_csv(
    "codelists/user-hjforbes-tia_snomed.csv",
    system="snomed",
    column="code",
)
tia_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-tia_icd10.csv",
    system="icd10",
    column="code",
)

# Angina
angina_snomed_clinical = codelist_from_csv(
    "codelists/user-hjforbes-angina_snomed.csv",
    system="snomed",
    column="code",
)
angina_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-angina_icd10.csv",
    system="icd10",
    column="code",
)

# Prostate
prostate_cancer_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-prostate_cancer_icd10.csv",
    system="icd10",
    column="code",
)
prostate_cancer_snomed_clinical = codelist_from_csv(
    "codelists/user-RochelleKnight-prostate_cancer_snomed.csv",
    system="snomed",
    column="code",
)

# Pregnancy
pregnancy_snomed_clinical = codelist_from_csv(
    "codelists/user-RochelleKnight-pregnancy_and_birth_snomed.csv",
    system="snomed",
    column="code",
)

# Heart Failure
hf_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-hf_snomed.csv",
    system="snomed",
    column="code",
)
hf_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-hf_icd10.csv",
    system="icd10",
    column="code",
)

# Stroke 
stroke_isch_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-stroke_isch_icd10.csv",
    system="icd10",
    column="code",
)
stroke_isch_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-stroke_isch_snomed.csv",
    system="snomed",
    column="code",
)
stroke_sah_hs_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-stroke_sah_hs_icd10.csv",
    system="icd10",
    column="code",
)
stroke_sah_hs_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-stroke_sah_hs_snomed.csv",
    system="snomed",
    column="code",
)

# BMI
bmi_obesity_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-bmi_obesity_snomed.csv",
    system="snomed",
    column="code",
)

bmi_obesity_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-bmi_obesity_icd10.csv",
    system="icd10",
    column="code",
)

bmi_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-bmi.csv",
    system="snomed",
    column="code",
)

# Total Cholesterol
cholesterol_snomed = codelist_from_csv(
    "codelists/opensafely-cholesterol-tests-numerical-value.csv",
    system="snomed",
    column="code",
)

# HDL Cholesterol
hdl_cholesterol_snomed = codelist_from_csv(
    "codelists/bristol-hdl-cholesterol.csv",
    system="snomed",
    column="code",
)
# Carer codes
carer_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-carer.csv",
    system="snomed",
    column="code",
)

# No longer a carer codes
notcarer_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-notcarer.csv",
    system="snomed",
    column="code",
)
# Wider Learning Disability
learndis_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-learndis.csv",
    system="snomed",
    column="code",
)
# Employed by Care Home codes
carehome_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-carehome.csv",
    system="snomed",
    column="code",
)

# Employed by nursing home codes
nursehome_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-nursehome.csv",
    system="snomed",
    column="code",
)

# Employed by domiciliary care provider codes
domcare_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-domcare.csv",
    system="snomed",
    column="code",
)

# Patients in long-stay nursing and residential care
longres_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-longres.csv",
    system="snomed",
    column="code",
)
# High Risk from COVID-19 code
shield_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-shield.csv",
    system="snomed",
    column="code",
)

# Lower Risk from COVID-19 codes
nonshield_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-nonshield.csv",
    system="snomed",
    column="code",
)

#For JCVI groups
# Pregnancy codes 
preg_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-preg.csv",
    system="snomed",
    column="code",
)

# Pregnancy or Delivery codes
pregdel_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-pregdel.csv",
    system="snomed",
    column="code",
)
# All BMI coded terms
bmi_stage_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-bmi_stage.csv",
    system="snomed",
    column="code",
)
# Severe Obesity code recorded
sev_obesity_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-sev_obesity.csv",
    system="snomed",
    column="code",
)
# Asthma Diagnosis code
ast_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-ast.csv",
    system="snomed",
    column="code",
)

# Asthma Admission codes
astadm_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-astadm.csv",
    system="snomed",
    column="code",
)

# Asthma systemic steroid prescription codes
astrx_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-astrx.csv",
    system="snomed",
    column="code",
)
# Chronic Respiratory Disease
resp_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-resp_cov.csv",
    system="snomed",
    column="code",
)
# Chronic Neurological Disease including Significant Learning Disorder
cns_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-cns_cov.csv",
    system="snomed",
    column="code",
)

# Asplenia or Dysfunction of the Spleen codes
spln_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-spln_cov.csv",
    system="snomed",
    column="code",
)
# Diabetes diagnosis codes
diab_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-diab.csv",
    system="snomed",
    column="code",
)
# Diabetes resolved codes
dmres_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-dmres.csv",
    system="snomed",
    column="code",
)
# Severe Mental Illness codes
sev_mental_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-sev_mental.csv",
    system="snomed",
    column="code",
)

# Remission codes relating to Severe Mental Illness
smhres_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-smhres.csv",
    system="snomed",
    column="code",
)

# Chronic heart disease codes
chd_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-chd_cov.csv",
    system="snomed",
    column="code",
)

# Chronic Kidney disease
ckd_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-ckd_snomed.csv",
    system="snomed",
    column="code",
)

ckd_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-ckd_icd10.csv",
    system="icd10",
    column="code",
)

# Chronic kidney disease diagnostic codes
ckd_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-ckd_cov.csv",
    system="snomed",
    column="code",
)

# Chronic kidney disease codes - all stages
ckd15_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-ckd15.csv",
    system="snomed",
    column="code",
)

# Chronic kidney disease codes-stages 3 - 5
ckd35_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-ckd35.csv",
    system="snomed",
    column="code",
)

# Chronic Liver disease codes
cld_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-cld.csv",
    system="snomed",
    column="code",
)
# Immunosuppression diagnosis codes
immdx_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-immdx_cov.csv",
    system="snomed",
    column="code",
)

# Immunosuppression medication codes
immrx_primis = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-immrx.csv",
    system="snomed",
    column="code",
)

# Diabetes
# Type 1 diabetes
diabetes_type1_snomed_clinical = codelist_from_csv(
    "codelists/user-hjforbes-type-1-diabetes.csv",
    system="ctv3",
    column="code",
)
# Type 1 diabetes secondary care
diabetes_type1_icd10 = codelist_from_csv(
    "codelists/opensafely-type-1-diabetes-secondary-care.csv",
    system="icd10",
    column="icd10_code",
)
# Type 2 diabetes
diabetes_type2_snomed_clinical = codelist_from_csv(
    "codelists/user-hjforbes-type-2-diabetes.csv",
    system="ctv3",
    column="code",
)
# Type 2 diabetes secondary care
diabetes_type2_icd10 = codelist_from_csv(
    "codelists/user-r_denholm-type-2-diabetes-secondary-care-bristol.csv",
    system="icd10",
    column="code",
)
# Non-diagnostic diabetes codes
diabetes_diagnostic_snomed_clinical = codelist_from_csv(
    "codelists/user-hjforbes-nondiagnostic-diabetes-codes.csv",
    system="ctv3",
    column="code",
)
# Other or non-specific diabetes
diabetes_other_snomed_clinical = codelist_from_csv(
    "codelists/user-hjforbes-other-or-nonspecific-diabetes.csv",
    system="ctv3",
    column="code",
)
# Gestational diabetes
diabetes_gestational_snomed_clinical = codelist_from_csv(
    "codelists/user-hjforbes-gestational-diabetes.csv",
    system="ctv3",
    column="code",
)
# Insulin medication 
insulin_snomed_clinical = codelist_from_csv(
     "codelists/opensafely-insulin-medication.csv",
     system="snomed",
     column="code",
)
# Antidiabetic drugs
antidiabetic_drugs_snomed_clinical = codelist_from_csv(
     "codelists/opensafely-antidiabetic-drugs.csv",
     system="snomed",
     column="code",
)
# Antidiabetic drugs - non metformin
non_metformin_dmd = codelist_from_csv(
    "codelists/user-r_denholm-non-metformin-antidiabetic-drugs_bristol.csv", 
    system="snomed", 
    column="code",
)
# Prediabetes
prediabetes_snomed = codelist_from_csv(
    "codelists/opensafely-prediabetes-snomed.csv",
    system="snomed",
    column="code",
)

##Quality assurance codes 

prostate_cancer_snomed_clinical = codelist_from_csv(
    "codelists/user-RochelleKnight-prostate_cancer_snomed.csv",
    system="snomed",
    column="code",
)
prostate_cancer_icd10 = codelist_from_csv(
    "codelists/user-RochelleKnight-prostate_cancer_icd10.csv",
    system="icd10",
    column="code",
)
pregnancy_snomed_clinical = codelist_from_csv(
    "codelists/user-RochelleKnight-pregnancy_and_birth_snomed.csv",
    system="snomed",
    column="code",
)
##################################################################################################################################
# Autoimmune disease codes                                                                                                       #
################################################################################################################################## 

##################################################################################################
# Outcome group 1:  Inflammatory arthritis                                                       #
##################################################################################################
# Reumatoid arthritis - snomed
ra_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-polymyalgia-rheumatica.csv",
    system="snomed",
    column="code",
)
# Reumatoid arthritis - icd
ra_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-arthritis-rheumatoid-arthritis-icd10.csv",
    system="icd10",
    column="code",
)
# Undifferentiated inflamatory arthritis - snomed
undiff_eia_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-undiff-eia.csv",
    system="snomed",
    column="code",
)
# undifferentiated inflmatory arthritis - no icd10 codelist for this disease, 14 Dec 2022 YW

# Psoriatic arthritis - snomed
psoa_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-psoriatic-arthritis.csv",
    system = "snomed",
    column = "code",
)
# Psoriatic arthritis - icd10 
psoa_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-arthritis-psoriatic-arthritis-icd10.csv",
    system = "icd10",
    column = "code",
)
# Axial spondyloarthritis - snomed
axial_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-axial-spondyloarthritis.csv",
    system = "snomed",
    column = "code",
)
# Axial spondyloarthritis - hes
axial_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-arthritis-axial-spondyloarthritis-icd10.csv",
    system = "icd10",
    column = "code",
)
##################################################################################################
# Outcome group 2:  Connective tissue disorders                                                  #
##################################################################################################
# Systematic lupus erythematosu - ctv
sle_code_ctv = codelist_from_csv(
    "codelists/opensafely-systemic-lupus-erythematosus-sle.csv",#user-markdrussell-systemic-sclerosisscleroderma.csv",
    system="ctv3",
    column="CTV3ID",
)
# Systematic lupus erythematosu - hes
sle_code_icd = codelist_from_csv(
    "codelists/user-josephignace-connective-tissue-disorders-systematic-lupus-erythematosus.csv",
    system="icd10",
    column="code",
)
#Sjogren’s syndrome - snomed
sjs_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-sjogrens-syndrome.csv",
    system="snomed",
    column="code",
)
#Sjogren’s syndrome - hes
sjs_code_icd = codelist_from_csv(
    "codelists/user-josephignace-connective-tissue-disorders-sjogrens-syndrome.csv",
    system="icd10",
    column="code",
)
#Systemic sclerosis/scleroderma - snomed
sss_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-systemic-sclerosisscleroderma.csv",
    system="snomed",
    column="code",
)
#Systemic sclerosis/scleroderma - hes
sss_code_icd = codelist_from_csv(
    "codelists/user-josephignace-connective-tissue-disorders-systemic-sclerosisscleroderma.csv",
    system="icd10",
    column="code",
)
# Inflammatory myositis/polymyositis/dermatolomyositis - snomed
im_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-inflammatory-myositis.csv",
    system="snomed",
    column="code",
)
# Inflammatory myositis/polymyositis/dermatolomyositis - hes
im_code_icd = codelist_from_csv(
    "codelists/user-josephignace-connective-tissue-disorders-inflammatory-myositispolymyositisdermatolomyositis.csv",
    system="icd10",
    column="code",
)
# Mixed Connective Tissue Disease - snomed
mctd_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-mctd.csv",
    system="snomed",
    column="code",
)
# Mixed Connective Tissue Disease - hes
mctd_code_icd = codelist_from_csv(
    "codelists/user-josephignace-connective-tissue-disorders-mixed-connective-tissue-disease.csv",
    system="icd10",
    column="code",
)
# Antiphospholipid syndrome - snomed
as_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-antiphospholipid-syndrome.csv",
    system="snomed",
    column="code",
)
# Antiphospholipid syndrome - no icd10 code
##################################################################################################
# Outcome group 3: Inflammatory skin disease                                                     #
##################################################################################################
## Psoriasis - primary care - ctv3
psoriasis_code_ctv = codelist_from_csv(
    "codelists/opensafely-psoriasis.csv",
    system="ctv3",
    column="code",
)
## Psoriasis - secondary care - icd10
psoriasis_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-skin-disease-psoriasis.csv",
    system="icd10",
    column="code",
)
## Hydradenitis suppurativa - ctv3
hs_code_ctv = codelist_from_csv(
    "codelists/opensafely-hidradenitis-suppurativa.csv",
    system="ctv3",
    column="CTV3ID",
)
## Hydradenitis suppurativa - hes
hs_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-skin-disease-hidradenitis-suppurativa-icd10.csv",
    system="icd10",
    column="code",
)
##################################################################################################
# Outcome group 4: Autoimmune GI/Inflammatory bowel disease                                      #
##################################################################################################
# Inflammatory bowel disease (combined UC and Crohn's) - snomed
ibd_code_snomed = codelist_from_csv(
    "codelists/opensafely-inflammatory-bowel-disease-snomed.csv",
    system="snomed",
    column="id",
)
# Inflammatory bowel disease (combined UC and Crohn's) - ctv3
ibd_code_ctv3 = codelist_from_csv(
    "codelists/opensafely-inflammatory-bowel-disease.csv",
    system="ctv3",
    column="CTV3ID",
)
# YW notes 17 Jan 2023: the ICD10 codelist for IBD doesn't work: 
# https://www.opencodelists.org/codelist/user/josephignace/autoimmune-gi-inflammatory-bowel-disease-inflammatory-bowel-disease-combined-uc-and-crohns/7224b1b6/
ibd_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-gi-inflammatory-bowel-disease-inflammatory-bowel-disease-combined-uc-and-crohns.csv",
    system = "icd10",
    column = "code",
)

# Crohn's disease - ctv
crohn_code_ctv = codelist_from_csv(
    "codelists/opensafely-crohns-disease.csv",
    system="ctv3",
    column="code",
)
# Crohn's disease - hes
crohn_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-gi-inflammatory-bowel-disease-crohns-disease-icd10.csv",
    system="icd10",
    column="code",
)
# Ulcerative colitis - ctv
uc_code_ctv = codelist_from_csv(
    "codelists/opensafely-ulcerative-colitis.csv",
    system="ctv3",
    column="code",
)
# Ulcerative colitis - hes
uc_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-gi-inflammatory-bowel-disease-ulcerative-colitis-icd10.csv",
    system="icd10",
    column="code",
)
# Celiac disease - snomed
celiac_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-celiaccoeliac-disease.csv",
    system="snomed",
    column="code",
)
# Celiac disease - hes
celiac_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-gi-inflammatory-bowel-disease-celiac-disease-icd10.csv",
    system="icd10",
    column="code",
)
##################################################################################################
# Outcome group 5: Thyroid diseases                                                              #
##################################################################################################
# Addison’s disease - snomed
addison_code_snomed = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-addis_cod.csv",
    system="snomed",
    column="code",
)
# Addison’s disease - hes
addison_code_icd= codelist_from_csv(
    "codelists/user-josephignace-thyroid-diseases-addisons-disease-icd10.csv",
    system="icd10",
    column="code",
)
# Grave’s disease - snomed
grave_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-graves-disease.csv",
    system="snomed",
    column="code",
)
# Grave’s disease - hes
grave_code_icd = codelist_from_csv(
    "codelists/user-josephignace-thyroid-diseases-graves-disease-icd10.csv",
    system="icd10",
    column="code",
)
# Hashimoto’s thyroiditis - snomed
hashimoto_thyroiditis_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-hashimotos-thyroiditis-autoimmune-thyroiditis.csv",
    system="snomed",
    column="code",
)
# Hashimoto’s thyroiditis - hes
hashimoto_thyroiditis_code_icd = codelist_from_csv(
    "codelists/user-josephignace-thyroid-diseases-hashimoto-thyroiditis-icd10.csv",
    system="icd10",
    column="code",
)
# Thyroid toxicosis / hyper thyroid - YW: This seems to have been taken out from the excel spreadsheet 13/Dec/2022
##################################################################################################
# Outcome group 6: Autoimmune vasculitis                                                          #
##################################################################################################
# ANCA-associated - snomed
anca_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-anca-vasculitis.csv",
    system="snomed",
    column="code",
)
# ANCA-associated - hes
anca_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-vasculitis-anca-associated.csv",
    system="icd10",
    column="code",
)
# Giant cell arteritis - snomed
gca_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-anca-vasculitis.csv",
    system="snomed",
    column="code",
)
# Giant cell arteritis - hes
gca_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-vasculitis-giant-cell-arteritis.csv",
    system="icd10",
    column="code",
)
# IgA (immunoglobulin A) vasculitis - snomed
iga_vasculitis_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-iga-immunoglobulin-a-vasculitis.csv",
    system="snomed",
    column="code",
)
# IgA (immunoglobulin A) vasculitis - hes
iga_vasculitis_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-vasculitis-iga-immunoglobulin-a-vasculitis.csv",
    system="icd10",
    column="code",
)
# Polymyalgia Rheumatica (PMR) - snomed
pmr_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-polymyalgia-rheumatica.csv",
    system="snomed",
    column="code",
)
# Polymyalgia Rheumatica (PMR) - hes
pmr_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-vasculitis-polymyalgia-rheumatica-pmr.csv",
    system="icd10",
    column="code",
)
##################################################################################################
# Outcome group 7: Hematologic Diseases                                                          #
##################################################################################################
# Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - snomed
immune_thromb_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-immune-thrombocytopenia-idiopathic-thrombocytopenic-purpura.csv",
    system="snomed",
    column="code",
)
# Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura) - hes
immune_thromb_code_icd = codelist_from_csv(
    "codelists/user-josephignace-hematologic-diseases-immune-thrombocytopenia-formerly-known-as-idiopathic-thrombocytopenic-purpura-icd10.csv",
    system="icd10",
    column="code",
)
# Pernicious anaemia - snomed
pernicious_anaemia_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-pernicious-anaemia.csv",
    system="snomed",
    column="code",
)
# Pernicious anaemia - hes
pernicious_anaemia_code_icd = codelist_from_csv(
    "codelists/user-josephignace-hematologic-diseases-pernicious-anaemia-icd10.csv",
    system="icd10",
    column="code",
)
# Aplastic Anaemia - snomed
apa_code_snomed = codelist_from_csv(
    "codelists/opensafely-aplastic-anaemia-snomed.csv",
    system="snomed",
    column="id",
)
# Aplastic Anaemia - ctv3
apa_code_ctv = codelist_from_csv(
    "codelists/opensafely-aplastic-anaemia.csv",
    system="ctv3",
    column="CTV3ID",
)
# Aplastic Anaemia - hes
apa_code_icd = codelist_from_csv(
    "codelists/user-josephignace-hematologic-diseases-aplastic-anaemia-icd10.csv",
    system="icd10",
    column="code",
)
# Autoimmune haemolytic anaemia - snomed
aha_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-autoimmune-haemolytic-anaemia-autoimmune-hemolytic-anemia.csv",
    system="snomed",
    column="code",
)
# Autoimmune haemolytic anaemia - hes
aha_code_icd = codelist_from_csv(
    "codelists/user-josephignace-hematologic-diseases-autoimmune-haemolytic-anaemia-icd10.csv",
    system="icd10",
    column="code",
)
##################################################################################################
# Outcome group 8: Inflammatory neuromuscular disease                                            #
##################################################################################################
# Guillain Barre - read
glb_code_ctv = codelist_from_csv(
    "codelists/opensafely-guillain-barre.csv",
    system="ctv3",
    column="code",
)
# Guillain Barre - hes
glb_code_icd = codelist_from_csv(
    "codelists/opensafely-guillain-barre-syndrome-icd10.csv",
    system="icd10",
    column="code",
)
# Multiple Sclerosis - read
multiple_sclerosis_code_ctv = codelist_from_csv(
    "codelists/opensafely-multiple-sclerosis-v2.csv",
    system="ctv3",
    column="code",
)
# Multiple Sclerosis - hes
multiple_sclerosis_code_icd = codelist_from_csv(
    "codelists/user-yinghuiwei-multiple-sclerosis.csv",
    system="icd10",
    column="code",
)
# Myasthenia gravis - snomed
myasthenia_gravis_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-myasthenia-gravis.csv",
    system="snomed",
    column="code",
)
# Myasthenia gravis - hes
myasthenia_gravis_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-neuromuscular-disease-myasthenia-gravis-icd10.csv",
    system="icd10",
    column="code",
)
# Longitudinal myelitis - snomed
longit_myelitis_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-longitudinal-myelitis-longitudinal-extensive-transverse-myelitis.csv",
    system="snomed",
    column="code",
)
# Longitudinal myelitis - hes
longit_myelitis_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-neuromuscular-disease-longitudinal-myelitis-icd10.csv",
    system="icd10",
    column="code",
)
# Clinically isolated syndrome - snomed
cis_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-clinically-isolated-syndrome.csv",
    system="snomed",
    column="code",
)
# Clinically isolated syndrome - hes
cis_code_icd = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-neuromuscular-disease-clinically-isolated-syndrome-icd10.csv",
    system="icd10",
    column="code",
)

cocp_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-cocp_dmd.csv",
    system="snomed",
    column="code",
)
hrt_dmd = codelist_from_csv(
    "codelists/user-elsie_horne-hrt_dmd.csv",
    system="snomed",
    column="code",
)
