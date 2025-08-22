package entity;

import java.time.LocalDateTime;

/**
 * Author: Your Name
 */
public class Appointment {
	private final String appointmentId;
	private final Patient patient;
	private final Doctor doctor;
	private final LocalDateTime dateTime;
	private String purpose;
	private boolean attended;

	public Appointment(String appointmentId, Patient patient, Doctor doctor, LocalDateTime dateTime, String purpose) {
		this.appointmentId = appointmentId;
		this.patient = patient;
		this.doctor = doctor;
		this.dateTime = dateTime;
		this.purpose = purpose;
		this.attended = false;
	}

	public String getAppointmentId() { return appointmentId; }
	public Patient getPatient() { return patient; }
	public Doctor getDoctor() { return doctor; }
	public LocalDateTime getDateTime() { return dateTime; }
	public String getPurpose() { return purpose; }
	public void setPurpose(String purpose) { this.purpose = purpose; }
	public boolean isAttended() { return attended; }
	public void setAttended(boolean attended) { this.attended = attended; }
}