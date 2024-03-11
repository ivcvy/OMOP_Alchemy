from datetime import datetime, date
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.hybrid import hybrid_property

from .modifiable_table import Modifiable_Table
from ...db import Base

class Condition_Occurrence(Modifiable_Table):
    __tablename__ = 'condition_occurrence'
    validators = {}

    # identifier
    condition_occurrence_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('modifiable_table.modifier_id'), primary_key=True, autoincrement=True)
    # temporal
    condition_start_date: so.Mapped[date] = so.mapped_column(sa.Date)
    condition_start_datetime: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)
    condition_end_date: so.Mapped[Optional[date]] = so.mapped_column(sa.Date, nullable=True)
    condition_end_datetime: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)
    # strings
    stop_reason: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    condition_source_value: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)
    condition_status_source_value: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)
    # fks
    person_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('person.person_id', name='co_fk_1'))
    provider_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('provider.provider_id', name='co_fk_2'), nullable=True)
    visit_occurrence_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('visit_occurrence.visit_occurrence_id', name='co_fk_3'), nullable=True)
    visit_detail_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('visit_detail.visit_detail_id', name='co_fk_4'), nullable=True)
    # concept fks
    condition_concept_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('concept.concept_id', name='co_fk_5'))
    condition_type_concept_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('concept.concept_id', name='co_fk_6'))
    condition_status_concept_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('concept.concept_id', name='co_fk_7'), nullable=True)
    condition_source_concept_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('concept.concept_id', name='co_fk_8'), nullable=True)
    # relationships
    person: so.Mapped['Person'] = so.relationship(foreign_keys=[person_id])
    provider: so.Mapped[Optional['Provider']] = so.relationship(foreign_keys=[provider_id])
    visit_occurrence: so.Mapped[Optional['Visit_Occurrence']] = so.relationship(foreign_keys=[visit_occurrence_id])
    visit_detail: so.Mapped[Optional['Visit_Detail']] = so.relationship(foreign_keys=[visit_detail_id])
    # concept relationships
    condition_concept: so.Mapped['Concept'] = so.relationship(foreign_keys=[condition_concept_id])
    condition_type_concept: so.Mapped['Concept'] = so.relationship(foreign_keys=[condition_type_concept_id])
    condition_status_concept: so.Mapped['Concept'] = so.relationship(foreign_keys=[condition_status_concept_id])
    condition_source_concept: so.Mapped['Concept'] = so.relationship(foreign_keys=[condition_source_concept_id])

    __mapper_args__ = {
        "polymorphic_identity": "condition",
        'inherit_condition': (condition_occurrence_id == Modifiable_Table.modifier_id)
    }

    @classmethod
    def set_validators(cls):
        # putting this here so that we can defer the import until after the models have all been instantiated, otherwise 
        # it tries to query the concepts from non-existent tables - there may be a better way?
        from ...conventions.vocab_lookups import tnm_lookup
        cls.validators = {'tnm': tnm_lookup}

    @hybrid_property
    def condition_label(self):
        if self.condition_concept:
            return self.condition_concept.concept_name
        
    @condition_label.expression
    def _condition_label_expression(cls) -> sa.ColumnElement[Optional[str]]:
        return sa.cast("SQLColumnExpression[Optional[str]]", cls.condition_concept.concept_name)

    # TODO: Down the line we should consider if all of these oncology-extension-specific properties need to be refactored out into a subclass?

    def get_stage(self, concepts):
        return sorted([m for m in self.modifiers if m.measurement_concept_id in concepts], key=lambda mod: mod.measurement_date)

    @hybrid_property
    def path_confirmation(self):
        # returns true is any of the stage modifiers of this condition are of type pathological
        if 'tnm' in self.validators:
            return len(self.get_stage(self.validators['tnm'].path_stage_concepts)) > 0

    @hybrid_property
    def group_stage(self):
        # returns group stage modifiers of this condition, ordered by modifier date (most recent last)
        if 'tnm' in self.validators:
            return self.get_stage(self.validators['tnm'].group_stage_concepts)
    
    @hybrid_property
    def t_stage(self):
        if 'tnm' in self.validators:
            return self.get_stage(self.validators['tnm'].t_stage_concepts)
            
    @hybrid_property
    def n_stage(self):
        if 'tnm' in self.validators:
            return self.get_stage(self.validators['tnm'].n_stage_concepts)

    @hybrid_property
    def m_stage(self):
        if 'tnm' in self.validators:
            return self.get_stage(self.validators['tnm'].m_stage_concepts)