package control;

import adt.MyIterator;
import adt.MyList;
import adt.SinglyLinkedList;
import entity.Appointment;
import entity.Consultation;
import entity.Doctor;
import entity.Patient;

import java.time.LocalDateTime;

/**
 * Author: Your Name
 */
public class ConsultationController {
	private final MyList<Patient> patients = new SinglyLinkedList<>();
	private final MyList<Doctor> doctors = new SinglyLinkedList<>();
	private final MyList<Appointment> appointments = new SinglyLinkedList<>();
	private final MyList<Consultation> consultations = new SinglyLinkedList<>();

	public MyList<Patient> getPatients() { return patients; }
	public MyList<Doctor> getDoctors() { return doctors; }
	public MyList<Appointment> getAppointments() { return appointments; }
	public MyList<Consultation> getConsultations() { return consultations; }

	public Patient registerPatient(String id, String name, String phone, String email) {
		Patient p = new Patient(id, name, phone, email);
		patients.addLast(p);
		return p;
	}

	public Doctor registerDoctor(String id, String name, String specialization) {
		Doctor d = new Doctor(id, name, specialization);
		doctors.addLast(d);
		return d;
	}

	public Appointment createAppointment(String id, String patientId, String doctorId, LocalDateTime dateTime, String purpose) {
		Patient p = findPatientById(patientId);
		Doctor d = findDoctorById(doctorId);
		if (p == null || d == null) return null;
		Appointment a = new Appointment(id, p, d, dateTime, purpose);
		appointments.addLast(a);
		return a;
	}

	public Consultation conductConsultation(String consultationId, String appointmentId, String symptoms, String diagnosis, String notes) {
		Appointment a = findAppointmentById(appointmentId);
		if (a == null) return null;
		a.setAttended(true);
		Consultation c = new Consultation(consultationId, a.getPatient(), a.getDoctor(), a.getDateTime(), symptoms, diagnosis, notes);
		consultations.addLast(c);
		return c;
	}

	public Appointment scheduleFollowUp(String newAppointmentId, String consultationId, LocalDateTime dateTime, String purpose) {
		Consultation c = findConsultationById(consultationId);
		if (c == null) return null;
		Appointment a = new Appointment(newAppointmentId, c.getPatient(), c.getDoctor(), dateTime, purpose);
		appointments.addLast(a);
		return a;
	}

	public Patient findPatientById(String id) {
		MyIterator<Patient> it = patients.iterator();
		while (it.hasNext()) {
			Patient p = it.next();
			if (p.getPatientId().equals(id)) return p;
		}
		return null;
	}

	public Doctor findDoctorById(String id) {
		MyIterator<Doctor> it = doctors.iterator();
		while (it.hasNext()) {
			Doctor d = it.next();
			if (d.getDoctorId().equals(id)) return d;
		}
		return null;
	}

	public Appointment findAppointmentById(String id) {
		MyIterator<Appointment> it = appointments.iterator();
		while (it.hasNext()) {
			Appointment a = it.next();
			if (a.getAppointmentId().equals(id)) return a;
		}
		return null;
	}

	public Consultation findConsultationById(String id) {
		MyIterator<Consultation> it = consultations.iterator();
		while (it.hasNext()) {
			Consultation c = it.next();
			if (c.getConsultationId().equals(id)) return c;
		}
		return null;
	}
}