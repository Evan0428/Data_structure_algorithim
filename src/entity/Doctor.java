package entity;

/**
 * Author: Your Name
 */
public class Doctor {
	private final String doctorId;
	private String name;
	private String specialization;

	public Doctor(String doctorId, String name, String specialization) {
		this.doctorId = doctorId;
		this.name = name;
		this.specialization = specialization;
	}

	public String getDoctorId() { return doctorId; }
	public String getName() { return name; }
	public void setName(String name) { this.name = name; }
	public String getSpecialization() { return specialization; }
	public void setSpecialization(String specialization) { this.specialization = specialization; }

	@Override
	public String toString() {
		return doctorId + " - " + name + " (" + specialization + ")";
	}
}