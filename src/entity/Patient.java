package entity;

/**
 * Author: Your Name
 */
public class Patient {
	private final String patientId;
	private String name;
	private String phone;
	private String email;

	public Patient(String patientId, String name, String phone, String email) {
		this.patientId = patientId;
		this.name = name;
		this.phone = phone;
		this.email = email;
	}

	public String getPatientId() { return patientId; }
	public String getName() { return name; }
	public void setName(String name) { this.name = name; }
	public String getPhone() { return phone; }
	public void setPhone(String phone) { this.phone = phone; }
	public String getEmail() { return email; }
	public void setEmail(String email) { this.email = email; }

	@Override
	public String toString() {
		return patientId + " - " + name;
	}
}