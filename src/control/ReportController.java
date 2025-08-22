package control;

import adt.MyIterator;
import adt.MyList;
import entity.Appointment;
import entity.Consultation;
import entity.Doctor;
import entity.Patient;

/**
 * Author: Your Name
 */
public class ReportController {
	private final ConsultationController consultationController;

	public ReportController(ConsultationController consultationController) {
		this.consultationController = consultationController;
	}

	// Report 1: Number of consultations per doctor
	public String generateConsultationsPerDoctorReport() {
		MyList<Doctor> doctors = consultationController.getDoctors();
		MyList<Consultation> consultations = consultationController.getConsultations();
		StringBuilder sb = new StringBuilder();
		sb.append("Consultations per Doctor\n");
		MyIterator<Doctor> dit = doctors.iterator();
		while (dit.hasNext()) {
			Doctor d = dit.next();
			int count = 0;
			MyIterator<Consultation> cit = consultations.iterator();
			while (cit.hasNext()) {
				Consultation c = cit.next();
				if (c.getDoctor().getDoctorId().equals(d.getDoctorId())) count++;
			}
			sb.append(d.getDoctorId()).append(" - ").append(d.getName()).append(": ").append(count).append("\n");
		}
		return sb.toString();
	}

	// Report 2: Upcoming appointments count per patient
	public String generateUpcomingAppointmentsPerPatientReport() {
		MyList<Patient> patients = consultationController.getPatients();
		MyList<Appointment> appointments = consultationController.getAppointments();
		StringBuilder sb = new StringBuilder();
		sb.append("Upcoming Appointments per Patient\n");
		MyIterator<Patient> pit = patients.iterator();
		while (pit.hasNext()) {
			Patient p = pit.next();
			int count = 0;
			MyIterator<Appointment> ait = appointments.iterator();
			while (ait.hasNext()) {
				Appointment a = ait.next();
				if (a.getPatient().getPatientId().equals(p.getPatientId()) && !a.isAttended()) count++;
			}
			sb.append(p.getPatientId()).append(" - ").append(p.getName()).append(": ").append(count).append("\n");
		}
		return sb.toString();
	}
}