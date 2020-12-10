# MaterializationOfDeductions
An extension of Owlready by Mandisa Baleni. Owlready was designed and written by Jean-Baptiste Lamy to aid automatically editing OWL ontologies with implicit inferences found in data models that are deduced  by a reasoner. 
The directory Extension_MOD is an extension designed and programmed by Mandisa Baleni to better realize ontology engineering for OWL ontologies that encapsulate EER concepts. 
Moreover, additional services include user validation mechanisms  like accepting and rejecting inferences and restructuring the ontology based on description logics semantics 
(formalised reasoning rules). This contributes to the efforts that have been made to achieve a data representation with underlying knowledge so that data has meaning. Data concepts can be expressed
in relation to one another in a knowledge layer and the actual data of said concepts can be stored in relational databases. This plays a role in achieving the semantic web and decision-making support 
in many subject domains like medicine practice.

For deeper insight into the purpose of this project, software design expected I/O, please find AToolforManagingtheDeductionsonaConceptualDataModel.pdf in the main directory. 

Instructions for running it:
1. Run Interface.py
2. Give full file path names of input and output OWL in RDF/XML format (can use sample models in testsamplemodels directory)
    File input/output specification example:
        /User/name/directory/pizza.owl
        (make sure output file empty)

A tool for managing materialization of deductions example samples have equivalent testsamplemodels shown below:

sample 1 ~EntitySubsumptionbinary1-1mand_i
sample 2 ~ entitysubsumptionbinary1-1optional_i
sample 3 ~ entitysubsumptionbinary1-Noptional_i
sample 4 ~entitysubsumptionbinary1-Nopt
sample 5 ~ EntityInconsistentDisjoint:covering_i
sample 6 ~wrapper_removesubclass_disjoint
sample 7 ~wrapper_removesubclass_1-1optional
sample 8 ~wrapper_removesubclass_1-Nmand
sample 9 ~ wrapper_removesubclass_disjoint (remove margherita, keep cheesey)
sample 10 ~ wrapper_remove_nochildren (remove margherita, keep cheesey)
