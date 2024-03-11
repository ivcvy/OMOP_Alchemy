import enum

class ConceptEnum(enum.Enum):

    @classmethod
    def member_values(cls):
        return (s.value for s in cls)
    
    @classmethod
    def is_member(cls, val):
        return not val or val in [s.value for s in cls]

    @classmethod
    def labels(cls):
        return [s.name for s in cls]
    
class ModifierFields(ConceptEnum):
    condition_occurrence_id = 1147127
    drug_exposure_id = 1147707
    procedure_occurrence_id = 1147082

class ModifierTables(ConceptEnum):
    drug_exposure = 1147339
    episode = 35225440
    observation = 1147304

class TreatmentEpisode(ConceptEnum):
    care_plan_assignment = 4207655  # SNOMED - Prescription of therapeutic regimen
    ehr_prescription = 32838        # EHR prescription
    ehr_planned_dispensing = 32837  # EHR planned dispensation
    ehr_encounter_record = 32827    # EHR encounter
    
class Modality(ConceptEnum):
    chemotherapy = 35803401
    radiotherapy = 35803411
    
class EpisodeConcepts(ConceptEnum):   
    episode_of_care = 32533           # Overarching disease episode
    treatment_regimen = 32531         # Assignment to or derivation of treatment regimen   
    treatment_cycle = 32532           # Assignment to or derivation of treatment cycle
    disease_first_occurrence = 32528  # Initial diagnosis
    disease_progression = 32677       # Diagnosis that is linked to another primary

class EpisodeTypes(ConceptEnum):
    ehr_defined = 32544               # Episode defined in EHR
    ehr_derived = 32545               # Episode derived algorithmically from EHR
    
class ConditionModifiers(ConceptEnum):
    # for measurement_concept_id grouping
    init_diag = 734306                # Cancer Modifier - Initial Diagnosis
    tnm = 734320                      # Cancer Modifier - Parent AJCC/UICC concept
    mets = 36769180                   # Cancer Modifier - Parent metastasis hierarchy parent


class TreatmentModifiers(ConceptEnum):
    ...


class TStageConcepts(ConceptEnum):
    # used to group tnm mappings into their relevant subtypes
    # preferably create a concept that is the parent of all these T concepts, but for now...
    t0 = 1634213
    t1 = 1635564
    t2 = 1635562
    t3 = 1634376
    t4 = 1634654
    ta = 1635682
    tx = 1635682
    tis = 1635682

class NStageConcepts(ConceptEnum):
    # as above for n...
    n0 = 1633440
    n1 = 1634434
    n2 = 1634119
    n3 = 1635320
    n4 = 1635445
    nx = 1633885

class MStageConcepts(ConceptEnum):
    # and m...
    m0 = 1635624
    m1 = 1635142
    mx = 1633547


class GroupStageConcepts(ConceptEnum):
    # there's a pattern here
    stage0 = 1633754
    stageI = 1633306
    stageII = 1634209
    stageIII = 1633650
    stageIV = 1633650
