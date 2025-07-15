MultiEmployer

Projects

- RemitOn – Remittances Online
  - a system for employers to report employee hours for dues and fringe remittances for Local 1MO
  - contractually required to to mimic the design and functionality of an existing system
  - backend, use cases, derived from HTML mockups
  - complex pay periods based on numbered work weeks
  - rates by contract, job classification, and employee status with start and end dates
  - relationship between contracts and contracters (employers) having start and end dates
  - architecture constrained to page based architecture with non-readable named files corresponding to files a FoxPro/WebConnect system.

- NatRemit – National Remittances
  - units reported same as RemitOn (which is really a subset of the national system, with different pay periods, I suppose)
  - complexity involving the classification of rates combined with complex rules (difficult to describe)
  - architecture constrained in the same way, but pages eventually were allowed to become human-readable, if not terribly structured
  - business rules captured in hierarchical remittance calculator classes, with the most general rules at the top and the most complex at the bottom

- BacPortal
  - member/local/iu portal for BAC data in a replicated SQL Server database
  - same type of single page architecture

- BacWorks
  - replaced local BAC portal, mixing single page architecture with Symfony framework
  - the Symfony part being based on data imported from Access MDBs used by BAC locals nationwide, BacWorks replaced the MDBs
  - application was developed without fully understanding HOW the locals used the MDB; the use cases (as they are) were derived from the schema of the MDB and hand waving
  - data is a mix of the BacPortal SQL server data (replicated, non writable) and BacWorks data imported from the MDBs
  - data displayed as though it came from a single source, however, and often inconsistent (the users were confused). You could not tell what you were actually looking at
  - data from a handful of locals came from entirely different systems and custom scripts had to be developed to transform and interpolate data to fit into the schema

- Ibew701 Remittances
  - first remittance system to use a framework
  - a web UI for remittance reporting that replaced the remittance UI of, and exchanged data with, an existing mainframe system
  - data imported from flat files, very simple CSV output to be slurped up by the mainframe system
  - much more complex units; in addition to hours, remittances per employee were based on various other reported factors
  - different contracts required an arbitrary set of the available units, so that needed to be tracked; the contract data was a lot more complex

- UBF United Benefit Fund
  - much simpler way of submitting remittances than Ibew701, but initially described as being the same (with this one I had to derive the use cases from a transcript of a meeting I did not attend)
  - required exchange of data with remote SQL Server with complicated schema, daily import, export to a staging schema
  - the ACH model I developed was very complete, based on a thorough research of what things an ACH has and how they're related

- 569trusts
  - integrated Symfony with WordPress to provide a portal for 569 Trusts
  - integrated claims and EOB data from provided text files

- Infrastructure
  - maintained IIS Servers with different versions of PHP, for internal draft, external draft, and production
  - made sure that each application was developed in its own PHP version with appropriate dependencies
  - extended Laravel Homestead to create a scripted, reproducible development environment for developers of any skill level
  - maintained a GitLab instance for source control
  - developed and maintained deployment scripts for each application, for internal draft, external draft, and production environments

- LineCo
  - oversaw the forking and merging of the application for complete front-end redesign and implied, undocumented changes to use cases
  - spent many hours poring over legacy code, finding bugs in processes

What I liked (in spite of myself)

- Figuring out how to make the complex business rules work within the peculiar constraints.

What I didn't like

- Lack of awareness of the amount of work involved in making things work within
the peculiar constraints, and not making progress with any systematic approach
due to constant and avoidable introduction of new problems as a result of this
lack of awareness.
