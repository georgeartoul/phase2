package GUI;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.util.ResourceBundle;

import javax.swing.plaf.basic.BasicInternalFrameTitlePane.SystemMenuBar;

import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.stage.Stage;

public class SetStrategyController implements Initializable {
	public static Stage primaryStage;
	FileWriter fw = null;
	BufferedWriter bw = null;
	PrintWriter pw = null;
	String st[] = { "all in road 1", "all in road 2", "Random road with equal probability",
			"send each driver to his preferred road" };

	@FXML
	private Button nextBtn;

	@FXML
	private Button backBtn;

	@FXML
	private ChoiceBox<String> strategyCb;

	@FXML
	void backStep(ActionEvent event) throws Exception {
		SimulatedTrafficController simulatedTrafficController = new SimulatedTrafficController();
		simulatedTrafficController.start(primaryStage);

	}

	@FXML
	void nextStep(ActionEvent event) throws IOException {
		if (strategyCb.getValue().equals("choose a strategy"))
			Platform.runLater(new Runnable() {
				@Override
				public void run() {
					Alert alert = new Alert(AlertType.ERROR);
					alert.setHeaderText("please choose a strategy!");
					alert.show();
				}
			});
		else {
			fw = new FileWriter("C:\\Users\\franc\\eclipse-workspace\\Phase2\\src\\GUI\\DataBase.txt", true);
			bw = new BufferedWriter(fw);
			pw = new PrintWriter(bw);
			pw.println(strategyCb.getValue());
			pw.flush();
			String s = null;
			Process process;
			BufferedReader in;
			String s1 = null;
			Process process1;
			BufferedReader in1;

			 process = Runtime.getRuntime().exec("python pythonScripts\\simple.py " + " "
					+ "C:\\\\Users\\\\franc\\\\eclipse-workspace\\\\Phase2\\\\src\\\\GUI\\\\DataBase.txt" + " ");


			 in = new BufferedReader(new InputStreamReader(process.getInputStream()));

			while ((s = in.readLine()) != null) {
				System.out.println(s);

			}
			
			try {
			    Thread.sleep(2000);
			} catch (InterruptedException e) {
			    // Handle interruption
			}
			
			
			process1 = Runtime.getRuntime().exec("python pythonScripts\\learning.py "+" ");


			 in1 = new BufferedReader(new InputStreamReader(process1.getInputStream()));

			while ((s1 = in1.readLine()) != null) {
				System.out.println(s1);
			}
			

			QualityController qualityController = new QualityController();
			qualityController.start(primaryStage);
		}

	}

	public void start(Stage primaryStage) {
		SetStrategyController.primaryStage = primaryStage;
		try {
			SimulatedTrafficController.primaryStage = primaryStage;
			Parent root;
			root = FXMLLoader.load(getClass().getResource("SetStrategy.fxml"));
			Scene scene = new Scene(root);
			SimulatedTrafficController.primaryStage.setScene(scene);
			SimulatedTrafficController.primaryStage.setTitle("Set Strategy");
			SimulatedTrafficController.primaryStage.show();
			SimulatedTrafficController.primaryStage.setOnCloseRequest(event -> {
				System.exit(0);
			});
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	@Override
	public void initialize(URL arg0, ResourceBundle arg1) {
		// TODO Auto-generated method stub
		strategyCb.setItems(FXCollections.observableArrayList(st));
		strategyCb.setValue("choose a strategy");
	}

}
