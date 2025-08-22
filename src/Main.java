import boundary.ConsultationUI;
import control.ConsultationController;

import java.time.LocalDateTime;

/**
 * Author: Your Name
 */
public class Main {
	public static void main(String[] args) {
		ConsultationController controller = new ConsultationController();

		// Seed data (patients, doctors, appointments)
		controller.registerPatient("P001", "Alice Tan", "012-1234567", "alice@example.com");
		controller.registerPatient("P002", "Bob Lee", "012-2223333", "bob@example.com");
		controller.registerDoctor("D001", "Dr. Lim", "General Medicine");
		controller.registerDoctor("D002", "Dr. Wong", "Dermatology");
		controller.createAppointment("A001", "P001", "D001", LocalDateTime.now().plusDays(1).withHour(9).withMinute(0), "Fever");
		controller.createAppointment("A002", "P002", "D002", LocalDateTime.now().plusDays(2).withHour(10).withMinute(30), "Rash");

		ConsultationUI ui = new ConsultationUI(controller);
		ui.run();
	}
}