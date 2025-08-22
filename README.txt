Clinic Management System - Module 3 (Consultation Management)

How to Compile & Run (Console UI)
1) Compile:
   javac -d bin $(find src -name "*.java")
2) Run:
   java -cp bin Main

Project Structure (ECB pattern)
- Entity classes: src/entity/*.java
  Patient, Doctor, Appointment, Consultation
- Control classes: src/control/*.java
  ConsultationController (business logic), ReportController (summary reports)
- Boundary class: src/boundary/ConsultationUI.java (console UI)
- Custom ADT: src/adt/*.java
  MyList (interface), MyIterator (interface), SinglyLinkedList (implementation)

Notes
- No Java Collections Framework is used. All collections use custom ADT.
- Two reports provided:
  1) Consultations per Doctor
  2) Upcoming Appointments per Patient
- Sample seed data added in Main.java