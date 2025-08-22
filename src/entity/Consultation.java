package entity;

import java.time.LocalDateTime;

/**
 * Author: Your Name
 */
public class Consultation {
	private final String consultationId;
	private final Patient patient;
	private final Doctor doctor;
	private final LocalDateTime dateTime;
	private String symptoms;
	private String diagnosis;
	private String notes;

	public Consultation(String consultationId, Patient patient, Doctor doctor, LocalDateTime dateTime,
			String symptoms, String diagnosis, String notes) {
		this.consultationId = consultationId;
		this.patient = patient;
		this.doctor = doctor;
		this.dateTime = dateTime;
		this.symptoms = symptoms;
		this.diagnosis = diagnosis;
		this.notes = notes;
	}

	public String getConsultationId() { return consultationId; }
	public Patient getPatient() { return patient; }
	public Doctor getDoctor() { return doctor; }
	public LocalDateTime getDateTime() { return dateTime; }
	public String getSymptoms() { return symptoms; }
	public void setSymptoms(String symptoms) { this.symptoms = symptoms; }
	public String getDiagnosis() { return diagnosis; }
	public void setDiagnosis(String diagnosis) { this.diagnosis = diagnosis; }
	public String getNotes() { return notes; }
	public void setNotes(String notes) { this.notes = notes; }
}