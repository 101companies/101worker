// schema of the 101 companies in the SimpleGraph Schema Notation (see megalib/SimpleGraph.php)
// @ means key
// ! means 1
// ? means 0..1
// * means *
// This file is used in particular in the context of the transformation json101AsRdf101
// Only the classes and attributes listed below will be converted
// This means that there could be more classes and attributes in the original json file.
// Attributes names should be the same as those in the json files.
// There is a mapping file for the binding between class and top level category.   


// Note (1): Some fields are currently ignored because the fact that they contain XML
// leads to problems in graphml generation. Will be fixed later. 
   
Category {
  id: string@ ;
  name: string! ;
  type: string! ;
  url: string! ;
  headline: string? ;
  headline_links: Entity* ; 
  // discussion:string? ;  // See Note (1)
  // discussion_links:Entity* ;  // See Note (1)
  categories: Category* ;
  languageMembers: Language* ;
  conceptMembers: Concept* ;
  featureMembers: Feature* ;
  implementationMembers: Implementation* ;
  technologyMembers: Technology*
}   
    
Concept {
  id: string@ ;
  name: string! ;
  type: string! ;
  url: string! ;
  headline:string? ;
  headline_links: Entity* ;
  // discussion:string?  ; // See Note (1)
  // discussion_links:Entity* ;  // See Note (1)
}
        
Feature {
  id: string@ ;
  name: string! ;
  type: string! ;
  url: string! ;
  headline:string! ;
  headline_links: Entity* ;
  // description:string? ;  // See Note (1)
  // description_links:Entity* ; ;  // See Note (1)
  // illustration:string? ; // See Note (1)
  // illustration_links:Entity* ; // See Note (1)
  implementations:Implementation*
}
    
Implementation {
  id: string@ ;
  name: string! ;
  type: string! ;
  url: string! ;
  headline: string! ;
  headline_links: Entity* ;
  // motivation: string! ;  // See Note (1)
  // motivation_links:Entity* ;  // See Note (1)
  features: Feature* ;
  languages: Language* ;
  technologies: Technology* ;
  // usage:string? ; // See Note (1)
  // usage_links:Entity* ;  // See Note (1)
}
    
Language {
  id: string@ ;
  name: string! ;
  type: string! ;
  url: string! ;
  headline: string! ;
  headline_links: Enitiy* ;
  // description: string? ;  // See Note (1)
  // description_links:Enitiy* ; ;  // See Note (1)
  implementations: Implementation*
}
    
Technology {
  id: string@ ;
  name: string! ;
  type: string! ;
  url: string! ;
  headline: string! ;
  headline_links: Entity* ; 
  // description: string? ;   // See Note (1)
  // description_links:Entity* ; ;  // See Note (1)
  implementations: Implementation*
}

Page {
  id: string@ ;
  name: string! ;
  type: string! ;
  url: string! ;
  headline: string! ; 
  headline_links: Entity* ;
  // discussion:string? ;  // See Note (1)
  // discussion_links:Entity* ;  // See Note (1)
}

Entity {
  id: string@ ;
  type: string! ;
  name: string! ;
}


