/*
All clafers: 19 | Abstract: 1 | Concrete: 18 | References: 0
Constraints: 3
Goals: 0
Global scope: 1..*
All names unique: False
*/
open util/integer
pred show {}
run  show for 1 but 1 c11_FunctionalRequirements, 1 c13_SalaryTotal, 1 c16_NonFunctionalRequirement, 1 c1_FeatureSpec, 1 c2_DataRequirements, 1 c6_FlatOrHierachicalCompanies

abstract sig c1_FeatureSpec
{ r_c2_DataRequirements : one c2_DataRequirements
, r_c11_FunctionalRequirements : one c11_FunctionalRequirements
, r_c16_NonFunctionalRequirement : one c16_NonFunctionalRequirement }
{ (some (this.@r_c11_FunctionalRequirements).@r_c15_CompanyDepth) => (some ((this.@r_c2_DataRequirements).@r_c6_FlatOrHierachicalCompanies).@r_c8_HierachicalCompanies)
  (some (this.@r_c2_DataRequirements).@r_c10_SalaryAlignment) => (some ((this.@r_c2_DataRequirements).@r_c6_FlatOrHierachicalCompanies).@r_c8_HierachicalCompanies) }

sig c2_DataRequirements
{ r_c3_OneOrManyCompanies : lone c3_OneOrManyCompanies
, r_c6_FlatOrHierachicalCompanies : one c6_FlatOrHierachicalCompanies
, r_c9_ConflictOfInterests : lone c9_ConflictOfInterests
, r_c10_SalaryAlignment : lone c10_SalaryAlignment }
{ one @r_c2_DataRequirements.this }

sig c3_OneOrManyCompanies
{ r_c4_OneCompany : lone c4_OneCompany
, r_c5_ManyCompanies : lone c5_ManyCompanies }
{ one @r_c3_OneOrManyCompanies.this
  let children = (r_c4_OneCompany + r_c5_ManyCompanies) | one children }

sig c4_OneCompany
{}
{ one @r_c4_OneCompany.this }

sig c5_ManyCompanies
{}
{ one @r_c5_ManyCompanies.this }

sig c6_FlatOrHierachicalCompanies
{ r_c7_FlatCompanies : lone c7_FlatCompanies
, r_c8_HierachicalCompanies : lone c8_HierachicalCompanies }
{ one @r_c6_FlatOrHierachicalCompanies.this
  let children = (r_c7_FlatCompanies + r_c8_HierachicalCompanies) | one children }

sig c7_FlatCompanies
{}
{ one @r_c7_FlatCompanies.this }

sig c8_HierachicalCompanies
{}
{ one @r_c8_HierachicalCompanies.this }

sig c9_ConflictOfInterests
{}
{ one @r_c9_ConflictOfInterests.this }

sig c10_SalaryAlignment
{}
{ one @r_c10_SalaryAlignment.this }

sig c11_FunctionalRequirements
{ r_c12_SalaryCut : lone c12_SalaryCut
, r_c13_SalaryTotal : lone c13_SalaryTotal
, r_c14_SalaryDelta : lone c14_SalaryDelta
, r_c15_CompanyDepth : lone c15_CompanyDepth }
{ one @r_c11_FunctionalRequirements.this }

sig c12_SalaryCut
{}
{ one @r_c12_SalaryCut.this }

sig c13_SalaryTotal
{}
{ one @r_c13_SalaryTotal.this }

sig c14_SalaryDelta
{}
{ one @r_c14_SalaryDelta.this }

sig c15_CompanyDepth
{}
{ one @r_c15_CompanyDepth.this }

sig c16_NonFunctionalRequirement
{ r_c17_SerializableCompanies : lone c17_SerializableCompanies
, r_c18_PersistentCompanies : lone c18_PersistentCompanies }
{ one @r_c16_NonFunctionalRequirement.this }

sig c17_SerializableCompanies
{}
{ one @r_c17_SerializableCompanies.this }

sig c18_PersistentCompanies
{}
{ one @r_c18_PersistentCompanies.this }

one sig c29_Atltotalplugin extends c1_FeatureSpec
{}
{ some (this.@r_c11_FunctionalRequirements).@r_c13_SalaryTotal }

