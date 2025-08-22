package boundary;

import adt.MyIterator;
import control.ConsultationController;
import control.ReportController;
import entity.Appointment;
import entity.Consultation;
import entity.Doctor;
import entity.Patient;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.Scanner;

/**
 * Author: Your Name
 */
public class ConsultationUI {
	private final ConsultationController controller;
	private final ReportController reportController;
	private final Scanner scanner = new Scanner(System.in);

	public ConsultationUI(ConsultationController controller) {
		this.controller = controller;
		this.reportController = new ReportController(controller);
	}

	public void run() {
		boolean exit = false;
		while (!exit) {
			System.out.println("\n=== Consultation Management (Module 3) ===");
			System.out.println("1. Register Patient");
			System.out.println("2. Register Doctor");
			System.out.println("3. Create Appointment");
			System.out.println("4. Conduct Consultation");
			System.out.println("5. Schedule Follow-up Appointment");
			System.out.println("6. List Patients");
			System.out.println("7. List Doctors");
			System.out.println("8. List Appointments");
			System.out.println("9. List Consultations");
			System.out.println("10. Report: Consultations per Doctor");
			System.out.println("11. Report: Upcoming Appointments per Patient");
			System.out.println("0. Exit");
			System.out.print("Choose: ");
			String choice = scanner.nextLine().trim();
			switch (choice) {
				case "1": registerPatient(); break;
				case "2": registerDoctor(); break;
				case "3": createAppointment(); break;
				case "4": conductConsultation(); break;
				case "5": scheduleFollowUp(); break;
				case "6": listPatients(); break;
				case "7": listDoctors(); break;
				case "8": listAppointments(); break;
				case "9": listConsultations(); break;
				case "10": System.out.println(reportController.generateConsultationsPerDoctorReport()); break;
				case "11": System.out.println(reportController.generateUpcomingAppointmentsPerPatientReport()); break;
				case "0": exit = true; break;
				default: System.out.println("Invalid option.");
			}
		}
	}

	private void registerPatient() {
		System.out.print("Patient ID: ");
		String id = scanner.nextLine().trim();
		System.out.print("Name: ");
		String name = scanner.nextLine().trim();
		System.out.print("Phone: ");
		String phone = scanner.nextLine().trim();
		System.out.print("Email: ");
		String email = scanner.nextLine().trim();
		Patient p = controller.registerPatient(id, name, phone, email);
		System.out.println("Registered: " + p);
	}

	private void registerDoctor() {
		System.out.print("Doctor ID: ");
		String id = scanner.nextLine().trim();
		System.out.print("Name: ");
		String name = scanner.nextLine().trim();
		System.out.print("Specialization: ");
		String spec = scanner.nextLine().trim();
		Doctor d = controller.registerDoctor(id, name, spec);
		System.out.println("Registered: " + d);
	}

	private void createAppointment() {
		System.out.print("Appointment ID: ");
		String id = scanner.nextLine().trim();
		System.out.print("Patient ID: ");
		String pid = scanner.nextLine().trim();
		System.out.print("Doctor ID: ");
		String did = scanner.nextLine().trim();
		LocalDate date = readDate("Date (YYYY-MM-DD): ");
		LocalTime time = readTime("Time (HH:MM): ");
		System.out.print("Purpose: ");
		String purpose = scanner.nextLine().trim();
		Appointment a = controller.createAppointment(id, pid, did, LocalDateTime.of(date, time), purpose);
		if (a == null) System.out.println("Invalid patient or doctor ID.");
		else System.out.println("Created: " + a.getAppointmentId());
	}

	private void conductConsultation() {
		System.out.print("Consultation ID: ");
		String cid = scanner.nextLine().trim();
		System.out.print("Appointment ID: ");
		String aid = scanner.nextLine().trim();
		System.out.print("Symptoms: ");
		String symptoms = scanner.nextLine().trim();
		System.out.print("Diagnosis: ");
		String diagnosis = scanner.nextLine().trim();
		System.out.print("Notes: ");
		String notes = scanner.nextLine().trim();
		Consultation c = controller.conductConsultation(cid, aid, symptoms, diagnosis, notes);
		if (c == null) System.out.println("Invalid appointment ID.");
		else System.out.println("Consultation recorded: " + c.getConsultationId());
	}

	private void scheduleFollowUp() {
		System.out.print("Existing Consultation ID: ");
		String cid = scanner.nextLine().trim();
		System.out.print("New Appointment ID: ");
		String aid = scanner.nextLine().trim();
		LocalDate date = readDate("Follow-up Date (YYYY-MM-DD): ");
		LocalTime time = readTime("Time (HH:MM): ");
		System.out.print("Purpose: ");
		String purpose = scanner.nextLine().trim();
		Appointment a = controller.scheduleFollowUp(aid, cid, LocalDateTime.of(date, time), purpose);
		if (a == null) System.out.println("Invalid consultation ID.");
		else System.out.println("Follow-up scheduled: " + a.getAppointmentId());
	}

	private void listPatients() {
		System.out.println("Patients:");
		MyIterator<Patient> it = controller.getPatients().iterator();
		while (it.hasNext()) System.out.println("- " + it.next());
	}

	private void listDoctors() {
		System.out.println("Doctors:");
		MyIterator<Doctor> it = controller.getDoctors().iterator();
		while (it.hasNext()) System.out.println("- " + it.next());
	}

	private void listAppointments() {
		System.out.println("Appointments:");
		MyIterator<Appointment> it = controller.getAppointments().iterator();
		while (it.hasNext()) {
			Appointment a = it.next();
			System.out.println("- " + a.getAppointmentId() + ": " + a.getPatient().getName() + " with " + a.getDoctor().getName() + " on " + a.getDateTime() + (a.isAttended() ? " (done)" : ""));
		}
	}

	private void listConsultations() {
		System.out.println("Consultations:");
		MyIterator<Consultation> it = controller.getConsultations().iterator();
		while (it.hasNext()) {
			Consultation c = it.next();
			System.out.println("- " + c.getConsultationId() + ": " + c.getPatient().getName() + " with " + c.getDoctor().getName() + " on " + c.getDateTime());
		}
	}

	private LocalDate readDate(String prompt) {
		while (true) {
			try {
				System.out.print(prompt);
				String s = scanner.nextLine().trim();
				return LocalDate.parse(s);
			} catch (Exception e) {
				System.out.println("Invalid date.");
			}
		}
	}

	private LocalTime readTime(String prompt) {
		while (true) {
			try {
				System.out.print(prompt);
				String s = scanner.nextLine().trim();
				return LocalTime.parse(s + (s.length()==5?":00":""));
			} catch (Exception e) {
				System.out.println("Invalid time.");
			}
		}
	}
}