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
ra_code_hes = codelist_from_csv(
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
pa_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-psoriatic-arthritis.csv",
    system = "snomed",
    column = "code",
)
# Psoriatic arthritis - icd10 
pa_code_hes = codelist_from_csv(
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
axial_code_hes = codelist_from_csv(
    "codelists/user-josephignace-inflammatory-arthritis-axial-spondyloarthritis-icd10.csv",
    system = "icd10",
    column = "code",
)
##################################################################################################
# Outcome group 2:  Connective tissue disorders                                                  #
##################################################################################################
# Systematic lupus erythematosu - snomed
sle_code_snomed = codelist_from_csv(
    "codelists/user-markdrussell-systemic-sclerosisscleroderma.csv",
    system="snomed",
    column="code",
)
# Systematic lupus erythematosu - hes
sle_code_hes = codelist_from_csv(
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
sjs_code_hes = codelist_from_csv(
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
sss_code_hes = codelist_from_csv(
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
im_code_hes = codelist_from_csv(
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
mctd_code_hes = codelist_from_csv(
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
hs_code_hes = codelist_from_csv(
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

# Crohn's disease - snomed
crohn_code_snomed = codelist_from_csv(
    "codelists/opensafely-crohns-disease.csv",
    system="snomed",
    column="code",
)
# Crohn's disease - hes
crohn_code_icd = codelist_from_csv(
    "codelists/user-josephignace-autoimmune-gi-inflammatory-bowel-disease-crohns-disease-icd10.csv",
    system="icd10",
    column="code",
)
# Ulcerative colitis - snomed
uc_code_snomed = codelist_from_csv(
    "codelists/opensafely-ulcerative-colitis.csv",
    system="snomed",
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
    "codelists/user-josephignace-thyroid-diseases-graves-disease-icd10.csv",
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
    "codelists/user-markdrussell-polymyalgia-rheumatica.csv",
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
    "codelists/user-markdrussell-autoimmune-haemolytic-anaemia-autoimmune-hemolytic-anemia.csv",
    system="icd10",
    column="code",
)
##################################################################################################
# Outcome group 8: Inflammatory neuromuscular disease                                            #
##################################################################################################
# Guillain Barre - snomed
glb_code_snomed = codelist_from_csv(
    "codelists/opensafely-guillain-barre.csv",
    system="snomed",
    column="code",
)
# Guillain Barre - hes
glb_code_hes = codelist_from_csv(
    "codelists/opensafely-guillain-barre-syndrome-icd10.csv",
    system="icd10",
    column="code",
)
# Multiple Sclerosis - snomed
multiple_sclerosis_code_snomed = codelist_from_csv(
    "codelists/opensafely-multiple-sclerosis-v2.csv",
    system="snomed",
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